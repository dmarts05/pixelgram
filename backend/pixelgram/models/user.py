from fastapi_users.db import (
    SQLAlchemyBaseUserTableUUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pixelgram.models.base import Base
from pixelgram.models.oauth_account import OAuthAccount


class User(SQLAlchemyBaseUserTableUUID, Base):
    """User model for FastAPI Users."""

    username: Mapped[str] = mapped_column(index=True)
    oauth_accounts: Mapped[list[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )
