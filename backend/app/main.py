"""
FastAPIアプリケーションエントリーポイント
アプリ初期化、ルーター登録、DB初期化（テーブル作成・初期管理者アカウント作成）を行う
"""
import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, SessionLocal, Base
from app.routers import auth, accounts, equipment, loans

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db() -> None:
    """
    アプリ起動時にDBの初期化を行う
    1. 全テーブルを作成する（既存テーブルはスキップ）
    2. accountsテーブルが空の場合のみ初期管理担当者アカウントを作成する
    """
    # 全モデルをインポートしてテーブルを認識させる
    from app.models import account, equipment as equip_model, loan_record  # noqa: F401

    # テーブルを作成する（既存の場合はスキップ）
    Base.metadata.create_all(bind=engine)
    logger.info("データベーステーブルの初期化が完了しました")

    # 初期管理担当者アカウントを作成する（テーブルが空の場合のみ）
    db = SessionLocal()
    try:
        from app.models.account import Account
        from app.security import hash_password

        count = db.query(Account).count()
        if count == 0:
            admin_name = os.getenv("INITIAL_ADMIN_NAME", "admin")
            admin_password = os.getenv("INITIAL_ADMIN_PASSWORD", "AdminPass123")
            admin = Account(
                account_name=admin_name,
                password_hash=hash_password(admin_password),
                role="admin",
            )
            db.add(admin)
            db.commit()
            logger.info(f"初期管理担当者アカウント「{admin_name}」を作成しました")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリ起動時にDB初期化を実行する"""
    init_db()
    yield


# FastAPIアプリケーションを生成する
app = FastAPI(
    title="社内備品管理・貸出管理システム",
    version="1.0.0",
    lifespan=lifespan,
)

# CORSミドルウェアを設定する（開発環境用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターを登録する
app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(equipment.router)
app.include_router(loans.router)
