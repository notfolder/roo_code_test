"""貸出モデル定義。"""

import uuid
from sqlalchemy import Column, Date, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from backend.app.core.database import Base


class Loan(Base):
    """貸出エンティティ。"""

    __tablename__ = "loans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reservation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("reservations.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    loan_start_date = Column(Date, nullable=False)
    planned_return_date = Column(Date, nullable=False)
    actual_return_date = Column(Date, nullable=True)
    status = Column(String(20), nullable=False, default="lent")  # lent/returned/overdue
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

