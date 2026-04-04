"""DB接続・セッション管理"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://appuser:apppassword@db:5432/equipment_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI依存性注入用DBセッション取得"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
