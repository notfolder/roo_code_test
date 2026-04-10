from sqlalchemy import Column, String, CheckConstraint
from app.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(
        String,
        CheckConstraint("status IN ('available', 'lending')"),
        nullable=False,
        default="available",
    )
