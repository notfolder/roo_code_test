from sqlalchemy import Column, Integer, String
from app.database import Base


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default="available")  # available / on_loan
    notes = Column(String(500), nullable=True)
