"""認証・認可関連のユーティリティ。"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.exc import PasswordSizeError

from backend.app.core.config import settings


# パスワードハッシュ方式: 長さ制限の少ない pbkdf2_sha256 を利用
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto",
    pbkdf2_sha256__rounds=29000,
)


def _normalize_password(password: str) -> str:
    """pbkdf2_sha256 用に文字列化のみを行う（長さ制限なし）。"""

    return password if isinstance(password, str) else str(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """平文パスワードとハッシュの照合（72バイト制限対応）。"""

    return pwd_context.verify(_normalize_password(plain_password), hashed_password)


def get_password_hash(password: str) -> str:
    """パスワードをハッシュ化（72バイト制限対応）。"""

    normalized = _normalize_password(password)
    return pwd_context.hash(normalized)


def create_access_token(subject: str, expires_minutes: int | None = None) -> str:
    """JWT を発行する。subject はユーザーID。"""

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.access_token_expire_minutes
    )
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")


def decode_access_token(token: str) -> Optional[str]:
    """JWT を検証し、ユーザーIDを返す。無効時は None。"""

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        return str(payload.get("sub"))
    except JWTError:
        return None
