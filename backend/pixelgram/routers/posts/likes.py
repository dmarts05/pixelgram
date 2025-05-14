from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    Response,
    status,
)
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from pixelgram.auth import current_active_user
from pixelgram.db import get_async_session
from pixelgram.models.post import Post
from pixelgram.models.post_like import PostLike
from pixelgram.models.user import User

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
):
    # Check if post exists
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    # Check if user has already liked the post
    stmt = select(PostLike).where(
        PostLike.post_id == post_id, PostLike.user_id == user.id
    )
    if (await db.execute(stmt)).scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Post already liked"
        )

    # Add like
    db.add(PostLike(post_id=post_id, user_id=user.id))
    await db.commit()
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
):
    # Check if post exists
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    # Delete like
    delete_stmt = (
        delete(PostLike)
        .where(PostLike.post_id == post_id, PostLike.user_id == user.id)
        .execution_options(synchronize_session="fetch")
    )
    result = await db.execute(delete_stmt)
    # If like was not deleted, it means the user didn't like the post in the first place
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Post not liked"
        )
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
