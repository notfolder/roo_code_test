from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User
from app.security import verify_password


class AuthService:
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User | None:
        user = db.scalar(
            select(User).where(User.email == email, User.status == "active")
        )
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
