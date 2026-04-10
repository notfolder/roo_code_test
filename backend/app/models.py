import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship

from .db import Base


class Role(str, enum.Enum):
    employee = "employee"
    admin = "admin"


class Status(str, enum.Enum):
    active = "active"
    deleted = "deleted"


class ItemState(str, enum.Enum):
    available = "available"
    lent = "lent"


class User(Base):
    __tablename__ = "users"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False, default=Role.employee)
    status = Column(Enum(Status), nullable=False, default=Status.active)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    loan_records = relationship("LoanRecord", back_populates="user")


class Item(Base):
    __tablename__ = "items"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_number = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    state = Column(Enum(ItemState), nullable=False, default=ItemState.available)
    current_user_id = Column(
        PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    current_user = relationship(
        "User", backref="current_items", foreign_keys=[current_user_id]
    )
    loan_record = relationship("LoanRecord", back_populates="item", uselist=False)


class LoanRecord(Base):
    __tablename__ = "loan_records"
    __table_args__ = (UniqueConstraint("item_id", name="uq_loan_item"),)

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_id = Column(PG_UUID(as_uuid=True), ForeignKey("items.id"), nullable=False)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    lent_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    returned_at = Column(DateTime, nullable=True)

    item = relationship("Item", back_populates="loan_record")
    user = relationship("User", back_populates="loan_records")


class OperationLog(Base):
    __tablename__ = "operation_logs"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    operation = Column(String, nullable=False)
    details = Column(String, nullable=True)
