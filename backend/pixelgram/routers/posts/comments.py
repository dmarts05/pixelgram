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
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pixelgram.auth import current_active_user
from pixelgram.db import get_async_session
from pixelgram.models.post import Post
from pixelgram.models.post_comment import PostComment
from pixelgram.models.user import User
from pixelgram.schemas.post_comment import (
    CommentResponse,
    PaginatedCommentsResponse,
    PostCommentCreate,
)
from pixelgram.services.posts.comment_service import (
    CommentService,
    get_comment_service,
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
    comment_service: CommentService = Depends(get_comment_service),
) -> PaginatedCommentsResponse:
    # Check if post exists
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return await comment_service.get_by_post_id(
        post_id=post_id,
        page=page,
        page_size=page_size,
        solicitor_id=user.id,
    )


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
    comment_service: CommentService = Depends(get_comment_service),
) -> CommentResponse:
    # Check if post exists
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return await comment_service.post_comment(
        post_id=post_id, user=user, content=payload.content
    )


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
    comment_service: CommentService = Depends(get_comment_service),
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

    await comment_service.delete_comment(comment)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
