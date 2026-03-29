from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_login_id(self, login_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.login_id == login_id).first()

    def has_active_loans(self, user_id: int) -> bool:
        from app.models.loan_record import LoanRecord
        return (
            self.db.query(LoanRecord)
            .filter(LoanRecord.user_id == user_id, LoanRecord.status == "active")
            .first()
        ) is not None
