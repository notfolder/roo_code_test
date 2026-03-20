"""備品エンドポイント。"""

from fastapi import APIRouter, Depends

from backend.app.schemas.item import ItemCreate, ItemUpdate, ItemRead
from backend.app.services.item import ItemService
from backend.app.api.deps import DBSession
from backend.app.core.deps import get_current_user, require_admin

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemRead], dependencies=[Depends(get_current_user)])
async def list_items(db: DBSession):
    service = ItemService(db)
    return await service.list_all()


@router.post("", response_model=ItemRead, dependencies=[Depends(require_admin)])
async def create_item(data: ItemCreate, db: DBSession):
    service = ItemService(db)
    return await service.create(data)


@router.put("/{item_id}", response_model=ItemRead, dependencies=[Depends(require_admin)])
async def update_item(item_id, data: ItemUpdate, db: DBSession):
    service = ItemService(db)
    return await service.update(item_id, data)
