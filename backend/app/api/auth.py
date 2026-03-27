"""認証API。"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.services import auth as auth_service

router = APIRouter()


@router.post("/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    """ログインしJWTを発行。"""
    token = auth_service.login(db, payload.email, payload.password)
    user = auth_service.authenticate_user(db, payload.email, payload.password)
    return {"token": token, "user": user}
