from pydantic import BaseModel, field_validator


class LoginRequest(BaseModel):
    """ログインリクエストスキーマ"""

    login_id: str
    password: str

    @field_validator("login_id", "password")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("空文字は指定できません")
        return v


class TokenResponse(BaseModel):
    """JWTトークンレスポンススキーマ"""

    access_token: str
    token_type: str = "bearer"
