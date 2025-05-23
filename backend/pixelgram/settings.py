from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    db_uri: str = ""
    secret: str = ""
    google_auth_client_id: str = ""
    google_oauth_client_secret: str = ""
    frontend_base_url: str = ""
    hf_token: str = ""
    hf_img2txt_model: str = ""
    supabase_url: str = ""
    supabase_service_key: str = ""
    supabase_bucket: str = ""
    max_img_mb_size: float = 5


settings = Settings()
"""Application settings instance"""


def get_settings() -> Settings:
    """
    Dependency to get settings.
    This function is a dependency that can be used in FastAPI routes.
    """
    return Settings()
