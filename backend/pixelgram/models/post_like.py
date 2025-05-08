from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pixelgram.models.base import Base

if TYPE_CHECKING:
    from pixelgram.models.post import Post
    from pixelgram.models.user import User


class PostLike(Base):
    """Represents a like on a post by a user. A user can only like a post once."""

    __tablename__ = "post_like"
    __table_args__ = (UniqueConstraint("user_id", "post_id", name="uq_post_user"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    post_id: Mapped[UUID] = mapped_column(
        ForeignKey("post.id", ondelete="CASCADE"),
        nullable=False,
    )
    liked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user: Mapped[User] = relationship("User", back_populates="post_likes")
    post: Mapped[Post] = relationship("Post", back_populates="post_likes")
