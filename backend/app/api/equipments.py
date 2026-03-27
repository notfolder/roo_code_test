"""備品API。"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.database import get_db
from app.services.equipments import EquipmentService

router = APIRouter()


@router.get("", response_model=list[schemas.EquipmentOut])
def list_equipments(name: str | None = None, status: str | None = None, db: Session = Depends(get_db), _: schemas.UserOut = Depends(deps.get_current_user)):
    return EquipmentService(db).list(name=name, status=status)


@router.post("", response_model=schemas.EquipmentOut)
def create_equipment(payload: schemas.EquipmentCreate, db: Session = Depends(get_db), _: schemas.UserOut = Depends(deps.require_admin)):
    return EquipmentService(db).create(**payload.dict())


@router.put("/{equipment_id}", response_model=schemas.EquipmentOut)
def update_equipment(equipment_id: str, payload: schemas.EquipmentUpdate, db: Session = Depends(get_db), _: schemas.UserOut = Depends(deps.require_admin)):
    return EquipmentService(db).update(equipment_id, **payload.dict(exclude_unset=True))


@router.put("/{equipment_id}/retire", response_model=schemas.EquipmentOut)
def retire_equipment(equipment_id: str, db: Session = Depends(get_db), _: schemas.UserOut = Depends(deps.require_admin)):
    return EquipmentService(db).retire(equipment_id)


@router.get("/{equipment_id}", response_model=schemas.EquipmentOut)
def get_equipment(equipment_id: str, db: Session = Depends(get_db), _: schemas.UserOut = Depends(deps.get_current_user)):
    return EquipmentService(db).get(equipment_id)

