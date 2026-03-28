"""
アカウント管理ルーター
アカウントの一覧取得・作成・削除エンドポイントを提供する（管理担当者のみ）
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountResponse
from app.services.account_service import AccountService

router = APIRouter(prefix="/api/accounts", tags=["アカウント管理"])


@router.get("/", response_model=list[AccountResponse])
def list_accounts(
    db: Session = Depends(get_db),
    _: Account = Depends(require_admin),
):
    """
    全アカウント一覧を返す（管理担当者のみ）
    """
    return AccountService.list_accounts(db)


@router.post("/", response_model=AccountResponse, status_code=201)
def create_account(
    data: AccountCreate,
    db: Session = Depends(get_db),
    _: Account = Depends(require_admin),
):
    """
    新規アカウントを作成する（管理担当者のみ）
    """
    return AccountService.create_account(db, data)


@router.delete("/{account_id}", status_code=204)
def delete_account(
    account_id: int,
    db: Session = Depends(get_db),
    _: Account = Depends(require_admin),
):
    """
    アカウントを削除する（管理担当者のみ）
    """
    AccountService.delete_account(db, account_id)
    return None
