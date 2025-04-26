from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTableUUID

from pixelgram.models.base import Base


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    """Access token table for the database."""

    pass
