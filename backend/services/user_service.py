"""ユーザーのCRUDビジネスロジック"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from repositories.user_repository import UserRepository
from utils.password_util import PasswordUtil


class UserService:
    @staticmethod
    def get_all(db: Session) -> list[User]:
        """全ユーザー一覧を返す"""
        return UserRepository.find_all(db)

    @staticmethod
    def create(db: Session, login_id: str, username: str, password: str, role: str) -> User:
        """ユーザーを新規登録する。ログインID重複時は409を返す"""
        if not login_id.strip() or not username.strip() or not password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="入力してください")
        if UserRepository.find_by_login_id(db, login_id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="このログインIDは既に使用されています")
        user = User(
            login_id=login_id.strip(),
            username=username.strip(),
            password_hash=PasswordUtil.hash(password),
            role=role,
        )
        return UserRepository.save(db, user)

    @staticmethod
    def update(db: Session, user_id: int, username: str, role: str) -> User:
        """ユーザー名とロールを更新する"""
        if not username.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="入力してください")
        user = UserRepository.find_by_id(db, user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="対象データが見つかりません")
        user.username = username.strip()
        user.role = role
        return UserRepository.save(db, user)

    @staticmethod
    def delete(db: Session, user_id: int, current_user_id: int) -> None:
        """ユーザーを削除する。自己削除は403を返す"""
        if user_id == current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="自分自身のアカウントは削除できません")
        user = UserRepository.find_by_id(db, user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="対象データが見つかりません")
        UserRepository.delete(db, user)
