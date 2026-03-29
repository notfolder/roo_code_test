from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.user import UserRepository
from app.dependencies import hash_password
from app.models.user import User
from app.schemas.user import UserCreate


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
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="ログインIDが既に使用されています")
        user = User(
            login_id=data.login_id,
            name=data.name,
            hashed_password=hash_password(data.password),
            role=data.role,
        )
        result = self.repo.add(user)
        self.db.commit()
        return result

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        if self.repo.has_active_loans(user_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="貸出中の利用者は削除できません",
            )
        self.repo.delete(user)
        self.db.commit()
