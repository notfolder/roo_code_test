from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Item, LoanRecord, OperationLog, User


class LoanService:
    @staticmethod
    def lend_item(db: Session, item_id: str, user_id: str, actor_id: str) -> LoanRecord:
        try:
            item = db.scalar(select(Item).where(Item.id == item_id).with_for_update())
            if not item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
                )
            if item.state != "available":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Item already lent"
                )

            target_user = db.scalar(
                select(User).where(User.id == user_id, User.status == "active")
            )
            if not target_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user"
                )

            loan_record = db.scalar(
                select(LoanRecord).where(LoanRecord.item_id == item.id)
            )
            now = datetime.now(timezone.utc)
            if loan_record:
                loan_record.user_id = user_id
                loan_record.lent_at = now
                loan_record.returned_at = None
            else:
                loan_record = LoanRecord(item_id=item.id, user_id=user_id, lent_at=now)
                db.add(loan_record)

            item.state = "lent"
            item.current_user_id = user_id
            db.add(
                OperationLog(
                    action="lend",
                    actor_user_id=actor_id,
                    item_id=item_id,
                    target_user_id=user_id,
                )
            )
            db.commit()
        except HTTPException:
            db.rollback()
            raise

        db.refresh(loan_record)
        return loan_record

    @staticmethod
    def return_item(db: Session, item_id: str, actor_id: str) -> LoanRecord:
        try:
            item = db.scalar(select(Item).where(Item.id == item_id).with_for_update())
            if not item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
                )

            loan_record = db.scalar(
                select(LoanRecord).where(LoanRecord.item_id == item.id)
            )
            if not loan_record or loan_record.returned_at is not None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Active loan record not found",
                )

            loan_record.returned_at = datetime.now(timezone.utc)
            item.state = "available"
            item.current_user_id = None
            db.add(
                OperationLog(action="return", actor_user_id=actor_id, item_id=item_id)
            )
            db.commit()
        except HTTPException:
            db.rollback()
            raise

        db.refresh(loan_record)
        return loan_record
