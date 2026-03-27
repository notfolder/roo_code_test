"""貸出サービス: 状態整合と日付チェック。"""
from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models
from app.repositories import ReservationRepository, LendingRepository, EquipmentRepository


class LendingService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = LendingRepository(db)
        self.reservation_repo = ReservationRepository(db)
        self.equipment_repo = EquipmentRepository(db)

    def create(self, reservation_id: str, lent_by: str, lend_date: date) -> models.Lending:
        reservation = self.reservation_repo.get(reservation_id)
        if not reservation:
            raise HTTPException(status_code=404, detail="予約が存在しません")
        if reservation.status != "confirmed":
            raise HTTPException(status_code=409, detail="予約が確定状態ではありません")
        equipment = self.equipment_repo.get(reservation.equipment_id)
        if not equipment:
            raise HTTPException(status_code=404, detail="備品が存在しません")
        if lend_date < reservation.start_date:
            raise HTTPException(status_code=400, detail="貸出日は予約開始日以降にしてください")
        due_date = reservation.end_date
        if self.repo.get_by_reservation(reservation_id):
            raise HTTPException(status_code=409, detail="すでに貸出登録済みです")

        lending = models.Lending(
            reservation_id=reservation_id,
            lent_by=lent_by,
            lend_date=lend_date,
            due_date=due_date,
            status="loaned",
        )

        # 状態更新: 予約→finished?（設計は貸出で予約終了扱いでOK/ここではloanedに合わせ後段で更新）
        reservation.status = "finished"
        equipment.status = "loaned"

        self.db.add(lending)
        self.db.commit()
        self.db.refresh(lending)
        return lending

    def list(self):
        return self.repo.list()

    def get(self, lending_id: str) -> models.Lending:
        lending = self.repo.get(lending_id)
        if not lending:
            raise HTTPException(status_code=404, detail="貸出が存在しません")
        return lending

