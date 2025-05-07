from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pixelgram.models.base import Base

if TYPE_CHECKING:
    from pixelgram.models.post_like import PostLike
    from pixelgram.models.user import User


class Post(Base):
    """Represents a pixel art post uploaded by a user."""

    __tablename__ = "post"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    description: Mapped[str] = mapped_column(String, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    author: Mapped[User] = relationship(back_populates="posts")
    post_likes: Mapped[list[PostLike]] = relationship(
        "PostLike",
        back_populates="post",
    )

    @property
    def like_count(self) -> int:
        return len(self.post_likes)
