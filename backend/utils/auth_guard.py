"""FastAPI依存性注入による認証・認可（共通処理）"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from utils.jwt_util import JWTUtil

bearer_scheme = HTTPBearer()


class AuthGuard:
    @staticmethod
    def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        db: Session = Depends(get_db),
    ):
        """JWTトークンを検証してログインユーザーを返す"""
        payload = JWTUtil.decode_token(credentials.credentials)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="無効なトークンです")

        from models.user import User
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="ユーザーが見つかりません")
        return user

    @staticmethod
    def require_admin(current_user=Depends(get_current_user)):
        """adminロールのみ許可する。staffの場合は403を返す"""
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="この操作は許可されていません",
            )
        return current_user
