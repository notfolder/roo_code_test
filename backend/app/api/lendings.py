"""貸出API。"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.database import get_db
from app.services.lendings import LendingService

router = APIRouter()


@router.get("", response_model=list[schemas.LendingOut])
def list_lendings(db: Session = Depends(get_db), _: schemas.UserOut = Depends(deps.require_admin)):
    return LendingService(db).list()


@router.post("", response_model=schemas.LendingOut)
def create_lending(payload: schemas.LendingCreate, db: Session = Depends(get_db), current=Depends(deps.require_admin)):
    return LendingService(db).create(reservation_id=payload.reservation_id, lent_by=str(current.id), lend_date=payload.lend_date)


@router.get("/{lending_id}", response_model=schemas.LendingOut)
def get_lending(lending_id: str, db: Session = Depends(get_db), _: schemas.UserOut = Depends(deps.require_admin)):
    return LendingService(db).get(lending_id)

