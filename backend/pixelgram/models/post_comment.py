from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pixelgram.models.base import Base

if TYPE_CHECKING:
    from pixelgram.models.post import Post
    from pixelgram.models.user import User


class PostComment(Base):
    """Represents a comment on a post by a user."""

    __tablename__ = "post_comment"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    post_id: Mapped[UUID] = mapped_column(
        ForeignKey("post.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    post: Mapped[Post] = relationship("Post", back_populates="post_comments")
    user: Mapped[User] = relationship("User", back_populates="post_comments")
