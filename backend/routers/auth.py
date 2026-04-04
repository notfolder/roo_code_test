"""認証ルーター"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import LoginRequest, LoginResponse
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["認証"])


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """ログイン：JWTトークンを発行する"""
    return AuthService.authenticate(db, request.login_id, request.password)


@router.post("/logout")
def logout():
    """ログアウト：クライアント側でトークンを破棄するため、サーバー側は何もしない"""
    return {"message": "ログアウトしました"}
