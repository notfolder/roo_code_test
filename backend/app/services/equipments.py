"""備品管理サービス。"""
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models
from app.repositories import EquipmentRepository


class EquipmentService:
    def __init__(self, db: Session):
        self.repo = EquipmentRepository(db)

    def create(self, **kwargs) -> models.Equipment:
        equipment = models.Equipment(**kwargs)
        return self.repo.add(equipment)

    def update(self, equipment_id: str, **kwargs) -> models.Equipment:
        equipment = self.repo.get(equipment_id)
        if not equipment:
            raise HTTPException(status_code=404, detail="備品が存在しません")
        for key, value in kwargs.items():
            if value is not None:
                setattr(equipment, key, value)
        return self.repo.update(equipment)

    def retire(self, equipment_id: str) -> models.Equipment:
        return self.update(equipment_id, status="retired")

    def list(self, name: str | None = None, status: str | None = None):
        return self.repo.list(name=name, status=status)

    def get(self, equipment_id: str) -> models.Equipment:
        equipment = self.repo.get(equipment_id)
        if not equipment:
            raise HTTPException(status_code=404, detail="備品が存在しません")
        return equipment

