from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.models import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    @staticmethod
    def list_items(db: Session) -> list[Item]:
        statement = (
            select(Item)
            .options(joinedload(Item.current_user))
            .order_by(Item.state.asc(), Item.asset_number.asc())
        )
        return list(db.scalars(statement).all())

    @staticmethod
    def get_item(db: Session, item_id: str, lock: bool = False) -> Item:
        statement = select(Item).where(Item.id == item_id)
        if lock:
            statement = statement.with_for_update()
        item = db.scalar(statement)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )
        return item

    @staticmethod
    def create_item(db: Session, payload: ItemCreate) -> Item:
        item = Item(
            asset_number=payload.asset_number, name=payload.name, state=payload.state
        )
        db.add(item)
        try:
            db.commit()
            db.refresh(item)
            return item
        except IntegrityError as exc:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Asset number already exists",
            ) from exc

    @staticmethod
    def update_item(db: Session, item_id: str, payload: ItemUpdate) -> Item:
        item = ItemService.get_item(db, item_id)

        item.name = payload.name
        item.state = payload.state
        if payload.state == "available":
            item.current_user_id = None

        db.commit()
        db.refresh(item)
        return item
