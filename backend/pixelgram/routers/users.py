from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from pixelgram.auth import UserManager, current_active_user, get_user_manager
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
    return await user_service.get_username_by_id(id)


@users_router.delete(
    "/me",
    summary="Delete your account",
    description="Deletes the account of the currently authenticated user.",
    response_model=None,
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Comment deleted"},
        401: {"description": "Unauthorized"},
    },
)
async def delete_me(
    user: User = Depends(current_active_user),
    user_manager: UserManager = Depends(get_user_manager),
):
    await user_manager.delete(user, None)
    return status.HTTP_204_NO_CONTENT
