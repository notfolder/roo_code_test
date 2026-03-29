from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.database import Base


class LoanRecord(Base):
    __tablename__ = "loan_records"

    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    loan_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    status = Column(String(20), nullable=False, default="active")  # active / returned
    purpose = Column(String(200), nullable=True)
