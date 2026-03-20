"""予約モデル定義。"""

import uuid
from sqlalchemy import Column, Date, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID, DATERANGE
from sqlalchemy.sql import func
from sqlalchemy import Index, ExcludeConstraint
from sqlalchemy import func as sa_func

from backend.app.core.database import Base


class Reservation(Base):
    """予約エンティティ。"""

    __tablename__ = "reservations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False, default="reserved")  # reserved/cancelled
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    # item_id と利用日付範囲に対する排他制約（重複予約防止）。
    __table_args__ = (
        ExcludeConstraint(
            (item_id, "="),
            (sa_func.daterange(start_date, end_date, "[]"), "&&"),
            name="excl_reservations_item_daterange",
            using="gist",
        ),
    )


# item_id + daterange に対する重複禁止のためのインデックスを追加予定（alembicでも扱えるように）。
Index(
    "idx_reservations_item_date",
    Reservation.item_id,
    Reservation.start_date,
    Reservation.end_date,
)
