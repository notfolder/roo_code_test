"""
データベース接続・セッション管理モジュール
SQLAlchemyエンジンとセッションファクトリを提供する
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# 環境変数からデータベース接続URLを取得
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://appuser:apppassword@db:5432/appdb")

# SQLAlchemyエンジンを作成
engine = create_engine(DATABASE_URL)

# セッションファクトリを作成（autocommit/autoflushは無効化してトランザクションを手動管理）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """全ORMモデルの基底クラス"""
    pass


def get_db():
    """
    DBセッションをDI（依存性注入）で提供するジェネレーター関数
    リクエスト処理後に自動でセッションをクローズする
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
