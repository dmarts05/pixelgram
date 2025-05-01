from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pixelgram.models.base import Base

if TYPE_CHECKING:
    from pixelgram.models.user import User
else:
    User = "User"

class Post(Base):
    """Post model for Pixelart posts."""

    __tablename__ = "posts"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    description: Mapped[str] = mapped_column(String, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=False)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    author: Mapped[User] = relationship("User", back_populates="posts")
