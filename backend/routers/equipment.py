from fastapi import APIRouter, Depends
from fastapi.responses import Response

from common.auth import get_current_admin
from models.equipment import EquipmentCreate, EquipmentResponse, EquipmentUpdate
from services.equipment_service import EquipmentService

router = APIRouter(prefix="/api/equipment", tags=["備品管理"])

_equipment_service = EquipmentService()


@router.get("", response_model=list[EquipmentResponse])
def get_equipment_list():
    """備品一覧を取得する（認証不要）"""
    return _equipment_service.get_all()


@router.post("", response_model=EquipmentResponse, status_code=201)
def create_equipment(data: EquipmentCreate, _: dict = Depends(get_current_admin)):
    """備品を登録する（認証必要）"""
    return _equipment_service.create(data.model_dump())


@router.put("/{equipment_id}", response_model=EquipmentResponse)
def update_equipment(
    equipment_id: int, data: EquipmentUpdate, _: dict = Depends(get_current_admin)
):
    """備品を更新する（認証必要）"""
    return _equipment_service.update(equipment_id, data.model_dump())


@router.delete("/{equipment_id}", status_code=204)
def delete_equipment(equipment_id: int, _: dict = Depends(get_current_admin)):
    """備品を削除する（認証必要）"""
    _equipment_service.delete(equipment_id)
    return Response(status_code=204)
