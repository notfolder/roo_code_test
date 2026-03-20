"""貸出のPydanticスキーマ。"""

from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel, Field


class LoanCreate(BaseModel):
    reservation_id: UUID


class LoanReturn(BaseModel):
    actual_return_date: date


class LoanRead(BaseModel):
    id: UUID
    reservation_id: UUID
    loan_start_date: date
    planned_return_date: date
    actual_return_date: date | None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

