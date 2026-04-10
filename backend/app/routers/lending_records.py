from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user, require_admin
from app.models.user import User
from app.schemas.lending_record import LendingRecordCreate, ReturnRequest, LendingRecordResponse
from app.services.lending_service import LendingService

router = APIRouter(prefix="/api/lending_records", tags=["lending_records"])
lending_service = LendingService()


@router.get("", response_model=List[LendingRecordResponse])
def get_lending_records(
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return lending_service.get_lending_records(db)


@router.post("", response_model=LendingRecordResponse, status_code=201)
def create_lending_record(
    record_create: LendingRecordCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    return lending_service.create_lending_record(db, record_create)


@router.put("/{record_id}/return", response_model=LendingRecordResponse)
def return_item(
    record_id: int,
    return_request: ReturnRequest,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    return lending_service.return_item(db, record_id, return_request)
