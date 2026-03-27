"""予約サービス: 重複チェックとバリデーション。"""
from datetime import date

from fastapi import HTTPException
from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app import models
from app.common.validators import validate_reservation_range
from app.repositories import ReservationRepository, EquipmentRepository


class ReservationService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ReservationRepository(db)
        self.equip_repo = EquipmentRepository(db)

    def _check_overlap(self, equipment_id: str, start: date, end: date, exclude_id: str | None = None):
        # daterange重複を簡易にチェック（設計書ではGIST EXCLUDEを推奨、ここではアプリ側でもガード）
        q = (
            self.db.query(models.Reservation)
            .filter(models.Reservation.equipment_id == equipment_id)
            .filter(models.Reservation.status == "confirmed")
            .filter(models.Reservation.start_date <= end)
            .filter(models.Reservation.end_date >= start)
        )
        if exclude_id:
            q = q.filter(models.Reservation.id != exclude_id)
        exists = self.db.query(q.exists()).scalar()
        if exists:
            raise HTTPException(status_code=409, detail="同一期間に予約があります")

    def create(self, user_id: str, equipment_id: str, start: date, end: date) -> models.Reservation:
        validate_reservation_range(start, end)
        if not self.equip_repo.get(equipment_id):
            raise HTTPException(status_code=404, detail="備品が存在しません")
        self._check_overlap(equipment_id, start, end)
        reservation = models.Reservation(
            equipment_id=equipment_id,
            user_id=user_id,
            start_date=start,
            end_date=end,
            status="confirmed",
        )
        return self.repo.add(reservation)

    def update(self, reservation_id: str, **kwargs) -> models.Reservation:
        reservation = self.repo.get(reservation_id)
        if not reservation:
            raise HTTPException(status_code=404, detail="予約が存在しません")
        start = kwargs.get("start_date", reservation.start_date)
        end = kwargs.get("end_date", reservation.end_date)
        validate_reservation_range(start, end)
        if reservation.status not in ("confirmed", "overdue"):
            raise HTTPException(status_code=409, detail="現在の状態では変更できません")
        self._check_overlap(reservation.equipment_id, start, end, exclude_id=reservation_id)
        reservation.start_date = start
        reservation.end_date = end
        if "status" in kwargs and kwargs["status"]:
            reservation.status = kwargs["status"]
        if "cancel_reason" in kwargs:
            reservation.cancel_reason = kwargs["cancel_reason"]
        return self.repo.update(reservation)

    def cancel(self, reservation_id: str) -> models.Reservation:
        reservation = self.repo.get(reservation_id)
        if not reservation:
            raise HTTPException(status_code=404, detail="予約が存在しません")
        if reservation.status != "confirmed":
            raise HTTPException(status_code=409, detail="キャンセルできません")
        reservation.status = "cancelled"
        return self.repo.update(reservation)

    def list(self, user_id: str | None = None):
        return self.repo.list(user_id=user_id)

    def get(self, reservation_id: str) -> models.Reservation:
        reservation = self.repo.get(reservation_id)
        if not reservation:
            raise HTTPException(status_code=404, detail="予約が存在しません")
        return reservation

