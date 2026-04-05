from fastapi import APIRouter, Depends

from common.auth import get_current_admin
from models.lending_record import LendingCreate, LendingRecordResponse, LendingReturn
from services.lending_service import LendingService

router = APIRouter(prefix="/api/lending", tags=["貸出・返却"])

_lending_service = LendingService()


@router.get("", response_model=list[LendingRecordResponse])
def get_lending_history(_: dict = Depends(get_current_admin)):
    """全貸出履歴を取得する（認証必要）"""
    return _lending_service.get_history()


@router.get("/active", response_model=list[LendingRecordResponse])
def get_active_lending(_: dict = Depends(get_current_admin)):
    """貸出中レコードを取得する（認証必要）"""
    return _lending_service.get_active()


@router.post("", response_model=LendingRecordResponse, status_code=201)
def create_lending(data: LendingCreate, _: dict = Depends(get_current_admin)):
    """貸出記録を登録する（認証必要）"""
    return _lending_service.lend(data.model_dump())


@router.put("/{record_id}/return", response_model=LendingRecordResponse)
def return_lending(
    record_id: int, data: LendingReturn, _: dict = Depends(get_current_admin)
):
    """返却記録を登録する（認証必要）"""
    return _lending_service.return_item(record_id, data.returned_at)
