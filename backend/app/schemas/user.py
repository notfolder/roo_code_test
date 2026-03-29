from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    login_id: str
    name: str
    password: str
    role: str = "general"


class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    login_id: str
    name: str
    role: str
    is_active: bool

    model_config = {"from_attributes": True}
