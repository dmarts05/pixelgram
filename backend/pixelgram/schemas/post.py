from datetime import datetime
from uuid import UUID

from pydantic import HttpUrl, field_validator

from pixelgram.schemas.camel_model import CamelModel


class PostBase(CamelModel):
    """Base schema for posts."""

    description: str
    image_url: HttpUrl

    @field_validator("description")
    @classmethod
    def description_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Description cannot be empty")
        return v

    @field_validator("image_url")
    @classmethod
    def image_url_must_not_be_empty(cls, v: HttpUrl) -> HttpUrl:
        if not v:
            raise ValueError("Image URL cannot be empty")
        return v


class PostCreate(PostBase):
    """Post schema for creating new posts."""

    user_id: UUID

    @field_validator("user_id")
    @classmethod
    def user_id_must_exist(cls, v: UUID) -> UUID:
        if v is None:
            raise ValueError("User ID cannot be empty")
        return v

    @field_validator("description")
    @classmethod
    def description_must_not_exceed_length(cls, v: str) -> str:
        if len(v) > 1000:
            raise ValueError("Description exceeds maximum length of 1000 characters")
        return v


class PostRead(PostBase):
    """Post schema for reading posts."""

    id: UUID
    user_id: UUID
    author_username: str
    author_email: str
    created_at: datetime
    likes_count: int
    liked_by_user: bool
    comments_count: int
    commented_by_user: bool
    saved_by_user: bool
