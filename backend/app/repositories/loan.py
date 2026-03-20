"""Loanリポジトリ。"""

from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models import Loan
from .base import BaseRepository


class LoanRepository(BaseRepository[Loan]):
    """貸出のCRUD/検索処理。"""

    def __init__(self, session: AsyncSession):
        super().__init__(Loan, session)

    async def list_overdue(self) -> List[Loan]:
        stmt = select(Loan).where(Loan.status.in_(["lent", "overdue"]))
        res = await self.session.execute(stmt)
        return res.scalars().all()
