"""ユーザーAPI。"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.database import get_db
from app.services.users import UserService

router = APIRouter()


@router.get("", response_model=list[schemas.UserOut])
def list_users(role: str | None = None, status: str | None = None, db: Session = Depends(get_db), _: schemas.UserOut = Depends(deps.require_admin)):
    return UserService(db).list(role=role, status=status)


@router.post("", response_model=schemas.UserOut)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db), _: schemas.UserOut = Depends(deps.require_admin)):
    return UserService(db).create(payload.email, payload.password, payload.name, payload.role, payload.status)


@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: str, payload: schemas.UserUpdate, db: Session = Depends(get_db), _: schemas.UserOut = Depends(deps.require_admin)):
    return UserService(db).update(user_id, **payload.dict(exclude_unset=True))


@router.put("/{user_id}/disable", response_model=schemas.UserOut)
def disable_user(user_id: str, db: Session = Depends(get_db), _: schemas.UserOut = Depends(deps.require_admin)):
    return UserService(db).disable(user_id)


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: str, db: Session = Depends(get_db), current=Depends(deps.require_admin)):
    return UserService(db).get(user_id)

