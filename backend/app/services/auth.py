from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.user import UserRepository
from app.dependencies import verify_password, hash_password, create_access_token
from app.models.user import User


class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def login(self, login_id: str, password: str) -> Optional[dict]:
        user = self.repo.get_by_login_id(login_id)
        if not user or not user.is_active:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        token = create_access_token({"sub": str(user.id)})
        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": user.id,
            "name": user.name,
            "role": user.role,
        }
