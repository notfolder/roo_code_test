from pydantic import BaseModel
from typing import Optional
from datetime import date


class LendingRecordCreate(BaseModel):
    item_id: str
    borrower_user_id: int
    lend_date: date


class ReturnRequest(BaseModel):
    return_date: date


class LendingRecordResponse(BaseModel):
    id: int
    item_id: str
    item_name: str
    borrower_name: str
    lend_date: date
    return_date: Optional[date] = None

    model_config = {"from_attributes": True}
