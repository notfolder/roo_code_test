"""Pydanticスキーマ（API入出力用）。"""
from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field, validator


# 共通スキーマ
class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: str = Field(..., regex="^(user|admin)$")
    status: str = Field(..., regex="^(active|inactive)$")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    name: Optional[str]
    role: Optional[str] = Field(None, regex="^(user|admin)$")
    status: Optional[str] = Field(None, regex="^(active|inactive)$")
    password: Optional[str] = Field(None, min_length=8)


class UserOut(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    token: str
    user: UserOut


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class EquipmentBase(BaseModel):
    name: str
    category: Optional[str]
    model: Optional[str]
    serial_no: Optional[str]
    asset_tag: Optional[str]
    purchase_date: Optional[date]
    note: Optional[str]
    status: str = Field(..., regex="^(available|reserved|loaned|overdue|retired)$")


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(BaseModel):
    name: Optional[str]
    category: Optional[str]
    model: Optional[str]
    serial_no: Optional[str]
    asset_tag: Optional[str]
    purchase_date: Optional[date]
    note: Optional[str]
    status: Optional[str] = Field(None, regex="^(available|reserved|loaned|overdue|retired)$")


class EquipmentOut(EquipmentBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ReservationBase(BaseModel):
    equipment_id: str
    start_date: date
    end_date: date

    @validator("end_date")
    def validate_range(cls, v, values):
        start_date = values.get("start_date")
        if start_date and v < start_date:
            raise ValueError("終了日は開始日以降にしてください")
        return v


class ReservationCreate(ReservationBase):
    pass


class ReservationUpdate(BaseModel):
    start_date: Optional[date]
    end_date: Optional[date]
    status: Optional[str] = Field(None, regex="^(confirmed|cancelled|finished|overdue)$")
    cancel_reason: Optional[str]


class ReservationOut(ReservationBase):
    id: str
    user_id: str
    status: str
    cancel_reason: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LendingCreate(BaseModel):
    reservation_id: str
    lend_date: date


class LendingOut(BaseModel):
    id: str
    reservation_id: str
    lent_by: str
    lend_date: date
    due_date: date
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ReturnCreate(BaseModel):
    lending_id: str
    return_date: date
    condition_note: Optional[str]


class ReturnOut(BaseModel):
    id: str
    lending_id: str
    returned_by: str
    return_date: date
    condition_note: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True


class OverdueOut(BaseModel):
    reservation_id: str
    equipment_id: str
    user_id: str
    due_date: date
    kind: str  # reservation/lending


class HistoryOut(BaseModel):
    kind: str
    id: str
    date: date
    equipment_id: str
    user_id: str
    info: str

