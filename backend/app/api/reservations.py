"""予約API。"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.database import get_db
from app.services.reservations import ReservationService

router = APIRouter()


@router.get("", response_model=list[schemas.ReservationOut])
def list_reservations(db: Session = Depends(get_db), current=Depends(deps.get_current_user)):
    # userは自分のみ、adminは全件
    user_id = None if current.role == "admin" else str(current.id)
    return ReservationService(db).list(user_id=user_id)


@router.post("", response_model=schemas.ReservationOut)
def create_reservation(payload: schemas.ReservationCreate, db: Session = Depends(get_db), current=Depends(deps.get_current_user)):
    return ReservationService(db).create(user_id=str(current.id), equipment_id=payload.equipment_id, start=payload.start_date, end=payload.end_date)


@router.put("/{reservation_id}", response_model=schemas.ReservationOut)
def update_reservation(reservation_id: str, payload: schemas.ReservationUpdate, db: Session = Depends(get_db), current=Depends(deps.get_current_user)):
    reservation = ReservationService(db).get(reservation_id)
    # 権限制御: 本人またはadmin
    if current.role != "admin" and str(reservation.user_id) != str(current.id):
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="権限がありません")
    return ReservationService(db).update(reservation_id, **payload.dict(exclude_unset=True))


@router.delete("/{reservation_id}", response_model=schemas.ReservationOut)
def cancel_reservation(reservation_id: str, db: Session = Depends(get_db), current=Depends(deps.get_current_user)):
    reservation = ReservationService(db).get(reservation_id)
    if current.role != "admin" and str(reservation.user_id) != str(current.id):
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="権限がありません")
    return ReservationService(db).cancel(reservation_id)


@router.get("/{reservation_id}", response_model=schemas.ReservationOut)
def get_reservation(reservation_id: str, db: Session = Depends(get_db), current=Depends(deps.get_current_user)):
    reservation = ReservationService(db).get(reservation_id)
    if current.role != "admin" and str(reservation.user_id) != str(current.id):
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="権限がありません")
    return reservation

