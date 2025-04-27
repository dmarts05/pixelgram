import uuid

from fastapi_users import schemas
from pydantic import field_validator


class UserRead(schemas.BaseUser[uuid.UUID]):
    """User schema for reading user data."""

    username: str


class UserCreate(schemas.BaseUserCreate):
    """User schema for creating new users."""

    username: str

    @field_validator("username")
    @classmethod
    def username_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Username cannot be empty")
        return v


class UserUpdate(schemas.BaseUserUpdate):
    """User schema for updating user data."""

    username: str | None = None

    @field_validator("username")
    @classmethod
    def username_must_not_be_empty(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("Username cannot be empty")
        return v
