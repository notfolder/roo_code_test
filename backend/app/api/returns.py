"""返却API。"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.database import get_db
from app.services.returns import ReturnService

router = APIRouter()


@router.get("", response_model=list[schemas.ReturnOut])
def list_returns(db: Session = Depends(get_db), _: schemas.UserOut = Depends(deps.require_admin)):
    return ReturnService(db).list()


@router.post("", response_model=schemas.ReturnOut)
def create_return(payload: schemas.ReturnCreate, db: Session = Depends(get_db), current=Depends(deps.require_admin)):
    return ReturnService(db).create(lending_id=payload.lending_id, returned_by=str(current.id), return_date=payload.return_date, condition_note=payload.condition_note)


@router.get("/{return_id}", response_model=schemas.ReturnOut)
def get_return(return_id: str, db: Session = Depends(get_db), _: schemas.UserOut = Depends(deps.require_admin)):
    return ReturnService(db).get(return_id)

