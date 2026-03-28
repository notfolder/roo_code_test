"""
備品スキーマ
備品の登録・編集リクエストとレスポンスのPydanticモデルを定義する
"""
from datetime import datetime
from pydantic import BaseModel, field_validator


class EquipmentCreate(BaseModel):
    """備品登録の入力定義"""
    management_number: str
    name: str
    note: str | None = None

    @field_validator("management_number")
    @classmethod
    def validate_management_number(cls, v: str) -> str:
        """管理番号は1文字以上50文字以内であること"""
        if not 1 <= len(v) <= 50:
            raise ValueError("管理番号は1文字以上50文字以内で入力してください")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """備品名は1文字以上200文字以内であること"""
        if not 1 <= len(v) <= 200:
            raise ValueError("備品名は1文字以上200文字以内で入力してください")
        return v


class EquipmentUpdate(BaseModel):
    """備品編集の入力定義"""
    management_number: str
    name: str
    note: str | None = None

    @field_validator("management_number")
    @classmethod
    def validate_management_number(cls, v: str) -> str:
        if not 1 <= len(v) <= 50:
            raise ValueError("管理番号は1文字以上50文字以内で入力してください")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not 1 <= len(v) <= 200:
            raise ValueError("備品名は1文字以上200文字以内で入力してください")
        return v


class EquipmentResponse(BaseModel):
    """備品レスポンスの定義"""
    id: int
    management_number: str
    name: str
    note: str | None
    status: str

    model_config = {"from_attributes": True}
