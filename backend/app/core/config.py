"""設定値の管理モジュール。環境変数から読み込み、サービス全体で共有する。
"""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """アプリ全体で利用する設定値を管理するクラス。"""

    app_name: str = "asset-reservation"
    secret_key: str = "change-me"  # 本番では必ず上書き
    access_token_expire_minutes: int = 60 * 24
    database_url: str = "postgresql+asyncpg://app:app@db:5432/app"
    # CORS 許可オリジン（複数あればカンマ区切り）
    cors_allow_origins: str = "http://localhost:5173"
    admin_email: str = "admin@example.com"
    admin_password: str = "AdminPass123"


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
