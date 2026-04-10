from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    secret_key: str = "supersecretkey"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    db_url: str = "postgresql://postgres:postgres@db:5432/asset_db"
    admin_email: str = "admin@example.com"
    admin_password: str = "adminpassword"
    api_prefix: str = "/api"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
