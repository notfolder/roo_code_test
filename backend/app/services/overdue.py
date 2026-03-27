"""遅延判定バッチ用サービス。"""
from datetime import date
from typing import List, Dict

from sqlalchemy.orm import Session

from app import models


class OverdueService:
    def __init__(self, db: Session):
        self.db = db

    def mark_overdue(self) -> Dict[str, int]:
        """予約・貸出の期限超過をoverdueへ更新する。
        戻り値は更新件数のサマリ。
        """
        today = date.today()
        # 予約: confirmedでend_date過ぎ
        res_updated = (
            self.db.query(models.Reservation)
            .filter(models.Reservation.status == "confirmed")
            .filter(models.Reservation.end_date < today)
        )
        res_count = res_updated.update({models.Reservation.status: "overdue"}, synchronize_session=False)

        # 貸出: loanedでdue_date過ぎ
        lend_updated = (
            self.db.query(models.Lending)
            .filter(models.Lending.status == "loaned")
            .filter(models.Lending.due_date < today)
        )
        lend_count = lend_updated.update({models.Lending.status: "overdue"}, synchronize_session=False)

        # 備品: loaned/overdueに紐づくものをoverdueへ
        equip_count = 0
        overdue_equipment_ids = {
            r.equipment_id for r in self.db.query(models.Reservation).filter(models.Reservation.status == "overdue").all()
        }
        overdue_equipment_ids |= {
            l.reservation.equipment_id for l in self.db.query(models.Lending).filter(models.Lending.status == "overdue").all()
        }
        if overdue_equipment_ids:
            equip_updated = (
                self.db.query(models.Equipment)
                .filter(models.Equipment.id.in_(list(overdue_equipment_ids)))
            )
            equip_count = equip_updated.update({models.Equipment.status: "overdue"}, synchronize_session=False)

        self.db.commit()
        return {"reservations": res_count, "lendings": lend_count, "equipments": equip_count}

    def list_overdues(self) -> List[dict]:
        """overdueの予約/貸出を一覧する（簡易情報）。"""
        today = date.today()
        items: List[dict] = []
        res = (
            self.db.query(models.Reservation)
            .filter(models.Reservation.status == "overdue")
            .all()
        )
        for r in res:
            items.append({
                "kind": "reservation",
                "reservation_id": str(r.id),
                "equipment_id": str(r.equipment_id),
                "user_id": str(r.user_id),
                "due_date": r.end_date,
            })
        lends = (
            self.db.query(models.Lending)
            .filter(models.Lending.status == "overdue")
            .all()
        )
        for l in lends:
            items.append({
                "kind": "lending",
                "lending_id": str(l.id),
                "reservation_id": str(l.reservation_id),
                "equipment_id": str(l.reservation.equipment_id),
                "user_id": str(l.reservation.user_id),
                "due_date": l.due_date,
            })
        return items

