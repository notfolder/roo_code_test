"""
貸出記録リポジトリ
loan_recordsテーブルに対するDB操作を集約する
"""
from datetime import datetime, timezone
from sqlalchemy.orm import Session, joinedload

from app.models.loan_record import LoanRecord
from app.schemas.loan import LoanCreate


class LoanRepository:
    """貸出記録テーブルの操作を提供するリポジトリ"""

    @staticmethod
    def find_all(db: Session) -> list[LoanRecord]:
        """
        全貸出記録を貸出日時の降順で取得する
        関連する備品・借りた社員・操作した管理担当者を結合取得する
        """
        return (
            db.query(LoanRecord)
            .options(
                joinedload(LoanRecord.equipment),
                joinedload(LoanRecord.borrower),
                joinedload(LoanRecord.operator),
            )
            .order_by(LoanRecord.loaned_at.desc())
            .all()
        )

    @staticmethod
    def find_active_by_equipment(db: Session, equipment_id: int) -> LoanRecord | None:
        """
        指定備品の未返却（returned_at IS NULL）の貸出記録を取得する
        返却操作の対象を特定するために使用する
        """
        return (
            db.query(LoanRecord)
            .filter(
                LoanRecord.equipment_id == equipment_id,
                LoanRecord.returned_at.is_(None),
            )
            .first()
        )

    @staticmethod
    def find_by_id(db: Session, loan_id: int) -> LoanRecord | None:
        """
        IDで貸出記録を取得する
        関連する備品・借りた社員・操作した管理担当者を結合取得する
        """
        return (
            db.query(LoanRecord)
            .options(
                joinedload(LoanRecord.equipment),
                joinedload(LoanRecord.borrower),
                joinedload(LoanRecord.operator),
            )
            .filter(LoanRecord.id == loan_id)
            .first()
        )

    @staticmethod
    def create(db: Session, data: LoanCreate, operator_id: int) -> LoanRecord:
        """
        貸出記録を新規作成してDBに保存する
        """
        loan = LoanRecord(
            equipment_id=data.equipment_id,
            borrower_account_id=data.borrower_account_id,
            operated_by_account_id=operator_id,
        )
        db.add(loan)
        db.flush()
        # 関連オブジェクトをロードするためにIDで再取得する
        return LoanRepository.find_by_id(db, loan.id)

    @staticmethod
    def set_returned(db: Session, loan: LoanRecord) -> LoanRecord:
        """
        貸出記録に返却日時（現在時刻）を設定する
        """
        loan.returned_at = datetime.now(timezone.utc)
        db.flush()
        db.refresh(loan)
        return loan
