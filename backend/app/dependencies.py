"""
依存性注入モジュール
認証済みユーザーの取得と管理担当者権限チェックを提供する共通モジュール
全ルーターからDIとして利用することで、認証・認可処理を一元管理する
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import decode_access_token
from app.repositories.account_repository import AccountRepository
from app.models.account import Account

# BearerトークンをAuthorizationヘッダーから取得するスキーム
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Account:
    """
    JWTトークンを検証し、認証済みユーザーのAccountオブジェクトを返す
    トークンが無効・期限切れ・ユーザー不存在の場合は401エラーを送出する
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="認証が必要です",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(credentials.credentials)
        account_name: str = payload.get("sub")
        if account_name is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    account = AccountRepository.find_by_name(db, account_name)
    if account is None:
        raise credentials_exception
    return account


def require_admin(current_user: Account = Depends(get_current_user)) -> Account:
    """
    ログインユーザーが管理担当者（admin）であることを確認する
    一般社員の場合は403エラーを送出する
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="この操作には管理担当者権限が必要です",
        )
    return current_user
