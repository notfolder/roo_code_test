"""共通依存関係（認証/認可）。"""
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.common import security
from app.database import get_db
from app.repositories import UserRepository


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials is None:
        raise HTTPException(status_code=401, detail="認証が必要です")
    token = credentials.credentials
    user_id = security.decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="トークンが不正です")
    user = UserRepository(db).get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="ユーザーが存在しません")
    if user.status != "active":
        raise HTTPException(status_code=403, detail="無効なユーザーです")
    return user


def require_admin(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="権限がありません")
    return current_user

