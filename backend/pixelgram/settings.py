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
    supabase_key: str = ""
    supabase_bucket: str = ""

settings = Settings()
"""Application settings instance"""
