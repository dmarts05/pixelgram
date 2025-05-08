from datetime import datetime
from uuid import UUID

from pydantic import field_validator

from pixelgram.schemas.camel_model import CamelModel


class PostCommentBase(CamelModel):
    """Base schema for post comments."""

    content: str

    @field_validator("content")
    @classmethod
    def content_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Content cannot be empty")
        return v

    @field_validator("content")
    @classmethod
    def content_must_not_exceed_length(cls, v: str) -> str:
        if len(v) > 1000:
            raise ValueError("Content exceeds maximum length of 1000 characters")
        return v


class PostCommentCreate(PostCommentBase):
    """PostComment schema for creating new comments."""

    pass


class PostCommentRead(PostCommentBase):
    """PostComment schema for reading comments."""

    id: UUID
    post_id: UUID
    user_id: UUID
    author_username: str
    author_email: str
    created_at: datetime
    by_user: bool
