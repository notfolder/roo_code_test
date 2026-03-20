"""認証・認可関連のユーティリティ。"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from backend.app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """平文パスワードとハッシュの照合。"""

    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """パスワードをハッシュ化。"""

    return pwd_context.hash(password)


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
