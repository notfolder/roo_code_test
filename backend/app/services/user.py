from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.user import UserRepository
from app.dependencies import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)
        self.db = db

    def list_users(self) -> List[User]:
        return self.repo.list()

    def get_user(self, user_id: int) -> User:
        user = self.repo.get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    def create_user(self, data: UserCreate) -> User:
        if self.repo.get_by_login_id(data.login_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="login_id already exists")
        user = User(
            login_id=data.login_id,
            name=data.name,
            hashed_password=hash_password(data.password),
            role=data.role,
            is_active=True,
        )
        result = self.repo.add(user)
        self.db.commit()
        return result

    def update_user(self, user_id: int, data: UserUpdate) -> User:
        user = self.get_user(user_id)
        if data.name is not None:
            user.name = data.name
        if data.password is not None:
            user.hashed_password = hash_password(data.password)
        if data.role is not None:
            user.role = data.role
        if data.is_active is not None:
            user.is_active = data.is_active
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        if self.repo.has_active_loans(user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete user with active loans",
            )
        self.repo.delete(user)
        self.db.commit()
