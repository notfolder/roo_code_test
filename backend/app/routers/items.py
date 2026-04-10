from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user, require_admin
from app.models.user import User
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.services.item_service import ItemService

router = APIRouter(prefix="/api/items", tags=["items"])
item_service = ItemService()


@router.get("", response_model=List[ItemResponse])
def get_items(
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return item_service.get_items(db)


@router.post("", response_model=ItemResponse, status_code=201)
def create_item(
    item_create: ItemCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    return item_service.create_item(db, item_create)


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: str,
    item_update: ItemUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    return item_service.update_item(db, item_id, item_update)


@router.delete("/{item_id}", status_code=204)
def delete_item(
    item_id: str,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    item_service.delete_item(db, item_id)
