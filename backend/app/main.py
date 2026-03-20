"""FastAPI エントリポイント。ルータ登録と起動時初期化を行う。"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import settings
from backend.app.core.database import init_db, SessionLocal
from backend.app.core.security import get_password_hash
from backend.app.repositories.user import UserRepository
from backend.app.models import User

from backend.app.api import auth as auth_router
from backend.app.api import items as items_router
from backend.app.api import reservations as reservations_router
from backend.app.api import loans as loans_router
from backend.app.api import users as users_router


app = FastAPI(title=settings.app_name)


# CORS 設定
origins = [o.strip() for o in settings.cors_allow_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    """起動時にDB初期化と管理者投入を行う。"""

    await init_db()
    async with SessionLocal() as session:
        await _ensure_admin(session)


async def _ensure_admin(session: AsyncSession) -> None:
    """初期管理者を作成する（存在すれば何もしない）。"""

    repo = UserRepository(session)
    admin = await repo.get_by_email(settings.admin_email)
    if admin:
        return
    user = User(
        email=settings.admin_email,
        name="Admin",
        role="admin",
        password_hash=get_password_hash(settings.admin_password),
    )
    await repo.add(user)
    await session.commit()


# ルータ登録
app.include_router(auth_router.router)
app.include_router(items_router.router)
app.include_router(reservations_router.router)
app.include_router(loans_router.router)
app.include_router(users_router.router)


@app.get("/health")
async def health():
    """簡易ヘルスチェック。"""

    return {"status": "ok"}


__all__ = ["app"]
