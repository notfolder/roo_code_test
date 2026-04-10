from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies import require_admin
from app.models import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService


router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
def list_users(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    return UserService.list_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: str, _: User = Depends(require_admin), db: Session = Depends(get_db)
):
    return UserService.get_user(db, user_id)


@router.post("", response_model=UserResponse)
def create_user(
    payload: UserCreate, _: User = Depends(require_admin), db: Session = Depends(get_db)
):
    return UserService.create_user(db, payload)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str,
    payload: UserUpdate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return UserService.update_user(db, user_id, payload)


@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return UserService.delete_user(db, user_id, actor_id=current_user.id)
