from pydantic import BaseModel
from typing import Optional


class EquipmentCreate(BaseModel):
    name: str
    category: str
    notes: Optional[str] = None


class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    notes: Optional[str] = None


class EquipmentResponse(BaseModel):
    id: int
    name: str
    category: str
    status: str
    notes: Optional[str] = None

    model_config = {"from_attributes": True}
