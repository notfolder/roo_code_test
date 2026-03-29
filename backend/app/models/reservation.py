from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, func
from app.database import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    planned_start_date = Column(Date, nullable=False)
    planned_return_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False, default="pending")  # pending / cancelled / loaned
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
