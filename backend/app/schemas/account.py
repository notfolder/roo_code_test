"""
アカウントスキーマ
アカウント作成リクエストとレスポンスのPydanticモデルを定義する
"""
from datetime import datetime
from pydantic import BaseModel, field_validator


class AccountCreate(BaseModel):
    """アカウント作成の入力定義"""
    account_name: str
    password: str
    role: str

    @field_validator("account_name")
    @classmethod
    def validate_account_name(cls, v: str) -> str:
        """アカウント名は1文字以上100文字以内であること"""
        if not 1 <= len(v) <= 100:
            raise ValueError("アカウント名は1文字以上100文字以内で入力してください")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """パスワードは8文字以上であること"""
        if len(v) < 8:
            raise ValueError("パスワードは8文字以上で入力してください")
        return v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        """役割はadminまたはemployeeのみ有効"""
        if v not in ("admin", "employee"):
            raise ValueError("役割はadminまたはemployeeを指定してください")
        return v


class AccountResponse(BaseModel):
    """アカウントレスポンスの定義"""
    id: int
    account_name: str
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}
