from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.database import Base


class LendingRecord(Base):
    __tablename__ = "lending_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(String, ForeignKey("items.id"), nullable=False)
    borrower_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lend_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
