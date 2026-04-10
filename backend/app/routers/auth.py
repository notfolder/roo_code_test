from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])
auth_service = AuthService()


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, request.login_id, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="IDまたはパスワードが正しくありません")
    access_token = auth_service.create_access_token(user.id, user.role)
    return TokenResponse(access_token=access_token)
