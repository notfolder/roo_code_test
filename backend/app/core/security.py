"""認証・認可関連のユーティリティ。"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from backend.app.core.config import settings


# bcrypt は72バイトを超えるパスワードでエラーになるため、明示的に72バイトで切り詰める
_BCRYPT_MAX_BYTES = 72

# bcrypt を利用したハッシュ/検証用コンテキスト
# bcrypt__truncate_error=False で 72 バイト超の入力でも自動で先頭72バイトに丸めてエラーにしない
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__truncate_error=False,
    bcrypt__ident="2b",
)


def _normalize_password(password: str) -> str:
    """bcrypt の上限 72 バイトを超えないよう、必ず先頭72バイトで丸める。"""

    if not isinstance(password, str):
        password = str(password)

    # 一律で 72 バイトに丸める（UTF-8 の不完全な末尾は破棄）
    truncated = password.encode("utf-8")[:_BCRYPT_MAX_BYTES]
    safe = truncated.decode("utf-8", errors="ignore")

    # 念のため再エンコード後も 72 バイト以下であることを保証
    if len(safe.encode("utf-8")) > _BCRYPT_MAX_BYTES:
        safe = safe.encode("utf-8")[:_BCRYPT_MAX_BYTES].decode("utf-8", errors="ignore")

    return safe


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """平文パスワードとハッシュの照合（72バイト制限対応）。"""

    return pwd_context.verify(_normalize_password(plain_password), hashed_password)


def get_password_hash(password: str) -> str:
    """パスワードをハッシュ化（72バイト制限対応）。"""

    return pwd_context.hash(_normalize_password(password))


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
