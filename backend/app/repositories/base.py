from typing import List, Optional, Type, TypeVar
from sqlalchemy.orm import Session
from app.database import Base

T = TypeVar("T", bound=Base)


class BaseRepository:
    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def get(self, id: int) -> Optional[T]:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def list(self) -> List[T]:
        return self.db.query(self.model).all()

    def add(self, obj: T) -> T:
        self.db.add(obj)
        self.db.flush()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: T) -> None:
        self.db.delete(obj)
        self.db.flush()
