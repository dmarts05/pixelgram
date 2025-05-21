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
from sqlalchemy.ext.asyncio import AsyncSession

from pixelgram.auth import current_active_user
from pixelgram.db import get_async_session
from pixelgram.models.post import Post
from pixelgram.models.user import User
from pixelgram.schemas.post import (
    PaginatedPostsResponse,
)
from pixelgram.services.posts.saved_service import SavedService, get_saved_service

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
    saved_service: SavedService = Depends(get_saved_service),
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
    await saved_service.save_post(post_id, user.id)
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
    saved_service: SavedService = Depends(get_saved_service),
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
    await saved_service.unsave_post(post_id, user.id)
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
    user: User = Depends(current_active_user),
    page: int = Query(1, ge=1, description="The page number to retrieve."),
    page_size: int = Query(
        10, ge=1, le=100, description="The number of posts per page."
    ),
    db: AsyncSession = Depends(get_async_session),
    saved_service: SavedService = Depends(get_saved_service),
) -> PaginatedPostsResponse:
    """
    Get all saved posts for the current user.
    """

    if not user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID"
        )

    return await saved_service.get_saved_posts(
        user_id=user.id, page=page, page_size=page_size
    )
