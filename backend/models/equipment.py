from typing import Optional

from pydantic import BaseModel, field_validator


class EquipmentCreate(BaseModel):
    """備品登録リクエストスキーマ"""

    management_number: str
    name: str
    equipment_type: str

    @field_validator("management_number", "name", "equipment_type")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("空文字は指定できません")
        return v.strip()


class EquipmentUpdate(BaseModel):
    """備品更新リクエストスキーマ"""

    management_number: str
    name: str
    equipment_type: str

    @field_validator("management_number", "name", "equipment_type")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("空文字は指定できません")
        return v.strip()


class EquipmentResponse(BaseModel):
    """備品レスポンススキーマ"""

    id: int
    management_number: str
    name: str
    equipment_type: str
    status: str
    borrower_name: Optional[str] = None
    created_at: str
    updated_at: str
