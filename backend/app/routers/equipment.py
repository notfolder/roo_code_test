from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user, require_admin
from app.services.equipment import EquipmentService
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate, EquipmentResponse
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[EquipmentResponse])
def list_equipment(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return EquipmentService(db).list_equipment()


@router.post("/", response_model=EquipmentResponse, status_code=201)
def create_equipment(data: EquipmentCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return EquipmentService(db).create_equipment(data)


@router.put("/{equipment_id}", response_model=EquipmentResponse)
def update_equipment(
    equipment_id: int, data: EquipmentUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)
):
    return EquipmentService(db).update_equipment(equipment_id, data)


@router.delete("/{equipment_id}", status_code=204)
def delete_equipment(equipment_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    EquipmentService(db).delete_equipment(equipment_id)
