from pydantic import BaseModel
from typing import Literal


class UserCreate(BaseModel):
    login_id: str
    password: str
    role: Literal["admin", "user"]


class UserResponse(BaseModel):
    id: int
    login_id: str
    role: str

    model_config = {"from_attributes": True}
