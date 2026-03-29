from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class LoanCreate(BaseModel):
    equipment_id: int
    borrower_user_id: int
    loan_date: date


class ReturnUpdate(BaseModel):
    return_date: date


class LoanRecordResponse(BaseModel):
    id: int
    equipment_id: int
    equipment_name: Optional[str] = None
    equipment_management_number: Optional[str] = None
    user_id: int
    user_name: Optional[str] = None
    loan_date: date
    return_date: Optional[date] = None
    status: str

    model_config = {"from_attributes": True}
