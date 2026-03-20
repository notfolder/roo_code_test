"""DB接続とセッション管理。アプリ起動時にテーブル作成も行う。"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import text

from .config import settings


Base = declarative_base()


# AsyncEngine を作成
engine = create_async_engine(
    settings.database_url,
    echo=False,
    future=True,
)

# セッションファクトリ
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI 依存性: 非同期セッションを提供する。"""

    async with SessionLocal() as session:
        yield session


async def init_db() -> None:
    """DB初期化: 拡張作成とテーブル作成、初期管理者投入。"""

    # btree_gist拡張は排他制約に必要
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS btree_gist"))
        # モデルのメタデータを取り込んでから create_all を呼ぶ必要がある
        import backend.app.models  # noqa: F401
        await conn.run_sync(Base.metadata.create_all)

