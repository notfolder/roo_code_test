from pydantic import BaseModel
from datetime import datetime


class EquipmentCreate(BaseModel):
    management_number: str
    name: str


class EquipmentUpdate(BaseModel):
    name: str


class EquipmentResponse(BaseModel):
    id: int
    management_number: str
    name: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
