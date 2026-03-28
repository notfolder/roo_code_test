"""
備品サービス
備品管理の業務ロジックを担う
"""
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.equipment_repository import EquipmentRepository
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate, EquipmentResponse


class EquipmentService:
    """備品業務ロジックを提供するサービス"""

    @staticmethod
    def list_equipment(db: Session, available_only: bool = False) -> list[EquipmentResponse]:
        """
        備品一覧を返す
        available_only=Trueの場合は貸出可能な備品のみを返す（一般社員向け）
        """
        if available_only:
            items = EquipmentRepository.find_available(db)
        else:
            items = EquipmentRepository.find_all(db)
        return [EquipmentResponse.model_validate(e) for e in items]

    @staticmethod
    def create_equipment(db: Session, data: EquipmentCreate) -> EquipmentResponse:
        """
        新規備品を登録する
        管理番号が既に存在する場合は409エラーを送出する
        """
        existing = EquipmentRepository.find_by_management_number(db, data.management_number)
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"管理番号「{data.management_number}」は既に存在します",
            )
        equipment = EquipmentRepository.create(db, data)
        db.commit()
        return EquipmentResponse.model_validate(equipment)

    @staticmethod
    def update_equipment(db: Session, equipment_id: int, data: EquipmentUpdate) -> EquipmentResponse:
        """
        備品情報を更新する
        対象備品が存在しない場合は404エラーを送出する
        管理番号が他の備品と重複する場合は409エラーを送出する
        """
        equipment = EquipmentRepository.find_by_id(db, equipment_id)
        if equipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定された備品が見つかりません",
            )
        # 管理番号の重複チェック（自分自身は除く）
        existing = EquipmentRepository.find_by_management_number(db, data.management_number)
        if existing is not None and existing.id != equipment_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"管理番号「{data.management_number}」は既に存在します",
            )
        updated = EquipmentRepository.update(db, equipment, data)
        db.commit()
        return EquipmentResponse.model_validate(updated)

    @staticmethod
    def delete_equipment(db: Session, equipment_id: int) -> None:
        """
        備品を削除する
        対象備品が存在しない場合は404エラーを送出する
        貸出中の備品は409エラーを送出する
        貸出記録から参照されている備品はFKエラーとなり409エラーを送出する
        """
        equipment = EquipmentRepository.find_by_id(db, equipment_id)
        if equipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定された備品が見つかりません",
            )
        if equipment.status == "borrowed":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="貸出中の備品は削除できません",
            )
        try:
            EquipmentRepository.delete(db, equipment)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="貸出記録が存在する備品は削除できません",
            )
