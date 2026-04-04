"""equipmentsテーブルのDB操作"""
from sqlalchemy.orm import Session
from models.equipment import Equipment


class EquipmentRepository:
    @staticmethod
    def find_all(db: Session) -> list[Equipment]:
        """全備品を取得する"""
        return db.query(Equipment).order_by(Equipment.code).all()

    @staticmethod
    def find_by_id(db: Session, equipment_id: int) -> Equipment | None:
        """IDで備品を取得する"""
        return db.query(Equipment).filter(Equipment.id == equipment_id).first()

    @staticmethod
    def find_by_id_for_update(db: Session, equipment_id: int) -> Equipment | None:
        """IDで備品を取得する（悲観的ロック：SELECT FOR UPDATE）"""
        return db.query(Equipment).filter(Equipment.id == equipment_id).with_for_update().first()

    @staticmethod
    def find_by_code(db: Session, code: str) -> Equipment | None:
        """管理番号で備品を取得する"""
        return db.query(Equipment).filter(Equipment.code == code).first()

    @staticmethod
    def save(db: Session, equipment: Equipment) -> Equipment:
        """備品を保存（新規・更新）する"""
        db.add(equipment)
        db.commit()
        db.refresh(equipment)
        return equipment

    @staticmethod
    def delete(db: Session, equipment: Equipment) -> None:
        """備品を削除する"""
        db.delete(equipment)
        db.commit()
