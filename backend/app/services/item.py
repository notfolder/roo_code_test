"""備品サービス。"""

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models import Item
from backend.app.repositories.item import ItemRepository
from backend.app.schemas.item import ItemCreate, ItemUpdate
from backend.app.services.log import LogService


class ItemService:
    """備品のビジネスロジック。"""

    def __init__(self, session: AsyncSession):
        self.repo = ItemRepository(session)
        self.log = LogService(session)
        self.session = session

    async def create(self, data: ItemCreate) -> Item:
        existing = await self.repo.get_by_code(data.item_code)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="備品コードが重複しています")
        item = Item(item_code=data.item_code, name=data.name, status=data.status)
        await self.repo.add(item)
        await self.log.record(None, "create_item", "item", item.id, f"{item.item_code} 作成")
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def update(self, item_id, data: ItemUpdate) -> Item:
        item = await self.repo.get(item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="備品が見つかりません")
        if data.name is not None:
            item.name = data.name
        if data.status is not None:
            item.status = data.status
        await self.log.record(None, "update_item", "item", item.id, f"{item.item_code} 更新")
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def list_all(self):
        return await self.repo.list()
