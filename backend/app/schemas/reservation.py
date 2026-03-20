"""予約関連のPydanticスキーマ。"""

from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel, Field, validator


class ReservationBase(BaseModel):
    item_id: UUID
    start_date: date
    end_date: date

    @validator("end_date")
    def validate_range(cls, v, values):
        start = values.get("start_date")
        if start and v < start:
            raise ValueError("end_dateはstart_date以降である必要があります")
        if start and (v - start).days > 6:  # 7日以内
            raise ValueError("最大7日までです")
        return v


class ReservationCreate(ReservationBase):
    pass


class ReservationRead(ReservationBase):
    id: UUID
    status: str
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

