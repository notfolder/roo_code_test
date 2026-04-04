"""usersテーブルのDB操作"""
from sqlalchemy.orm import Session
from models.user import User


class UserRepository:
    @staticmethod
    def find_all(db: Session) -> list[User]:
        """全ユーザーを取得する"""
        return db.query(User).order_by(User.id).all()

    @staticmethod
    def find_by_id(db: Session, user_id: int) -> User | None:
        """IDでユーザーを取得する"""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def find_by_login_id(db: Session, login_id: str) -> User | None:
        """ログインIDでユーザーを取得する"""
        return db.query(User).filter(User.login_id == login_id).first()

    @staticmethod
    def save(db: Session, user: User) -> User:
        """ユーザーを保存（新規・更新）する"""
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user: User) -> None:
        """ユーザーを削除する"""
        db.delete(user)
        db.commit()
