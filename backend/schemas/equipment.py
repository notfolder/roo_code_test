"""備品関連のPydanticスキーマ"""
from pydantic import BaseModel
from typing import Optional


class EquipmentCreate(BaseModel):
    code: str
    name: str


class EquipmentUpdate(BaseModel):
    name: str


class LendRequest(BaseModel):
    borrower_name: str


class EquipmentResponse(BaseModel):
    id: int
    code: str
    name: str
    status: str
    borrower_name: Optional[str] = None

    model_config = {"from_attributes": True}
