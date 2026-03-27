from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app import models
from app.config import settings
from app.database import Base, engine, get_db
from app.services import auth as auth_service
from app.api import (
    auth,
    users,
    equipments,
    reservations,
    lendings,
    returns,
    overdues,
    histories,
    jobs,
)


# FastAPI本体の初期化
app = FastAPI(title="備品管理・貸出予約API", version="1.0.0")


@app.on_event("startup")
def on_startup() -> None:
    """起動時にDBテーブル作成と初期管理者作成を実施する。"""
    Base.metadata.create_all(bind=engine)
    # 初期管理者の存在確認と作成
    with get_db() as db:
        auth_service.ensure_initial_admin(db)


@app.get("/health")
def health() -> dict:
    """簡易ヘルスチェック。監視/動作確認用。"""
    return {"status": "ok"}


# ルーター登録（機能別に分離）
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(equipments.router, prefix="/equipments", tags=["equipments"])
app.include_router(reservations.router, prefix="/reservations", tags=["reservations"])
app.include_router(lendings.router, prefix="/lendings", tags=["lendings"])
app.include_router(returns.router, prefix="/returns", tags=["returns"])
app.include_router(overdues.router, prefix="/overdues", tags=["overdues"])
app.include_router(histories.router, prefix="/histories", tags=["histories"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
