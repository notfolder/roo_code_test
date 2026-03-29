from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user, require_admin
from app.services.reservation import ReservationService
from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=ReservationResponse, status_code=201)
def create_reservation(
    data: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReservationService(db).create_reservation(data, current_user)


@router.get("/", response_model=List[ReservationResponse])
def list_reservations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReservationService(db).get_reservations(current_user)


@router.get("/pending/{equipment_id}", response_model=List[ReservationResponse])
def list_pending_by_equipment(
    equipment_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """S3（貸出登録画面）用: 指定備品のpending予約一覧を管理者のみ取得できる"""
    return ReservationService(db).get_pending_by_equipment(equipment_id)


@router.put("/{id}/cancel", response_model=ReservationResponse)
def cancel_reservation(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReservationService(db).cancel_reservation(id, current_user)
