from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_admin
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["users"])
user_service = UserService()


@router.get("", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    return user_service.get_users(db)


@router.post("", response_model=UserResponse, status_code=201)
def create_user(
    user_create: UserCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    return user_service.create_user(db, user_create)


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    user_service.delete_user(db, user_id)
