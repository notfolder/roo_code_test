"""予約エンドポイント。"""

from fastapi import APIRouter, Depends

from backend.app.schemas.reservation import ReservationCreate, ReservationRead
from backend.app.services.reservation import ReservationService
from backend.app.api.deps import DBSession
from backend.app.core.deps import get_current_user, require_admin

router = APIRouter(prefix="/reservations", tags=["reservations"])


@router.get("", response_model=list[ReservationRead], dependencies=[Depends(get_current_user)])
async def list_my_reservations(db: DBSession, current_user=Depends(get_current_user)):
    service = ReservationService(db)
    return await service.list_my(current_user.id)


@router.post("", response_model=ReservationRead, dependencies=[Depends(get_current_user)])
async def create_reservation(data: ReservationCreate, db: DBSession, current_user=Depends(get_current_user)):
    service = ReservationService(db)
    return await service.create(current_user.id, data)


@router.post("/{reservation_id}/cancel", response_model=ReservationRead, dependencies=[Depends(get_current_user)])
async def cancel_reservation(reservation_id, db: DBSession, current_user=Depends(get_current_user)):
    service = ReservationService(db)
    return await service.cancel(reservation_id, current_user.id)


@router.get("/all", response_model=list[ReservationRead], dependencies=[Depends(require_admin)])
async def list_all_reservations(db: DBSession):
    service = ReservationService(db)
    return await service.list_all()
