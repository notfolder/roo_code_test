from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies import get_current_user, require_admin
from app.models import User
from app.schemas.item import (
    ItemCreate,
    ItemResponse,
    ItemUpdate,
    LoanRecordResponse,
    LoanRequest,
)
from app.services.item_service import ItemService
from app.services.loan_service import LoanService


router = APIRouter(prefix="/api/items", tags=["items"])


@router.get("", response_model=list[ItemResponse])
def list_items(_: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = ItemService.list_items(db)
    result = []
    for item in items:
        result.append(
            ItemResponse(
                id=item.id,
                asset_number=item.asset_number,
                name=item.name,
                state=item.state,
                current_user_id=item.current_user_id,
                current_user_name=item.current_user.name if item.current_user else None,
                updated_at=item.updated_at,
            )
        )
    return result


@router.post("", response_model=ItemResponse)
def create_item(
    payload: ItemCreate, _: User = Depends(require_admin), db: Session = Depends(get_db)
):
    item = ItemService.create_item(db, payload)
    return ItemResponse(
        id=item.id,
        asset_number=item.asset_number,
        name=item.name,
        state=item.state,
        current_user_id=item.current_user_id,
        current_user_name=item.current_user.name if item.current_user else None,
        updated_at=item.updated_at,
    )


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: str,
    payload: ItemUpdate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    item = ItemService.update_item(db, item_id, payload)
    return ItemResponse(
        id=item.id,
        asset_number=item.asset_number,
        name=item.name,
        state=item.state,
        current_user_id=item.current_user_id,
        current_user_name=item.current_user.name if item.current_user else None,
        updated_at=item.updated_at,
    )


@router.post("/{item_id}/loan", response_model=LoanRecordResponse)
def loan_item(
    item_id: str,
    payload: LoanRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    loan_record = LoanService.lend_item(
        db, item_id=item_id, user_id=payload.user_id, actor_id=current_user.id
    )
    return LoanRecordResponse(
        id=loan_record.id,
        item_id=loan_record.item_id,
        user_id=loan_record.user_id,
        lent_at=loan_record.lent_at,
        returned_at=loan_record.returned_at,
    )


@router.post("/{item_id}/return", response_model=LoanRecordResponse)
def return_item(
    item_id: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    loan_record = LoanService.return_item(db, item_id=item_id, actor_id=current_user.id)
    return LoanRecordResponse(
        id=loan_record.id,
        item_id=loan_record.item_id,
        user_id=loan_record.user_id,
        lent_at=loan_record.lent_at,
        returned_at=loan_record.returned_at,
    )
