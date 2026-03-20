"""備品モデル定義。"""

import uuid
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from backend.app.core.database import Base


class Item(Base):
    """備品を表すエンティティ。"""

    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    status = Column(String(20), nullable=False, default="active")  # active/retired
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

