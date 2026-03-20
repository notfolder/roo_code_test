"""ユーザー関連のPydanticスキーマ。"""

from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="メールアドレス")
    name: str = Field(..., max_length=100, description="氏名")
    role: str = Field(..., description="general/admin")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="パスワード")


class UserRead(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

