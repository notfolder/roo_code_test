from sqlalchemy import select

from app.models import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def find_by_email(self, email: str) -> User | None:
        return self.session.scalar(select(User).where(User.email == email))

    def find_by_id(self, user_id: str) -> User | None:
        return self.session.scalar(select(User).where(User.id == user_id))
