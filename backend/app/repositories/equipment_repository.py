"""
備品リポジトリ
equipmentテーブルに対するDB操作を集約する
"""
from sqlalchemy.orm import Session

from app.models.equipment import Equipment
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate


class EquipmentRepository:
    """備品テーブルのCRUD操作を提供するリポジトリ"""

    @staticmethod
    def find_all(db: Session) -> list[Equipment]:
        """
        全備品を管理番号の昇順で取得する
        """
        return db.query(Equipment).order_by(Equipment.management_number.asc()).all()

    @staticmethod
    def find_available(db: Session) -> list[Equipment]:
        """
        貸出可能（status='available'）な備品のみを管理番号の昇順で取得する
        """
        return (
            db.query(Equipment)
            .filter(Equipment.status == "available")
            .order_by(Equipment.management_number.asc())
            .all()
        )

    @staticmethod
    def find_by_id(db: Session, equipment_id: int) -> Equipment | None:
        """
        IDで備品を取得する
        存在しない場合はNoneを返す
        """
        return db.query(Equipment).filter(Equipment.id == equipment_id).first()

    @staticmethod
    def find_by_id_for_update(db: Session, equipment_id: int) -> Equipment | None:
        """
        IDで備品を悲観的ロック（FOR UPDATE）付きで取得する
        貸出操作時の二重貸出防止に使用する
        存在しない場合はNoneを返す
        """
        return (
            db.query(Equipment)
            .filter(Equipment.id == equipment_id)
            .with_for_update()
            .first()
        )

    @staticmethod
    def find_by_management_number(db: Session, management_number: str) -> Equipment | None:
        """
        管理番号で備品を取得する
        重複チェックに使用する
        """
        return (
            db.query(Equipment)
            .filter(Equipment.management_number == management_number)
            .first()
        )

    @staticmethod
    def create(db: Session, data: EquipmentCreate) -> Equipment:
        """
        新規備品を作成してDBに保存する
        初期状態は「貸出可能（available）」に設定する
        """
        equipment = Equipment(
            management_number=data.management_number,
            name=data.name,
            note=data.note,
            status="available",
        )
        db.add(equipment)
        db.flush()
        db.refresh(equipment)
        return equipment

    @staticmethod
    def update(db: Session, equipment: Equipment, data: EquipmentUpdate) -> Equipment:
        """
        備品情報を更新する
        貸出状態（status）は変更しない
        """
        equipment.management_number = data.management_number
        equipment.name = data.name
        equipment.note = data.note
        db.flush()
        db.refresh(equipment)
        return equipment

    @staticmethod
    def update_status(db: Session, equipment: Equipment, status: str) -> Equipment:
        """
        備品の貸出状態（status）を更新する
        貸出時は'borrowed'、返却時は'available'を指定する
        """
        equipment.status = status
        db.flush()
        return equipment

    @staticmethod
    def delete(db: Session, equipment: Equipment) -> None:
        """
        指定された備品を削除する
        貸出記録から参照されている場合はFKエラーが発生する
        """
        db.delete(equipment)
        db.flush()
