"""
アカウントORMモデル
accountsテーブルのマッピングを定義する
"""
from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Account(Base):
    """アカウントテーブルのORMモデル"""
    __tablename__ = "accounts"

    # 内部ID（主キー）
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # アカウント名（ログインID、一意制約）
    account_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    # bcryptハッシュ化済みパスワード
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    # 役割（admin=管理担当者、employee=一般社員）
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    # 作成日時（自動設定）
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # 借りた貸出記録との関連（borrower側）
    loan_records_as_borrower: Mapped[list] = relationship(
        "LoanRecord",
        foreign_keys="LoanRecord.borrower_account_id",
        back_populates="borrower",
    )
    # 操作した貸出記録との関連（operator側）
    loan_records_as_operator: Mapped[list] = relationship(
        "LoanRecord",
        foreign_keys="LoanRecord.operated_by_account_id",
        back_populates="operator",
    )
