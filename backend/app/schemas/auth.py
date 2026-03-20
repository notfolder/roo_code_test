"""認証関連のPydanticスキーマ。"""

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="メールアドレス")
    password: str = Field(..., min_length=8, description="パスワード")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

