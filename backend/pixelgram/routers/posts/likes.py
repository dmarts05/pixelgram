from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    Response,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from pixelgram.auth import current_active_user
from pixelgram.db import get_async_session
from pixelgram.models.post import Post
from pixelgram.models.user import User
from pixelgram.services.posts.like_service import LikeService, get_like_service

post_likes_router = APIRouter(
    prefix="/{post_id}/like",
    tags=["posts"],
)


@post_likes_router.post(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Like a post",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Post liked"},
        status.HTTP_404_NOT_FOUND: {"description": "Post not found"},
        status.HTTP_409_CONFLICT: {"description": "Already liked"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
    },
)
async def like_post(
    post_id: UUID = Path(..., description="The ID of the post to like"),
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session),
    like_service: LikeService = Depends(get_like_service),
):
    # Check if post exists
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    await like_service.like_post(post_id, user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@post_likes_router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Unlike a post",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Post unliked"},
        status.HTTP_400_BAD_REQUEST: {"description": "Post not liked"},
        status.HTTP_404_NOT_FOUND: {"description": "Post not found"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
    },
)
async def unlike_post(
    post_id: UUID = Path(..., description="The ID of the post to unlike"),
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session),
    like_service: LikeService = Depends(get_like_service),
):
    # Check if post exists
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    await like_service.unlike_post(post_id, user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
