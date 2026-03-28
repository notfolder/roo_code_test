"""
セキュリティモジュール
パスワードのbcryptハッシュ化・検証と、JWTトークンの生成・検証を担う共通モジュール
"""
import os
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt

# bcryptによるパスワードハッシュ化コンテキスト
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT署名に使用する秘密鍵（環境変数から取得）
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production-secret-key-32chars")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", "8"))


def hash_password(plain_password: str) -> str:
    """
    平文パスワードをbcryptでハッシュ化して返す
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    平文パスワードとbcryptハッシュを照合し、一致すればTrueを返す
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    指定されたデータを含むJWTアクセストークンを生成して返す
    有効期限はACCESS_TOKEN_EXPIRE_HOURS時間後に設定する
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    JWTトークンをデコードしてペイロード辞書を返す
    トークンが無効または期限切れの場合はJWTErrorを送出する
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
