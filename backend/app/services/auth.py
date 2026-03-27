"""認証・初期管理者作成サービス。"""
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from app import models
from app.common import security
from app.config import settings
from app.database import get_db
from app.repositories import UserRepository


def ensure_initial_admin(db: Session) -> None:
    """初期管理者が存在しなければ作成する。"""
    repo = UserRepository(db)
    if repo.get_by_email(settings.admin_email):
        return
    admin = models.User(
        email=settings.admin_email,
        password_hash=security.hash_password(settings.admin_password),
        name="Administrator",
        role="admin",
        status="active",
    )
    repo.add(admin)


def authenticate_user(db: Session, email: str, password: str) -> models.User:
    repo = UserRepository(db)
    user = repo.get_by_email(email)
    if not user or not security.verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="認証に失敗しました")
    if user.status != "active":
        raise HTTPException(status_code=403, detail="無効なユーザーです")
    return user


def login(db: Session, email: str, password: str) -> str:
    user = authenticate_user(db, email, password)
    return security.create_access_token(str(user.id))

