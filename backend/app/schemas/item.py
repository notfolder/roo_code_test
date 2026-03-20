"""備品のPydanticスキーマ。"""

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class ItemBase(BaseModel):
    item_code: str = Field(..., max_length=50, description="備品コード")
    name: str = Field(..., max_length=255, description="備品名称")
    status: str = Field("active", description="active/retired")


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    status: str | None = Field(None)


class ItemRead(ItemBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

