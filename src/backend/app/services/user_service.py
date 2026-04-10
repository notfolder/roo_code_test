from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import OperationLog, User
from app.schemas.user import UserCreate, UserUpdate
from app.security import hash_password


class UserService:
    @staticmethod
    def list_users(db: Session) -> list[User]:
        return list(db.scalars(select(User).order_by(User.created_at.asc())).all())

    @staticmethod
    def get_user(db: Session, user_id: str) -> User:
        user = db.scalar(select(User).where(User.id == user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    @staticmethod
    def create_user(db: Session, payload: UserCreate) -> User:
        user = User(
            email=payload.email,
            hashed_password=hash_password(payload.password),
            name=payload.name,
            role=payload.role,
            status="active",
        )
        db.add(user)
        try:
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError as exc:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
            ) from exc

    @staticmethod
    def update_user(db: Session, user_id: str, payload: UserUpdate) -> User:
        user = UserService.get_user(db, user_id)
        user.email = str(payload.email)
        user.name = payload.name
        user.role = payload.role
        try:
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError as exc:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
            ) from exc

    @staticmethod
    def delete_user(db: Session, user_id: str, actor_id: str) -> dict:
        user = UserService.get_user(db, user_id)
        user.status = "deleted"
        db.add(
            OperationLog(
                action="user_delete", actor_user_id=actor_id, target_user_id=user_id
            )
        )
        db.commit()
        return {"status": "deleted"}
