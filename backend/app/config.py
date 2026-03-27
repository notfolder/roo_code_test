"""アプリ設定の読み込み（環境変数ベース）。"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """環境変数を用いた設定クラス。
    デフォルト値はローカル開発用。"""

    database_url: str = "postgresql+psycopg2://appuser:apppass@db:5432/appdb"
    jwt_secret: str = "devsecret"
    access_token_expire_minutes: int = 60 * 24
    admin_email: str = "admin@example.com"
    admin_password: str = "adminpass123"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

