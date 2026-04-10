from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.item import Item
from app.models.lending_record import LendingRecord
from app.models.user import User
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse


class ItemService:
    def get_items(self, db: Session) -> List[ItemResponse]:
        rows = (
            db.query(Item, User.login_id)
            .outerjoin(
                LendingRecord,
                (LendingRecord.item_id == Item.id) & (LendingRecord.return_date.is_(None)),
            )
            .outerjoin(User, User.id == LendingRecord.borrower_user_id)
            .all()
        )
        result = []
        for item, borrower_name in rows:
            result.append(
                ItemResponse(
                    id=item.id,
                    name=item.name,
                    status=item.status,
                    borrower_name=borrower_name,
                )
            )
        return result

    def get_item(self, db: Session, item_id: str) -> Item:
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="指定されたリソースが見つかりません")
        return item

    def create_item(self, db: Session, item_create: ItemCreate) -> Item:
        if db.query(Item).filter(Item.id == item_create.id).first():
            raise HTTPException(status_code=409, detail="この管理番号は既に使用されています")
        item = Item(id=item_create.id, name=item_create.name, status="available")
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    def update_item(self, db: Session, item_id: str, item_update: ItemUpdate) -> Item:
        item = self.get_item(db, item_id)
        item.name = item_update.name
        db.commit()
        db.refresh(item)
        return item

    def delete_item(self, db: Session, item_id: str) -> None:
        item = self.get_item(db, item_id)
        if item.status == "lending":
            raise HTTPException(status_code=409, detail="貸出中の備品は削除できません")
        db.delete(item)
        db.commit()
