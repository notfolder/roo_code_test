"""返却サービス: 貸出と予約・備品の状態復帰。"""
from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models
from app.repositories import LendingRepository, ReturnRepository, EquipmentRepository, ReservationRepository


class ReturnService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ReturnRepository(db)
        self.lending_repo = LendingRepository(db)
        self.equipment_repo = EquipmentRepository(db)
        self.reservation_repo = ReservationRepository(db)

    def create(self, lending_id: str, returned_by: str, return_date: date, condition_note: str | None = None) -> models.Return:
        lending = self.lending_repo.get(lending_id)
        if not lending:
            raise HTTPException(status_code=404, detail="貸出が存在しません")
        if lending.status != "loaned" and lending.status != "overdue":
            raise HTTPException(status_code=409, detail="返却可能な状態ではありません")
        if return_date < lending.lend_date:
            raise HTTPException(status_code=400, detail="返却日は貸出日以降にしてください")
        if self.repo.get_by_lending(lending_id):
            raise HTTPException(status_code=409, detail="すでに返却登録済みです")

        ret = models.Return(
            lending_id=lending_id,
            returned_by=returned_by,
            return_date=return_date,
            condition_note=condition_note,
        )

        # 状態更新: 貸出→returned、備品→available、予約→finished
        lending.status = "returned"
        reservation = lending.reservation
        equipment = self.equipment_repo.get(reservation.equipment_id)
        reservation.status = "finished"
        equipment.status = "available"

        self.db.add(ret)
        self.db.commit()
        self.db.refresh(ret)
        return ret

    def list(self):
        return self.repo.list()

    def get(self, return_id: str) -> models.Return:
        ret = self.repo.get(return_id)
        if not ret:
            raise HTTPException(status_code=404, detail="返却が存在しません")
        return ret

