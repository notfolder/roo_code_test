from datetime import date
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.reservation import ReservationRepository
from app.repositories.equipment import EquipmentRepository
from app.models.reservation import Reservation
from app.models.user import User
from app.schemas.reservation import ReservationCreate, ReservationResponse


class ReservationService:
    def __init__(self, db: Session):
        self.reservation_repo = ReservationRepository(db)
        self.equipment_repo = EquipmentRepository(db)
        self.db = db

    def get_reservations(self, current_user: User) -> List[ReservationResponse]:
        if current_user.role == "admin":
            reservations = self.reservation_repo.list()
        else:
            reservations = self.reservation_repo.get_by_user_id(current_user.id)
        return [self._to_response(r) for r in reservations]

    def get_pending_by_equipment(self, equipment_id: int) -> List[ReservationResponse]:
        reservations = self.reservation_repo.get_pending_by_equipment(equipment_id)
        return [self._to_response(r) for r in reservations]

    def create_reservation(self, data: ReservationCreate, current_user: User) -> ReservationResponse:
        today = date.today()
        if data.planned_start_date < today:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="貸出開始予定日は本日以降の日付を入力してください",
            )
        if data.planned_return_date < data.planned_start_date:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="返却予定日は貸出開始予定日以降の日付を入力してください",
            )
        equipment = self.equipment_repo.get(data.equipment_id)
        if not equipment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="備品が存在しません")

        if self.reservation_repo.check_overlap(data.equipment_id, data.planned_start_date, data.planned_return_date):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="指定期間に同一備品の予約が既に存在します",
            )

        reservation = Reservation(
            equipment_id=data.equipment_id,
            user_id=current_user.id,
            planned_start_date=data.planned_start_date,
            planned_return_date=data.planned_return_date,
            status="pending",
        )
        self.reservation_repo.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)
        return self._to_response(reservation)

    def cancel_reservation(self, id: int, current_user: User) -> ReservationResponse:
        reservation = (
            self.db.query(Reservation)
            .filter(Reservation.id == id)
            .with_for_update()
            .first()
        )
        if not reservation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="予約が存在しません")
        if current_user.role != "admin" and reservation.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="この予約をキャンセルする権限がありません",
            )
        if reservation.status != "pending":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="予約中の予約のみキャンセルできます",
            )
        reservation.status = "cancelled"
        self.db.commit()
        self.db.refresh(reservation)
        return self._to_response(reservation)

    def _to_response(self, reservation: Reservation) -> ReservationResponse:
        equipment = self.equipment_repo.get(reservation.equipment_id)
        from app.repositories.user import UserRepository
        user_repo = UserRepository(self.db)
        user = user_repo.get(reservation.user_id)
        return ReservationResponse(
            id=reservation.id,
            equipment_id=reservation.equipment_id,
            equipment_name=equipment.name if equipment else None,
            user_id=reservation.user_id,
            user_name=user.name if user else None,
            planned_start_date=reservation.planned_start_date,
            planned_return_date=reservation.planned_return_date,
            status=reservation.status,
            created_at=reservation.created_at,
        )
