"""簡易リポジトリ実装（SQLAlchemy）。"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app import models


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[models.User]:
        return self.db.query(models.User).filter(models.User.email == email).first()

    def get(self, user_id: str) -> Optional[models.User]:
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    def list(self, role: Optional[str] = None, status: Optional[str] = None) -> List[models.User]:
        q = self.db.query(models.User)
        if role:
            q = q.filter(models.User.role == role)
        if status:
            q = q.filter(models.User.status == status)
        return q.all()

    def add(self, user: models.User) -> models.User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: models.User) -> models.User:
        self.db.commit()
        self.db.refresh(user)
        return user


class EquipmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, equipment_id: str) -> Optional[models.Equipment]:
        return self.db.query(models.Equipment).filter(models.Equipment.id == equipment_id).first()

    def list(self, name: Optional[str] = None, status: Optional[str] = None) -> List[models.Equipment]:
        q = self.db.query(models.Equipment)
        if name:
            q = q.filter(models.Equipment.name.ilike(f"%{name}%"))
        if status:
            q = q.filter(models.Equipment.status == status)
        return q.all()

    def add(self, equipment: models.Equipment) -> models.Equipment:
        self.db.add(equipment)
        self.db.commit()
        self.db.refresh(equipment)
        return equipment

    def update(self, equipment: models.Equipment) -> models.Equipment:
        self.db.commit()
        self.db.refresh(equipment)
        return equipment


class ReservationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, reservation_id: str) -> Optional[models.Reservation]:
        return self.db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()

    def list(self, user_id: Optional[str] = None) -> List[models.Reservation]:
        q = self.db.query(models.Reservation)
        if user_id:
            q = q.filter(models.Reservation.user_id == user_id)
        return q.all()

    def add(self, reservation: models.Reservation) -> models.Reservation:
        self.db.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def update(self, reservation: models.Reservation) -> models.Reservation:
        self.db.commit()
        self.db.refresh(reservation)
        return reservation


class LendingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, lending_id: str) -> Optional[models.Lending]:
        return self.db.query(models.Lending).filter(models.Lending.id == lending_id).first()

    def get_by_reservation(self, reservation_id: str) -> Optional[models.Lending]:
        return self.db.query(models.Lending).filter(models.Lending.reservation_id == reservation_id).first()

    def list(self) -> List[models.Lending]:
        return self.db.query(models.Lending).all()

    def add(self, lending: models.Lending) -> models.Lending:
        self.db.add(lending)
        self.db.commit()
        self.db.refresh(lending)
        return lending

    def update(self, lending: models.Lending) -> models.Lending:
        self.db.commit()
        self.db.refresh(lending)
        return lending


class ReturnRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, return_id: str) -> Optional[models.Return]:
        return self.db.query(models.Return).filter(models.Return.id == return_id).first()

    def get_by_lending(self, lending_id: str) -> Optional[models.Return]:
        return self.db.query(models.Return).filter(models.Return.lending_id == lending_id).first()

    def list(self) -> List[models.Return]:
        return self.db.query(models.Return).all()

    def add(self, ret: models.Return) -> models.Return:
        self.db.add(ret)
        self.db.commit()
        self.db.refresh(ret)
        return ret

