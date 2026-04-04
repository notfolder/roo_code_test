"""備品のCRUD・貸出・返却ビジネスロジック"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.equipment import Equipment
from repositories.equipment_repository import EquipmentRepository


class EquipmentService:
    @staticmethod
    def get_all(db: Session) -> list[Equipment]:
        """全備品一覧を返す"""
        return EquipmentRepository.find_all(db)

    @staticmethod
    def create(db: Session, code: str, name: str) -> Equipment:
        """備品を新規登録する。管理番号重複時は409を返す"""
        if not code.strip() or not name.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="入力してください")
        if EquipmentRepository.find_by_code(db, code):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="この管理番号は既に登録されています")
        equipment = Equipment(code=code.strip(), name=name.strip())
        return EquipmentRepository.save(db, equipment)

    @staticmethod
    def update(db: Session, equipment_id: int, name: str) -> Equipment:
        """備品名を更新する"""
        if not name.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="入力してください")
        equipment = EquipmentRepository.find_by_id(db, equipment_id)
        if equipment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="対象データが見つかりません")
        equipment.name = name.strip()
        return EquipmentRepository.save(db, equipment)

    @staticmethod
    def delete(db: Session, equipment_id: int) -> None:
        """備品を削除する。貸出中の場合は409を返す"""
        equipment = EquipmentRepository.find_by_id(db, equipment_id)
        if equipment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="対象データが見つかりません")
        if equipment.status == "lending":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="貸出中の備品は削除できません")
        EquipmentRepository.delete(db, equipment)

    @staticmethod
    def lend(db: Session, equipment_id: int, borrower_name: str) -> Equipment:
        """貸出登録する。既に貸出中の場合は409を返す（悲観的ロック使用）"""
        if not borrower_name.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="入力してください")
        equipment = EquipmentRepository.find_by_id_for_update(db, equipment_id)
        if equipment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="対象データが見つかりません")
        if equipment.status == "lending":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="この備品は既に貸出中です")
        equipment.status = "lending"
        equipment.borrower_name = borrower_name.strip()
        return EquipmentRepository.save(db, equipment)

    @staticmethod
    def return_equipment(db: Session, equipment_id: int) -> Equipment:
        """返却登録する。在庫ありの場合は409を返す（悲観的ロック使用）"""
        equipment = EquipmentRepository.find_by_id_for_update(db, equipment_id)
        if equipment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="対象データが見つかりません")
        if equipment.status == "available":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="この備品は貸出中ではありません")
        equipment.status = "available"
        equipment.borrower_name = None
        return EquipmentRepository.save(db, equipment)
