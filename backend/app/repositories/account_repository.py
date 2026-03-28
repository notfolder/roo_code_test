"""
アカウントリポジトリ
accountsテーブルに対するDB操作を集約する
"""
from sqlalchemy.orm import Session

from app.models.account import Account
from app.schemas.account import AccountCreate
from app.security import hash_password


class AccountRepository:
    """アカウントテーブルのCRUD操作を提供するリポジトリ"""

    @staticmethod
    def find_by_name(db: Session, account_name: str) -> Account | None:
        """
        アカウント名でアカウントを取得する
        存在しない場合はNoneを返す
        """
        return db.query(Account).filter(Account.account_name == account_name).first()

    @staticmethod
    def find_by_id(db: Session, account_id: int) -> Account | None:
        """
        IDでアカウントを取得する
        存在しない場合はNoneを返す
        """
        return db.query(Account).filter(Account.id == account_id).first()

    @staticmethod
    def find_all(db: Session) -> list[Account]:
        """
        全アカウントを作成日時の昇順で取得する
        """
        return db.query(Account).order_by(Account.created_at.asc()).all()

    @staticmethod
    def create(db: Session, data: AccountCreate) -> Account:
        """
        新規アカウントを作成してDBに保存する
        パスワードはbcryptでハッシュ化して保存する
        """
        account = Account(
            account_name=data.account_name,
            password_hash=hash_password(data.password),
            role=data.role,
        )
        db.add(account)
        db.flush()
        db.refresh(account)
        return account

    @staticmethod
    def delete(db: Session, account: Account) -> None:
        """
        指定されたアカウントを削除する
        """
        db.delete(account)
        db.flush()
