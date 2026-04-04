"""備品ルーター"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.equipment import EquipmentCreate, EquipmentUpdate, LendRequest, EquipmentResponse
from services.equipment_service import EquipmentService
from utils.auth_guard import AuthGuard

router = APIRouter(prefix="/equipments", tags=["備品"])


@router.get("", response_model=list[EquipmentResponse])
def list_equipments(
    db: Session = Depends(get_db),
    _=Depends(AuthGuard.get_current_user),
):
    """備品一覧取得（ログイン済みユーザー全員）"""
    return EquipmentService.get_all(db)


@router.post("", response_model=EquipmentResponse, status_code=status.HTTP_201_CREATED)
def create_equipment(
    body: EquipmentCreate,
    db: Session = Depends(get_db),
    _=Depends(AuthGuard.require_admin),
):
    """備品登録（adminのみ）"""
    return EquipmentService.create(db, body.code, body.name)


@router.put("/{equipment_id}", response_model=EquipmentResponse)
def update_equipment(
    equipment_id: int,
    body: EquipmentUpdate,
    db: Session = Depends(get_db),
    _=Depends(AuthGuard.require_admin),
):
    """備品名更新（adminのみ）"""
    return EquipmentService.update(db, equipment_id, body.name)


@router.delete("/{equipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_equipment(
    equipment_id: int,
    db: Session = Depends(get_db),
    _=Depends(AuthGuard.require_admin),
):
    """備品削除（adminのみ）"""
    EquipmentService.delete(db, equipment_id)


@router.post("/{equipment_id}/lend", response_model=EquipmentResponse)
def lend_equipment(
    equipment_id: int,
    body: LendRequest,
    db: Session = Depends(get_db),
    _=Depends(AuthGuard.require_admin),
):
    """貸出登録（adminのみ）"""
    return EquipmentService.lend(db, equipment_id, body.borrower_name)


@router.post("/{equipment_id}/return", response_model=EquipmentResponse)
def return_equipment(
    equipment_id: int,
    db: Session = Depends(get_db),
    _=Depends(AuthGuard.require_admin),
):
    """返却登録（adminのみ）"""
    return EquipmentService.return_equipment(db, equipment_id)
