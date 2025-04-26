from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    db_uri: str = ""
    secret: str = ""
    token_lifetime_seconds: int = 3600
    google_auth_client_id: str = ""
    google_oauth_client_secret: str = ""


settings = Settings()
"""Application settings instance"""
