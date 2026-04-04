"""ユーザールーター"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import UserCreate, UserUpdate, UserResponse
from services.user_service import UserService
from utils.auth_guard import AuthGuard

router = APIRouter(prefix="/users", tags=["ユーザー"])


@router.get("", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    _=Depends(AuthGuard.require_admin),
):
    """ユーザー一覧取得（adminのみ）"""
    return UserService.get_all(db)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    body: UserCreate,
    db: Session = Depends(get_db),
    _=Depends(AuthGuard.require_admin),
):
    """ユーザー登録（adminのみ）"""
    return UserService.create(db, body.login_id, body.username, body.password, body.role)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    body: UserUpdate,
    db: Session = Depends(get_db),
    _=Depends(AuthGuard.require_admin),
):
    """ユーザー更新（adminのみ）"""
    return UserService.update(db, user_id, body.username, body.role)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(AuthGuard.require_admin),
):
    """ユーザー削除（adminのみ、自己削除不可）"""
    UserService.delete(db, user_id, current_user.id)
