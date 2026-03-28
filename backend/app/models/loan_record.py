"""
貸出記録ORMモデル
loan_recordsテーブルのマッピングを定義する
"""
from datetime import datetime
from sqlalchemy import Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class LoanRecord(Base):
    """貸出記録テーブルのORMモデル"""
    __tablename__ = "loan_records"

    # 内部ID（主キー）
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # 貸出対象備品のID（外部キー）
    equipment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("equipment.id"), nullable=False
    )
    # 借りた社員のアカウントID（外部キー）
    borrower_account_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("accounts.id"), nullable=False
    )
    # 操作した管理担当者のアカウントID（外部キー）
    operated_by_account_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("accounts.id"), nullable=False
    )
    # 貸出日時（自動設定）
    loaned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    # 返却日時（返却前はNULL）
    returned_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # 備品との関連
    equipment: Mapped["Equipment"] = relationship(  # noqa: F821
        "Equipment", back_populates="loan_records"
    )
    # 借りた社員との関連
    borrower: Mapped["Account"] = relationship(  # noqa: F821
        "Account",
        foreign_keys=[borrower_account_id],
        back_populates="loan_records_as_borrower",
    )
    # 操作した管理担当者との関連
    operator: Mapped["Account"] = relationship(  # noqa: F821
        "Account",
        foreign_keys=[operated_by_account_id],
        back_populates="loan_records_as_operator",
    )
