import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, SessionLocal, Base
import app.models  # noqa: F401 - テーブル作成のためモデルをインポート
from app.routers import auth, items, lending_records, users
from app.services.auth_service import AuthService
from app.services.user_service import UserService

Base.metadata.create_all(bind=engine)

app = FastAPI(title="備品・貸出管理システム API", docs_url="/api/docs", openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(items.router)
app.include_router(lending_records.router)
app.include_router(users.router)


@app.on_event("startup")
def create_initial_admin():
    login_id = os.environ.get("INITIAL_ADMIN_LOGIN_ID")
    password = os.environ.get("INITIAL_ADMIN_PASSWORD")
    if not login_id or not password:
        return
    db = SessionLocal()
    try:
        user_service = UserService()
        from app.models.user import User
        if not db.query(User).filter(User.login_id == login_id).first():
            auth_service = AuthService()
            from app.models.user import User as UserModel
            user = UserModel(
                login_id=login_id,
                password_hash=auth_service.hash_password(password),
                role="admin",
            )
            db.add(user)
            db.commit()
    finally:
        db.close()
