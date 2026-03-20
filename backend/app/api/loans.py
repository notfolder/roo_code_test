"""貸出/返却/未返却一覧エンドポイント。"""

from datetime import date
from fastapi import APIRouter, Depends

from backend.app.schemas.loan import LoanCreate, LoanReturn, LoanRead
from backend.app.services.loan import LoanService
from backend.app.api.deps import DBSession
from backend.app.core.deps import get_current_user, require_admin

router = APIRouter(prefix="/loans", tags=["loans"], dependencies=[Depends(require_admin)])


@router.post("", response_model=LoanRead)
async def start_loan(data: LoanCreate, db: DBSession):
    service = LoanService(db)
    return await service.start_loan(data.reservation_id)


@router.post("/{loan_id}/return", response_model=LoanRead)
async def finish_loan(loan_id, data: LoanReturn, db: DBSession):
    service = LoanService(db)
    return await service.finish_loan(loan_id, data.actual_return_date)


@router.get("/overdue", response_model=list[LoanRead])
async def list_overdue(db: DBSession):
    service = LoanService(db)
    return await service.list_overdue()
