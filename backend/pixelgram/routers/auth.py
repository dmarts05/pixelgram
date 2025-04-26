from fastapi import APIRouter

from pixelgram.auth import (
    auth_backend,
    fastapi_users,
    google_oauth_client,
)
from pixelgram.schemas.user import UserCreate, UserRead
from pixelgram.settings import settings

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)
auth_router.include_router(fastapi_users.get_auth_router(auth_backend))
auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
auth_router.include_router(
    fastapi_users.get_reset_password_router(),
)
auth_router.include_router(
    fastapi_users.get_verify_router(UserRead),
)
auth_router.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, settings.secret),
    prefix="/google",
)
