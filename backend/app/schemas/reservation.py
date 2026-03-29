from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class ReservationCreate(BaseModel):
    equipment_id: int
    planned_start_date: date
    planned_return_date: date


class ReservationResponse(BaseModel):
    id: int
    equipment_id: int
    equipment_name: Optional[str] = None
    user_id: int
    user_name: Optional[str] = None
    planned_start_date: date
    planned_return_date: date
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
