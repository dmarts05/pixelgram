from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from pixelgram.auth import current_active_user
from pixelgram.db import get_async_session
from pixelgram.models.user import User
from pixelgram.schemas.user import UserPublicInfo
from pixelgram.services.user_service import UserService, get_user_service

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@users_router.get(
    "/{id}/info",
    summary="Get username by user ID",
    description="Returns the username associated with the given user ID.",
    response_model=UserPublicInfo,
    responses={
        200: {
            "description": "Username successfully retrieved",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "username": "john_doe",
                    }
                }
            },
        },
        404: {
            "description": "User not found",
            "content": {"application/json": {"example": {"detail": "User not found."}}},
        },
        401: {"description": "Unauthorized"},
    },
)
async def get_username_by_id(
    id: UUID,
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session),
    user_service: UserService = Depends(get_user_service),
):
    """
    Get username by user ID.
    """
    return await get_user_service(db).get_username_by_id(id)
