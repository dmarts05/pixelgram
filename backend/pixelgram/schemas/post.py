from uuid import UUID
from datetime import datetime

from pydantic import field_validator, BaseModel, HttpUrl


class PostBase(BaseModel):
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


class PostRead(PostBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
