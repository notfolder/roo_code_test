from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    asset_number: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=255)
    state: str = Field(pattern="^(available|lent)$")


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    state: str = Field(pattern="^(available|lent)$")


class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    asset_number: str
    name: str
    state: str
    current_user_id: str | None = None
    current_user_name: str | None = None
    updated_at: datetime


class LoanRequest(BaseModel):
    user_id: str


class LoanRecordResponse(BaseModel):
    id: str
    item_id: str
    user_id: str
    lent_at: datetime
    returned_at: datetime | None = None
