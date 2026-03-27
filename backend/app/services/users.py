"""ユーザー管理サービス。"""
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models
from app.common import security
from app.repositories import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def create(self, email: str, password: str, name: str, role: str, status: str) -> models.User:
        if self.repo.get_by_email(email):
            raise HTTPException(status_code=409, detail="emailが重複しています")
        user = models.User(
            email=email,
            password_hash=security.hash_password(password),
            name=name,
            role=role,
            status=status,
        )
        return self.repo.add(user)

    def update(self, user_id: str, **kwargs) -> models.User:
        user = self.repo.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="ユーザーが存在しません")
        if "password" in kwargs and kwargs["password"]:
            user.password_hash = security.hash_password(kwargs["password"])
        for key in ["name", "role", "status"]:
            if key in kwargs and kwargs[key] is not None:
                setattr(user, key, kwargs[key])
        return self.repo.update(user)

    def disable(self, user_id: str) -> models.User:
        return self.update(user_id, status="inactive")

    def list(self, role: str | None = None, status: str | None = None):
        return self.repo.list(role=role, status=status)

    def get(self, user_id: str) -> models.User:
        user = self.repo.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="ユーザーが存在しません")
        return user

