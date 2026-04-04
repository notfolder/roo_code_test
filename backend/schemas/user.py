"""ユーザー関連のPydanticスキーマ"""
from pydantic import BaseModel
from typing import Literal


class LoginRequest(BaseModel):
    login_id: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    role: str
    username: str


class UserCreate(BaseModel):
    login_id: str
    username: str
    password: str
    role: Literal["admin", "staff"]


class UserUpdate(BaseModel):
    username: str
    role: Literal["admin", "staff"]


class UserResponse(BaseModel):
    id: int
    login_id: str
    username: str
    role: str

    model_config = {"from_attributes": True}
