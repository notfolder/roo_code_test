"""認証ロジック（パスワード検証・JWT発行）"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from utils.password_util import PasswordUtil
from utils.jwt_util import JWTUtil


class AuthService:
    @staticmethod
    def authenticate(db: Session, login_id: str, password: str) -> dict:
        """ログインIDとパスワードを検証してJWTトークンを返す"""
        user = db.query(User).filter(User.login_id == login_id).first()
        if user is None or not PasswordUtil.verify(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="IDまたはパスワードが正しくありません",
            )
        token = JWTUtil.create_token({"sub": str(user.id), "role": user.role})
        return {"access_token": token, "role": user.role, "username": user.username}
