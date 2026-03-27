"""バッチAPI: 遅延更新ジョブ実行。"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.database import get_db
from app.services.overdue import OverdueService

router = APIRouter()


@router.post("/mark-overdue")
def run_mark_overdue(db: Session = Depends(get_db), _: deps.require_admin = Depends(deps.require_admin)):
    return OverdueService(db).mark_overdue()

