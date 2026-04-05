from typing import Optional

from pydantic import BaseModel, field_validator


class LendingCreate(BaseModel):
    """貸出記録登録リクエストスキーマ"""

    equipment_id: int
    borrower_name: str
    lent_at: str

    @field_validator("borrower_name", "lent_at")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("空文字は指定できません")
        return v.strip()


class LendingReturn(BaseModel):
    """返却記録登録リクエストスキーマ"""

    returned_at: str

    @field_validator("returned_at")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("空文字は指定できません")
        return v.strip()


class LendingRecordResponse(BaseModel):
    """貸出記録レスポンススキーマ"""

    id: int
    equipment_id: int
    management_number: str
    name: str
    borrower_name: str
    lent_at: str
    returned_at: Optional[str] = None
    created_at: str
