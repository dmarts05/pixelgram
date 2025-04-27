from contextlib import asynccontextmanager

from fastapi import FastAPI

from pixelgram.auth import (
    fastapi_users,
)
from pixelgram.db import create_db_and_tables
from pixelgram.routers.auth import auth_router
from pixelgram.schemas.user import UserRead, UserUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(
    title="Pixelgram API",
    description="Pixelgram is a social network for creating and sharing pixel art.",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(auth_router)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
