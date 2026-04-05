import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from common.errors import UnauthorizedError

# bcryptハッシュコンテキスト
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWTの有効期限（8時間）
_ACCESS_TOKEN_EXPIRE_HOURS = 8

_security = HTTPBearer(auto_error=False)


def _get_secret_key() -> str:
    """JWT署名キーを環境変数から取得する"""
    return os.environ.get("JWT_SECRET_KEY", "change-me-in-production")


def verify_password(plain_password: str, password_hash: str) -> bool:
    """平文パスワードとbcryptハッシュを照合する"""
    return _pwd_context.verify(plain_password, password_hash)


def create_access_token(data: dict) -> str:
    """JWTアクセストークンを生成する"""
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=_ACCESS_TOKEN_EXPIRE_HOURS)
    payload.update({"exp": expire})
    return jwt.encode(payload, _get_secret_key(), algorithm="HS256")


def decode_token(token: str) -> Optional[dict]:
    """JWTトークンを検証してペイロードを返す。無効または期限切れの場合はNoneを返す"""
    try:
        payload = jwt.decode(token, _get_secret_key(), algorithms=["HS256"])
        return payload
    except JWTError:
        return None


def get_current_admin(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_security),
) -> dict:
    """認証済み管理者情報を返すFastAPI Dependency。未認証の場合は例外を送出する"""
    if credentials is None:
        raise UnauthorizedError("認証が必要です。ログインしてください")
    payload = decode_token(credentials.credentials)
    if payload is None:
        raise UnauthorizedError("認証が必要です。再ログインしてください")
    return payload
