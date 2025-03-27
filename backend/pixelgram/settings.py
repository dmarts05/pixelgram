from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    db_uri: str = ""


settings = Settings()
"""Application settings instance"""
