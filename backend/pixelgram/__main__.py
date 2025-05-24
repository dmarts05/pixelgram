from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from pixelgram.auth import (
    fastapi_users,
)
from pixelgram.db import create_db_and_tables
from pixelgram.limiter import limiter
from pixelgram.routers.auth import auth_router
from pixelgram.routers.captions import captions_router
from pixelgram.routers.posts.posts import posts_router
from pixelgram.routers.users import users_router
from pixelgram.schemas.user import UserRead, UserUpdate
from pixelgram.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


# App
app = FastAPI(
    title="Pixelgram API",
    description="Pixelgram is a social network for creating and sharing pixel art.",
    version="1.0.0",
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_base_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore

# Routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(captions_router)
app.include_router(posts_router)


@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok"}
