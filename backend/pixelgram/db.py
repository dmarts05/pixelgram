from collections.abc import AsyncGenerator
from typing import Coroutine

from fastapi import Depends
from fastapi_users.db import (
    SQLAlchemyUserDatabase,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from pixelgram.models.base import Base
from pixelgram.models.oauth_account import OAuthAccount
from pixelgram.models.user import User
from pixelgram.settings import settings

engine = create_async_engine(settings.db_uri)
"""Engine for the database"""

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
"""Session maker for the database"""


async def create_db_and_tables() -> Coroutine | None:
    """Create the database and tables if they do not exist."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get an async session for the database.
    This function is a dependency that can be used in FastAPI routes.
    """
    async with async_session_maker() as session:
        yield session


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    """
    Get user table from the database.
    This function is a dependency that can be used in FastAPI routes.
    """
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)
