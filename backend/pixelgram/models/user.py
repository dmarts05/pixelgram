from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi_users.db import (
    SQLAlchemyBaseUserTableUUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pixelgram.models.base import Base
from pixelgram.models.oauth_account import OAuthAccount

if TYPE_CHECKING:
    from pixelgram.models.post import Post
    from pixelgram.models.post_comment import PostComment
    from pixelgram.models.post_like import PostLike
    from pixelgram.models.post_saved import PostSaved


class User(SQLAlchemyBaseUserTableUUID, Base):
    """User model for FastAPI Users."""

    username: Mapped[str] = mapped_column(index=True)
    oauth_accounts: Mapped[list[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )
    posts: Mapped[list[Post]] = relationship("Post", back_populates="author")
    post_likes: Mapped[list[PostLike]] = relationship(
        "PostLike",
        back_populates="user",
    )
    post_comments: Mapped[list[PostComment]] = relationship(
        "PostComment", back_populates="user", cascade="all, delete-orphan"
    )

    posts_saved: Mapped[list[PostSaved]] = relationship(
        "PostSaved",
        back_populates="user",
    )

    @property
    def liked_posts(self) -> list[Post]:
        return [pl.post for pl in self.post_likes]
