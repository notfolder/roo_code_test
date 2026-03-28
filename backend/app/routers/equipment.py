"""
備品管理ルーター
備品の一覧取得・登録・編集・削除エンドポイントを提供する
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.models.account import Account
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate, EquipmentResponse
from app.services.equipment_service import EquipmentService

router = APIRouter(prefix="/api/equipment", tags=["備品管理"])


@router.get("/", response_model=list[EquipmentResponse])
def list_equipment(
    available_only: bool = False,
    db: Session = Depends(get_db),
    current_user: Account = Depends(get_current_user),
):
    """
    備品一覧を返す（全ユーザー）
    一般社員はavailable_only=Trueで貸出可能な備品のみを取得する
    管理担当者はavailable_only=Falseで全備品を取得する
    """
    # 一般社員は貸出可能な備品のみ参照可能
    if current_user.role != "admin":
        available_only = True
    return EquipmentService.list_equipment(db, available_only)


@router.post("/", response_model=EquipmentResponse, status_code=201)
def create_equipment(
    data: EquipmentCreate,
    db: Session = Depends(get_db),
    _: Account = Depends(require_admin),
):
    """
    備品を新規登録する（管理担当者のみ）
    """
    return EquipmentService.create_equipment(db, data)


@router.put("/{equipment_id}", response_model=EquipmentResponse)
def update_equipment(
    equipment_id: int,
    data: EquipmentUpdate,
    db: Session = Depends(get_db),
    _: Account = Depends(require_admin),
):
    """
    備品情報を編集する（管理担当者のみ）
    """
    return EquipmentService.update_equipment(db, equipment_id, data)


@router.delete("/{equipment_id}", status_code=204)
def delete_equipment(
    equipment_id: int,
    db: Session = Depends(get_db),
    _: Account = Depends(require_admin),
):
    """
    備品を削除する（管理担当者のみ）
    """
    EquipmentService.delete_equipment(db, equipment_id)
    return None
