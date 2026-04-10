import os
from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.environ.get("SECRET_KEY", "")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 8


class AuthService:
    def authenticate_user(self, db: Session, login_id: str, password: str):
        user = db.query(User).filter(User.login_id == login_id).first()
        if not user:
            return None
        if not pwd_context.verify(password, user.password_hash):
            return None
        return user

    def create_access_token(self, user_id: int, role: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        payload = {"sub": str(user_id), "role": role, "exp": expire}
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def verify_token(self, token: str) -> dict:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
