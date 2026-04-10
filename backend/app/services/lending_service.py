from typing import List
from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.item import Item
from app.models.lending_record import LendingRecord
from app.models.user import User
from app.schemas.lending_record import LendingRecordCreate, ReturnRequest, LendingRecordResponse


class LendingService:
    def get_lending_records(self, db: Session) -> List[LendingRecordResponse]:
        rows = (
            db.query(LendingRecord, Item.name, User.login_id)
            .join(Item, Item.id == LendingRecord.item_id)
            .join(User, User.id == LendingRecord.borrower_user_id)
            .all()
        )
        result = []
        for record, item_name, borrower_name in rows:
            result.append(
                LendingRecordResponse(
                    id=record.id,
                    item_id=record.item_id,
                    item_name=item_name,
                    borrower_name=borrower_name,
                    lend_date=record.lend_date,
                    return_date=record.return_date,
                )
            )
        return result

    def create_lending_record(
        self, db: Session, record_create: LendingRecordCreate
    ) -> LendingRecordResponse:
        item = db.query(Item).filter(Item.id == record_create.item_id).first()
        if not item or item.status != "available":
            raise HTTPException(status_code=409, detail="この備品は既に貸出中です")

        record = LendingRecord(
            item_id=record_create.item_id,
            borrower_user_id=record_create.borrower_user_id,
            lend_date=record_create.lend_date,
        )
        db.add(record)
        item.status = "lending"
        db.commit()
        db.refresh(record)

        user = db.query(User).filter(User.id == record_create.borrower_user_id).first()
        return LendingRecordResponse(
            id=record.id,
            item_id=record.item_id,
            item_name=item.name,
            borrower_name=user.login_id if user else "",
            lend_date=record.lend_date,
            return_date=record.return_date,
        )

    def return_item(
        self, db: Session, record_id: int, return_request: ReturnRequest
    ) -> LendingRecordResponse:
        record = (
            db.query(LendingRecord)
            .filter(LendingRecord.id == record_id, LendingRecord.return_date.is_(None))
            .first()
        )
        if not record:
            raise HTTPException(status_code=409, detail="この貸出記録は既に返却済みです")

        record.return_date = return_request.return_date
        item = db.query(Item).filter(Item.id == record.item_id).first()
        item.status = "available"
        db.commit()
        db.refresh(record)

        user = db.query(User).filter(User.id == record.borrower_user_id).first()
        return LendingRecordResponse(
            id=record.id,
            item_id=record.item_id,
            item_name=item.name,
            borrower_name=user.login_id if user else "",
            lend_date=record.lend_date,
            return_date=record.return_date,
        )
