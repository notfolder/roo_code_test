from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    login_id: str
    name: str
    password: str
    role: str = "general"


class UserResponse(BaseModel):
    id: int
    login_id: str
    name: str
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}
