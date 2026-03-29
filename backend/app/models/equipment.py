from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    management_number = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False, default="available")  # available / loaned
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
