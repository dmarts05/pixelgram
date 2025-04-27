from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    db_uri: str = ""
    secret: str = ""
    google_auth_client_id: str = ""
    google_oauth_client_secret: str = ""
    frontend_base_url: str = ""


settings = Settings()
"""Application settings instance"""
