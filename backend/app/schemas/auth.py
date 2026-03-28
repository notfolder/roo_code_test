"""
認証スキーマ
ログインリクエストとJWTトークンレスポンスのPydanticモデルを定義する
"""
from pydantic import BaseModel


class LoginRequest(BaseModel):
    """ログインリクエストの入力定義"""
    account_name: str
    password: str


class TokenResponse(BaseModel):
    """JWTトークンレスポンスの定義"""
    access_token: str
    token_type: str = "bearer"
    role: str
