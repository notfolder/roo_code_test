"""JWTトークンの生成・検証（共通処理）"""
import os
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import HTTPException, status

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "change-this-secret-key-in-production")
ALGORITHM = "HS256"
EXPIRE_HOURS = int(os.environ.get("JWT_EXPIRE_HOURS", "8"))


class JWTUtil:
    @staticmethod
    def create_token(payload: dict) -> str:
        """ペイロードからJWTトークンを生成する（有効期限を付与）"""
        data = payload.copy()
        expire = datetime.now(timezone.utc) + timedelta(hours=EXPIRE_HOURS)
        data["exp"] = expire
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict:
        """JWTトークンをデコードしてペイロードを返す。無効な場合は例外を発生させる"""
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="セッションが切れました。再ログインしてください",
            )
