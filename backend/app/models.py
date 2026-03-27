"""ORMモデル定義。要件の全エンティティを網羅。"""
import uuid
from datetime import date, datetime

from sqlalchemy import (
    Column,
    String,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class TimestampMixin:
    """作成・更新時刻共通カラム。"""

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(Enum("user", "admin", name="user_role"), nullable=False, default="user")
    status = Column(Enum("active", "inactive", name="user_status"), nullable=False, default="active")
    last_login_at = Column(DateTime)

    reservations = relationship("Reservation", back_populates="user")
    lendings = relationship("Lending", back_populates="lent_by_user", foreign_keys="Lending.lent_by")
    returns = relationship("Return", back_populates="returned_by_user", foreign_keys="Return.returned_by")


class Equipment(Base, TimestampMixin):
    __tablename__ = "equipments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    category = Column(String)
    model = Column(String)
    serial_no = Column(String)
    asset_tag = Column(String, unique=True)
    purchase_date = Column(Date)
    note = Column(String)
    status = Column(Enum("available", "reserved", "loaned", "overdue", "retired", name="equipment_status"), nullable=False, default="available")

    reservations = relationship("Reservation", back_populates="equipment")


class Reservation(Base, TimestampMixin):
    __tablename__ = "reservations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    equipment_id = Column(UUID(as_uuid=True), ForeignKey("equipments.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(Enum("confirmed", "cancelled", "finished", "overdue", name="reservation_status"), nullable=False, default="confirmed")
    cancel_reason = Column(String)

    equipment = relationship("Equipment", back_populates="reservations")
    user = relationship("User", back_populates="reservations")
    lending = relationship("Lending", back_populates="reservation", uselist=False)

    __table_args__ = (
        CheckConstraint("start_date <= end_date", name="ck_reservation_date_range"),
    )


class Lending(Base, TimestampMixin):
    __tablename__ = "lendings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reservation_id = Column(UUID(as_uuid=True), ForeignKey("reservations.id"), nullable=False, unique=True)
    lent_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    lend_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    status = Column(Enum("loaned", "returned", "overdue", name="lending_status"), nullable=False, default="loaned")

    reservation = relationship("Reservation", back_populates="lending")
    lent_by_user = relationship("User", back_populates="lendings", foreign_keys=[lent_by])
    returned = relationship("Return", back_populates="lending", uselist=False)

    __table_args__ = (
        CheckConstraint("lend_date <= due_date", name="ck_lending_date_order"),
    )


class Return(Base, TimestampMixin):
    __tablename__ = "returns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lending_id = Column(UUID(as_uuid=True), ForeignKey("lendings.id"), nullable=False, unique=True)
    returned_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    return_date = Column(Date, nullable=False)
    condition_note = Column(String)

    lending = relationship("Lending", back_populates="returned")
    returned_by_user = relationship("User", back_populates="returns", foreign_keys=[returned_by])


class AuthFailLog(Base):
    __tablename__ = "auth_fail_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    occurred_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ip = Column(String)
