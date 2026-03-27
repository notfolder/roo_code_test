"""遅延一覧API。"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.database import get_db
from app.services.overdue import OverdueService

router = APIRouter()


@router.get("")
def list_overdues(db: Session = Depends(get_db), _: deps.require_admin = Depends(deps.require_admin)):
    return OverdueService(db).list_overdues()

