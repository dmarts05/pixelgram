from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
)

from pixelgram.models.base import Base


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    """OAuth account model for FastAPI Users."""

    pass
