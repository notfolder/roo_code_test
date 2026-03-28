"""
貸出管理ルーター
貸出記録の一覧取得・貸出登録・返却登録エンドポイントを提供する（管理担当者のみ）
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models.account import Account
from app.schemas.loan import LoanCreate, LoanResponse
from app.services.loan_service import LoanService

router = APIRouter(prefix="/api/loans", tags=["貸出管理"])


@router.get("/", response_model=list[LoanResponse])
def list_loans(
    db: Session = Depends(get_db),
    _: Account = Depends(require_admin),
):
    """
    全貸出記録一覧を返す（管理担当者のみ）
    """
    return LoanService.list_loans(db)


@router.post("/", response_model=LoanResponse, status_code=201)
def create_loan(
    data: LoanCreate,
    db: Session = Depends(get_db),
    current_user: Account = Depends(require_admin),
):
    """
    貸出を登録する（管理担当者のみ）
    備品の状態を確認し、悲観的ロックで二重貸出を防止する
    """
    return LoanService.create_loan(db, data, current_user.id)


@router.put("/{loan_id}/return", response_model=LoanResponse)
def return_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: Account = Depends(require_admin),
):
    """
    返却を登録する（管理担当者のみ）
    """
    return LoanService.return_loan(db, loan_id, current_user.id)
