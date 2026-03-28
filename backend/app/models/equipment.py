"""
備品ORMモデル
equipmentテーブルのマッピングを定義する
"""
from datetime import datetime
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Equipment(Base):
    """備品テーブルのORMモデル"""
    __tablename__ = "equipment"

    # 内部ID（主キー）
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # 管理番号（備品を一意に識別する番号）
    management_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    # 備品名
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    # 備考（任意）
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    # 貸出状態（available=貸出可能、borrowed=貸出中）
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="available")
    # 作成日時（自動設定）
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    # 更新日時（更新時に自動設定）
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # 貸出記録との関連
    loan_records: Mapped[list] = relationship("LoanRecord", back_populates="equipment")
