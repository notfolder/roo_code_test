from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from app.models.reservation import Reservation
from app.repositories.base import BaseRepository


class ReservationRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(Reservation, db)

    def get_by_user_id(self, user_id: int) -> List[Reservation]:
        return self.db.query(Reservation).filter(Reservation.user_id == user_id).all()

    def get_pending_by_equipment(self, equipment_id: int) -> List[Reservation]:
        return (
            self.db.query(Reservation)
            .filter(Reservation.equipment_id == equipment_id, Reservation.status == "pending")
            .all()
        )

    def check_overlap(self, equipment_id: int, start_date: date, end_date: date) -> bool:
        """指定備品のpending予約の中に期間重複があればTrueを返す（SELECT FOR UPDATE）"""
        result = (
            self.db.query(Reservation)
            .filter(
                Reservation.equipment_id == equipment_id,
                Reservation.status == "pending",
                Reservation.planned_start_date <= end_date,
                Reservation.planned_return_date >= start_date,
            )
            .with_for_update()
            .first()
        )
        return result is not None

    def cancel(self, id: int) -> Optional[Reservation]:
        reservation = (
            self.db.query(Reservation)
            .filter(Reservation.id == id)
            .with_for_update()
            .first()
        )
        if reservation:
            reservation.status = "cancelled"
            self.db.flush()
        return reservation

    def mark_as_loaned(self, equipment_id: int) -> Optional[Reservation]:
        """指定備品のpending予約の最古の1件をloaned状態に更新する"""
        reservation = (
            self.db.query(Reservation)
            .filter(Reservation.equipment_id == equipment_id, Reservation.status == "pending")
            .order_by(Reservation.created_at)
            .with_for_update()
            .first()
        )
        if reservation:
            reservation.status = "loaned"
            self.db.flush()
        return reservation
