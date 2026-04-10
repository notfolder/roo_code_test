from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.lending_record import LendingRecord
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService

auth_service = AuthService()


class UserService:
    def get_users(self, db: Session) -> List[UserResponse]:
        users = db.query(User).all()
        return [UserResponse(id=u.id, login_id=u.login_id, role=u.role) for u in users]

    def create_user(self, db: Session, user_create: UserCreate) -> UserResponse:
        if db.query(User).filter(User.login_id == user_create.login_id).first():
            raise HTTPException(status_code=409, detail="このログインIDは既に使用されています")
        user = User(
            login_id=user_create.login_id,
            password_hash=auth_service.hash_password(user_create.password),
            role=user_create.role,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return UserResponse(id=user.id, login_id=user.login_id, role=user.role)

    def delete_user(self, db: Session, user_id: int) -> None:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="指定されたリソースが見つかりません")
        if user.role == "admin":
            admin_count = db.query(User).filter(User.role == "admin").count()
            if admin_count <= 1:
                raise HTTPException(status_code=409, detail="最後の管理者アカウントは削除できません")
        active_lending = (
            db.query(LendingRecord)
            .filter(
                LendingRecord.borrower_user_id == user_id,
                LendingRecord.return_date.is_(None),
            )
            .first()
        )
        if active_lending:
            raise HTTPException(status_code=409, detail="貸出中の借用者のアカウントは削除できません")
        db.delete(user)
        db.commit()

    def get_user_by_login_id(self, db: Session, login_id: str):
        return db.query(User).filter(User.login_id == login_id).first()
