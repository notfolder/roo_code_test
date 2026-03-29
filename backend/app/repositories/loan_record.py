from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.loan_record import LoanRecord
from app.repositories.base import BaseRepository


class LoanRecordRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(LoanRecord, db)

    def list_active(self) -> List[LoanRecord]:
        return self.db.query(LoanRecord).filter(LoanRecord.status == "active").all()

    def get_active_by_equipment(self, equipment_id: int) -> Optional[LoanRecord]:
        return (
            self.db.query(LoanRecord)
            .filter(LoanRecord.equipment_id == equipment_id, LoanRecord.status == "active")
            .with_for_update()
            .first()
        )
