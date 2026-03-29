from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.equipment import EquipmentRepository
from app.models.equipment import Equipment
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate


class EquipmentService:
    def __init__(self, db: Session):
        self.repo = EquipmentRepository(db)
        self.db = db

    def list_equipment(self) -> List[Equipment]:
        return self.repo.list()

    def get_equipment(self, equipment_id: int) -> Equipment:
        eq = self.repo.get(equipment_id)
        if not eq:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found")
        return eq

    def create_equipment(self, data: EquipmentCreate) -> Equipment:
        eq = Equipment(
            name=data.name,
            category=data.category,
            notes=data.notes,
            status="available",
        )
        result = self.repo.add(eq)
        self.db.commit()
        return result

    def update_equipment(self, equipment_id: int, data: EquipmentUpdate) -> Equipment:
        eq = self.get_equipment(equipment_id)
        if data.name is not None:
            eq.name = data.name
        if data.category is not None:
            eq.category = data.category
        if data.notes is not None:
            eq.notes = data.notes
        self.db.commit()
        self.db.refresh(eq)
        return eq

    def delete_equipment(self, equipment_id: int) -> None:
        eq = self.get_equipment(equipment_id)
        if eq.status != "available":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete equipment that is on loan",
            )
        self.repo.delete(eq)
        self.db.commit()
