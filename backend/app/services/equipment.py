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
        if self.db.query(Equipment).filter(Equipment.management_number == data.management_number).first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="管理番号が既に使用されています",
            )
        eq = Equipment(
            management_number=data.management_number,
            name=data.name,
            status="available",
        )
        result = self.repo.add(eq)
        self.db.commit()
        return result

    def update_equipment(self, equipment_id: int, data: EquipmentUpdate) -> Equipment:
        eq = self.get_equipment(equipment_id)
        eq.name = data.name
        self.db.commit()
        self.db.refresh(eq)
        return eq

    def delete_equipment(self, equipment_id: int) -> None:
        eq = self.get_equipment(equipment_id)
        if eq.status != "available":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="貸出中の備品は削除できません",
            )
        self.repo.delete(eq)
        self.db.commit()
