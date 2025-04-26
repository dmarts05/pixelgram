from contextlib import asynccontextmanager

from fastapi import FastAPI

from pixelgram.auth import (
    auth_backend,
    fastapi_users,
    google_oauth_client,
)
from pixelgram.db import create_db_and_tables
from pixelgram.schemas.user import UserCreate, UserRead, UserUpdate
from pixelgram.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, settings.secret),
    prefix="/auth/google",
    tags=["auth"],
)
