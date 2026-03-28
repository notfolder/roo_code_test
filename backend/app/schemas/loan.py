"""
貸出スキーマ
貸出登録リクエストとレスポンスのPydanticモデルを定義する
"""
from datetime import datetime
from pydantic import BaseModel


class LoanCreate(BaseModel):
    """貸出登録の入力定義"""
    equipment_id: int
    borrower_account_id: int


class LoanResponse(BaseModel):
    """貸出記録レスポンスの定義"""
    id: int
    equipment_id: int
    management_number: str
    equipment_name: str
    borrower_name: str
    operator_name: str
    loaned_at: datetime
    returned_at: datetime | None

    model_config = {"from_attributes": True}
