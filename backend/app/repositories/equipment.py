from sqlalchemy.orm import Session
from app.models.equipment import Equipment
from app.repositories.base import BaseRepository


class EquipmentRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(Equipment, db)

    def get_for_update(self, equipment_id: int):
        return (
            self.db.query(Equipment)
            .filter(Equipment.id == equipment_id)
            .with_for_update()
            .first()
        )
