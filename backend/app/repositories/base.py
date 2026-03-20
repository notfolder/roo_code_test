"""Repositoryのベースクラス群。"""

from typing import Generic, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """CRUDの共通処理を提供するベースリポジトリ。"""

    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id_):
        return await self.session.get(self.model, id_)

    async def list(self):
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def add(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def delete(self, obj: T) -> None:
        await self.session.delete(obj)

