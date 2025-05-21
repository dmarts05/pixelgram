from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from pixelgram.db import get_async_session
from pixelgram.models.post_like import PostLike


class LikeService:
    """
    Service for managing likes on posts.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def like_post(self, post_id: UUID, user_id: UUID) -> None:
        """
        Asynchronously likes a post on behalf of a user.
        Checks if the user has already liked the specified post. If so, raises an HTTP 409 Conflict exception.
        Otherwise, adds a like to the post by the user and commits the change to the database.
        Args:
            post_id (UUID): The unique identifier of the post to like.
            user_id (UUID): The unique identifier of the user liking the post.
        Raises:
            HTTPException: If the user has already liked the post (HTTP 409 Conflict).
        """

        # Check if user has already liked the post
        stmt = select(PostLike).where(
            PostLike.post_id == post_id, PostLike.user_id == user_id
        )
        if (await self.db.execute(stmt)).scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Post already liked"
            )

        # Add like
        self.db.add(PostLike(post_id=post_id, user_id=user_id))
        await self.db.commit()

    async def unlike_post(self, post_id: UUID, user_id: UUID) -> None:
        """
        Asynchronously removes a like from a post by a specific user.
        Args:
            post_id (UUID): The unique identifier of the post to unlike.
            user_id (UUID): The unique identifier of the user unliking the post.
        Raises:
            HTTPException: If the user has not previously liked the post, raises a 400 Bad Request error.
        Returns:
            None
        """

        # Delete like
        delete_stmt = (
            delete(PostLike)
            .where(PostLike.post_id == post_id, PostLike.user_id == user_id)
            .execution_options(synchronize_session="fetch")
        )
        result = await self.db.execute(delete_stmt)
        # If like was not deleted, it means the user didn't like the post in the first place
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Post not liked"
            )
        await self.db.commit()


def get_like_service(db: AsyncSession = Depends(get_async_session)) -> LikeService:
    """
    Dependency to get the LikeService instance.
    """
    return LikeService(db)
