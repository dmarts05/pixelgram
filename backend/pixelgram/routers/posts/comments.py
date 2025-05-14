from uuid import UUID

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Path,
    Query,
    Response,
    status,
)
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from pixelgram.auth import current_active_user
from pixelgram.db import get_async_session
from pixelgram.models.post import Post
from pixelgram.models.post_comment import PostComment
from pixelgram.models.user import User
from pixelgram.schemas.post_comment import (
    CommentResponse,
    PaginatedCommentsResponse,
    PostCommentCreate,
    PostCommentRead,
)

posts_comments_router = APIRouter(
    prefix="/{post_id}/comments",
    tags=["posts"],
)


@posts_comments_router.get(
    "/",
    summary="Retrieve paginated comments for a post",
    description="Returns a paginated list of comments on a given post.",
    responses={
        status.HTTP_200_OK: {
            "description": "A paginated list of comments",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "id": "11111111-1111-1111-1111-111111111111",
                                "postId": "00000000-0000-0000-0000-000000000001",
                                "userId": "22222222-2222-2222-2222-222222222222",
                                "authorUsername": "catlover123",
                                "authorEmail": "catlover123@example.com",
                                "content": "So cute!",
                                "createdAt": "2025-05-07T12:34:56.789012+00:00",
                                "byUser": False,
                            }
                        ],
                        "nextPage": 2,
                        "total": 15,
                    }
                }
            },
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
        status.HTTP_404_NOT_FOUND: {"description": "Post not found"},
    },
)
async def get_post_comments(
    post_id: UUID = Path(..., description="The ID of the post to fetch comments for"),
    user: User = Depends(current_active_user),
    page: int = Query(1, ge=1, description="The page number to retrieve."),
    page_size: int = Query(
        10, ge=1, le=100, description="The number of comments per page."
    ),
    db: AsyncSession = Depends(get_async_session),
) -> PaginatedCommentsResponse:
    # Check if post exists
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    # Get comments with pagination
    stmt = (
        select(PostComment)
        .where(PostComment.post_id == post_id)
        .order_by(PostComment.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .options(selectinload(PostComment.user))
    )
    result = await db.execute(stmt)
    comments = result.scalars().all()

    # Count total comments for pagination and determine next page
    count_stmt = select(func.count(PostComment.id)).where(
        PostComment.post_id == post_id
    )
    total = (await db.execute(count_stmt)).scalar() or 0
    next_page = page + 1 if (page * page_size) < total else None

    # Construct the response
    data = []
    for c in comments:
        cr = PostCommentRead(
            id=c.id,
            post_id=c.post_id,
            user_id=c.user_id,
            author_username=c.user.username,
            author_email=c.user.email,
            content=c.content,
            created_at=c.created_at,
            by_user=(c.user_id == user.id),
        )
        data.append(cr.model_dump(by_alias=True))

    return PaginatedCommentsResponse(data=data, nextPage=next_page, total=total)


@posts_comments_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Add a comment to a post",
    response_model=CommentResponse,
    responses={
        status.HTTP_201_CREATED: {"description": "Comment created"},
        status.HTTP_404_NOT_FOUND: {"description": "Post not found"},
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid input"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
    },
)
async def post_comment(
    post_id: UUID = Path(..., description="The ID of the post to comment on"),
    payload: PostCommentCreate = Body(...),
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session),
) -> CommentResponse:
    # Check if post exists
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    # Validate comment content and create comment
    try:
        comment = PostComment(
            post_id=post_id,
            user_id=user.id,
            content=payload.content,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid comment data: {str(e)}",
        )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)

    # Return the created comment
    cr = PostCommentRead(
        id=comment.id,
        post_id=comment.post_id,
        user_id=comment.user_id,
        author_username=user.username,
        author_email=user.email,
        content=comment.content,
        created_at=comment.created_at,
        by_user=True,
    )
    return CommentResponse(comment=cr)


@posts_comments_router.delete(
    "/{comment_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a comment",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Comment deleted"},
        status.HTTP_404_NOT_FOUND: {"description": "Post or comment not found"},
        status.HTTP_403_FORBIDDEN: {"description": "Not comment owner"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
    },
)
async def delete_comment(
    post_id: UUID = Path(..., description="The ID of the post"),
    comment_id: UUID = Path(..., description="The ID of the comment to delete"),
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session),
):
    # Check if post exists
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    # Check if comment exists
    stmt = select(PostComment).where(
        PostComment.id == comment_id, PostComment.post_id == post_id
    )
    result = await db.execute(stmt)
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    # Check if user is the owner of the comment
    if str(comment.user_id) != str(user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not comment owner"
        )

    # Delete the comment
    await db.delete(comment)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
