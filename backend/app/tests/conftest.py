"""pytest 用の共通フィクスチャ。"""

import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.main import app
from backend.app.core.database import engine, Base, SessionLocal


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    # テスト用にテーブル作成
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture()
async def session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


@pytest.fixture()
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
