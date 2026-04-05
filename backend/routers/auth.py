from fastapi import APIRouter
from fastapi.responses import JSONResponse

from models.admin_user import LoginRequest, TokenResponse
from services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["認証"])

_auth_service = AuthService()


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    """ログインしてJWTトークンを発行する"""
    token = _auth_service.login(request.login_id, request.password)
    return TokenResponse(access_token=token)


@router.post("/logout")
def logout():
    """ログアウト（クライアント側でトークンを破棄する）"""
    return JSONResponse(content={"message": "ログアウトしました"})
