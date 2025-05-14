from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    Query,
    Response,
    status,
)
from pydantic import HttpUrl
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from pixelgram.auth import current_active_user
from pixelgram.db import get_async_session
from pixelgram.models.post import Post
from pixelgram.models.post_comment import PostComment
from pixelgram.models.post_like import PostLike
from pixelgram.models.post_saved import PostSaved
from pixelgram.models.user import User
from pixelgram.schemas.post import (
    PaginatedPostsResponse,
    PostRead,
)

saved_posts_router = APIRouter(
    tags=["posts"],
)


@saved_posts_router.post(
    "/{post_id}/save/",
    summary="Save a specific post by ID",
    description="Saves a post for the current user.",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Post saved successfully"},
        status.HTTP_404_NOT_FOUND: {"description": "Post not found"},
        status.HTTP_409_CONFLICT: {"description": "Post already saved"},
    },
)
async def save_post(
    post_id: UUID = Path(..., description="The ID of the post to save"),
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Save a post for the current user.
    """

    # Check if post exists
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    # Check if user has already saved the post
    stmt = select(PostSaved).where(
        PostSaved.post_id == post_id, PostSaved.user_id == user.id
    )

    if (await db.execute(stmt)).scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Post already saved"
        )

    # Add save
    db.add(PostSaved(post_id=post_id, user_id=user.id))
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@saved_posts_router.delete(
    "/{post_id}/save/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Unsave a specific post by ID",
    description="Removes a post from the saved list for the current user.",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Post unsaved successfully"},
        status.HTTP_400_BAD_REQUEST: {"description": "Post not saved"},
        status.HTTP_404_NOT_FOUND: {"description": "Post not found"},
    },
)
async def unsave_post(
    post_id: UUID = Path(..., description="The ID of the post to unsave"),
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Remove a post from the saved list for the current user.
    """
    # Check if post exists
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    # Delete save
    delete_stmt = (
        delete(PostSaved)
        .where(PostSaved.post_id == post_id, PostSaved.user_id == user.id)
        .execution_options(synchronize_session="fetch")
    )
    result = await db.execute(delete_stmt)
    # If save was not deleted, it means the user didn't save the post in the first place
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Post not saved"
        )
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@saved_posts_router.get(
    "/saved/",
    summary="Get all saved posts",
    description="Retrieves all posts saved by the current user.",
    responses={
        status.HTTP_200_OK: {
            "description": "List of paginated saved posts",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "id": "00000000-0000-0000-0000-000000000001",
                                "description": "A cat sitting on a chair",
                                "imageUrl": "https://example.com/image.png",
                                "userId": "00000000-0000-0000-0000-000000000001",
                                "authorUsername": "catlover123",
                                "authorEmail": "catlover123@email.com",
                            }
                        ]
                    }
                }
            },
        }
    },
)
async def get_saved_posts(
    # user_id: UUID = Path(..., description="The user ID to filter posts by."),
    user: User = Depends(current_active_user),
    page: int = Query(1, ge=1, description="The page number to retrieve."),
    page_size: int = Query(
        10, ge=1, le=100, description="The number of posts per page."
    ),
    # user_id: str | None = Query(None, description="The user ID to filter posts by."),
    db: AsyncSession = Depends(get_async_session),
) -> PaginatedPostsResponse:
    """
    Get all saved posts for the current user.
    """

    if not user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID"
        )
    # 1. Get all post IDs saved by the current user
    saved_posts_ids_stmt = select(PostSaved.post_id).where(PostSaved.user_id == user.id)
    result = await db.execute(saved_posts_ids_stmt)
    saved_posts_ids = [row[0] for row in result.fetchall()]

    if not saved_posts_ids:
        return PaginatedPostsResponse(data=[], nextPage=None, total=0)

    stmt = (
        select(Post)
        .where(Post.id.in_(saved_posts_ids))
        .order_by(Post.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .options(
            selectinload(Post.author),
            selectinload(Post.post_likes),
            selectinload(Post.post_comments),
        )
    )

    result = await db.execute(stmt)
    saved_posts = result.scalars().all()

    # Count total saved posts for pagination and determine next page
    count_stmt = select(func.count(PostSaved.id))
    if user.id:
        count_stmt = count_stmt.where(PostSaved.user_id == user.id)
    total = (await db.execute(count_stmt)).scalar() or 0
    next_page = page + 1 if (page * page_size) < total else None

    # Fetch likes count for each post
    likes_stmt = (
        select(PostLike.post_id, func.count(PostLike.user_id))
        .where(PostLike.post_id.in_(saved_posts_ids))
        .group_by(PostLike.post_id)
    )
    likes_result = await db.execute(likes_stmt)
    likes_map = {post_id: count for post_id, count in likes_result.all()}

    # Fetch liked posts by the user
    liked_stmt = select(PostLike.post_id).where(
        PostLike.post_id.in_(saved_posts_ids), PostLike.user_id == user.id
    )
    liked_result = await db.execute(liked_stmt)
    liked_post_ids = {post_id for (post_id,) in liked_result.all()}

    # Fetch comments count for each post
    comments_stmt = (
        select(PostComment.post_id, func.count(PostComment.id))
        .where(PostComment.post_id.in_(saved_posts_ids))
        .group_by(PostComment.post_id)
    )
    comments_result = await db.execute(comments_stmt)
    comments_map = {post_id: count for post_id, count in comments_result.all()}

    # Fetch commented posts by the user
    commented_stmt = select(PostComment.post_id).where(
        PostComment.post_id.in_(saved_posts_ids), PostComment.user_id == user.id
    )
    commented_result = await db.execute(commented_stmt)
    commented_post_ids = {post_id for (post_id,) in commented_result.all()}

    # Construct the response
    data = []
    for saved_post in saved_posts:
        pr = PostRead(
            id=saved_post.id,
            description=saved_post.description,
            image_url=HttpUrl(saved_post.image_url),
            user_id=saved_post.user_id,
            author_username=saved_post.author.username,
            author_email=saved_post.author.email,
            created_at=saved_post.created_at,
            likes_count=likes_map.get(saved_post.id, 0),
            liked_by_user=saved_post.id in liked_post_ids,
            comments_count=comments_map.get(saved_post.id, 0),
            commented_by_user=saved_post.id in commented_post_ids,
            saved_by_user=True,
        )
        data.append(pr.model_dump(by_alias=True))

    return PaginatedPostsResponse(data=data, nextPage=next_page, total=total)
