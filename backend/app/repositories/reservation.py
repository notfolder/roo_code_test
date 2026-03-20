"""Reservationリポジトリ。"""

from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models import Reservation
from .base import BaseRepository


class ReservationRepository(BaseRepository[Reservation]):
    """予約のCRUD/検索処理。"""

    def __init__(self, session: AsyncSession):
        super().__init__(Reservation, session)

    async def list_by_user(self, user_id) -> List[Reservation]:
        stmt = select(Reservation).where(Reservation.user_id == user_id)
        res = await self.session.execute(stmt)
        return res.scalars().all()
