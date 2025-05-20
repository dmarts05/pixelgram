from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pixelgram.models.user import User
from pixelgram.schemas.user import UserPublicInfo


class UserService:
    """
    User service to handle custom user-related operations.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_username_by_id(
        self,
        id: UUID,
    ) -> UserPublicInfo:
        """
        Get username by user ID.
        """
        result = await self.db.execute(select(User).filter_by(id=id))
        user_row = result.unique().scalar_one_or_none()
        if not user_row:
            raise HTTPException(status_code=404, detail="User not found.")

        return UserPublicInfo(
            id=user_row.id,
            username=user_row.username,
        )


def get_user_service(
    db: AsyncSession,
) -> UserService:
    """
    Dependency to get the User service.
    """
    return UserService(db)
