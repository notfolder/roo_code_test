"""
認証ルーター
ログイン・ログアウトエンドポイントを提供する
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["認証"])


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    アカウント名とパスワードで認証し、JWTトークンを返す
    """
    return AuthService.login(db, request.account_name, request.password)


@router.post("/logout", status_code=204)
def logout():
    """
    ログアウト（フロントエンド側でトークンを削除するため、サーバー側は何もしない）
    """
    return None
