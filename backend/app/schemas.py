from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]


class UserOut(UserBase):
    id: str
    role: str
    status: str

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    asset_number: str
    name: str


class ItemCreate(ItemBase):
    state: Optional[str] = None


class ItemUpdate(BaseModel):
    name: Optional[str]
    state: Optional[str]


class ItemOut(ItemBase):
    id: str
    state: str
    current_user_id: Optional[str]
    current_user_name: Optional[str]
    updated_at: datetime

    class Config:
        orm_mode = True


class LoanRequest(BaseModel):
    user_id: str


class LoanOut(BaseModel):
    id: str
    item_id: str
    user_id: str
    lent_at: datetime
    returned_at: Optional[datetime]

    class Config:
        orm_mode = True
