from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from sqlmodel import Session, SQLModel, create_engine

from pixelgram.settings import settings

engine = create_engine(settings.db_uri)
"""SQLModel engine to connect to the database"""


def create_db_and_tables():
    """Create the database and tables if they don't exist."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get a new session from the engine."""
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def init_db_lifespan(app: FastAPI):
    """
    Initialize the database and tables when the app starts.

    :param app: FastAPI application instance
    """
    create_db_and_tables()
    yield
