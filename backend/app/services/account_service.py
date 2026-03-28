"""
アカウントサービス
アカウント管理の業務ロジックを担う
"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.account_repository import AccountRepository
from app.schemas.account import AccountCreate, AccountResponse


class AccountService:
    """アカウント業務ロジックを提供するサービス"""

    @staticmethod
    def list_accounts(db: Session) -> list[AccountResponse]:
        """
        全アカウントの一覧を返す
        """
        accounts = AccountRepository.find_all(db)
        return [AccountResponse.model_validate(a) for a in accounts]

    @staticmethod
    def create_account(db: Session, data: AccountCreate) -> AccountResponse:
        """
        新規アカウントを作成する
        アカウント名が既に存在する場合は409エラーを送出する
        """
        existing = AccountRepository.find_by_name(db, data.account_name)
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"アカウント名「{data.account_name}」は既に存在します",
            )
        account = AccountRepository.create(db, data)
        db.commit()
        return AccountResponse.model_validate(account)

    @staticmethod
    def delete_account(db: Session, account_id: int) -> None:
        """
        アカウントを削除する
        対象アカウントが存在しない場合は404エラーを送出する
        """
        account = AccountRepository.find_by_id(db, account_id)
        if account is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定されたアカウントが見つかりません",
            )
        AccountRepository.delete(db, account)
        db.commit()
