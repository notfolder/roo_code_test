"""Itemリポジトリ。"""

from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models import Item
from .base import BaseRepository


class ItemRepository(BaseRepository[Item]):
    """備品のCRUD/検索処理。"""

    def __init__(self, session: AsyncSession):
        super().__init__(Item, session)

    async def get_by_code(self, code: str) -> Optional[Item]:
        stmt = select(Item).where(Item.item_code == code)
        res = await self.session.execute(stmt)
        return res.scalars().first()
