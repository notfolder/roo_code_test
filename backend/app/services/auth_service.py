"""
認証サービス
ログイン認証とJWTトークン生成の業務ロジックを担う
"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.account_repository import AccountRepository
from app.schemas.auth import TokenResponse
from app.security import verify_password, create_access_token


class AuthService:
    """認証業務ロジックを提供するサービス"""

    @staticmethod
    def login(db: Session, account_name: str, password: str) -> TokenResponse:
        """
        アカウント名とパスワードを検証し、JWTトークンを返す
        アカウントが存在しない、またはパスワードが一致しない場合は401エラーを送出する
        """
        account = AccountRepository.find_by_name(db, account_name)

        # アカウントが存在しない場合、またはパスワードが一致しない場合は同一のエラーを返す
        # （情報漏洩を防ぐためにどちらが原因かを明示しない）
        if account is None or not verify_password(password, account.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="アカウント名またはパスワードが正しくありません",
            )

        # JWTペイロードにアカウント名と役割を含める
        token = create_access_token({"sub": account.account_name, "role": account.role})
        return TokenResponse(access_token=token, role=account.role)
