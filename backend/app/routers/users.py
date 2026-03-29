from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db, require_admin
from app.services.user import UserService
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return UserService(db).list_users()


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return UserService(db).create_user(data)


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    UserService(db).delete_user(user_id)
