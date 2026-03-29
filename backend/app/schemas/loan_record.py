from pydantic import BaseModel
from typing import Optional
from datetime import date


class LoanCreate(BaseModel):
    equipment_id: int
    user_id: int
    loan_date: date
    purpose: Optional[str] = None


class ReturnUpdate(BaseModel):
    return_date: date


class LoanRecordResponse(BaseModel):
    id: int
    equipment_id: int
    user_id: int
    loan_date: date
    return_date: Optional[date] = None
    status: str
    purpose: Optional[str] = None
    equipment_name: Optional[str] = None
    user_name: Optional[str] = None

    model_config = {"from_attributes": True}
