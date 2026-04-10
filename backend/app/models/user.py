from sqlalchemy import Column, Integer, String, CheckConstraint
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    login_id = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    role = Column(
        String,
        CheckConstraint("role IN ('admin', 'user')"),
        nullable=False,
    )
