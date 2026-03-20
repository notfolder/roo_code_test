"""予約サービス。"""

from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models import Reservation
from backend.app.repositories.reservation import ReservationRepository
from backend.app.repositories.item import ItemRepository
from backend.app.schemas.reservation import ReservationCreate
from backend.app.services.log import LogService


class ReservationService:
    """予約のビジネスロジック。"""

    def __init__(self, session: AsyncSession):
        self.repo = ReservationRepository(session)
        self.item_repo = ItemRepository(session)
        self.log = LogService(session)
        self.session = session

    async def create(self, user_id, data: ReservationCreate) -> Reservation:
        # 備品存在/廃棄チェック
        item = await self.item_repo.get(data.item_id)
        if not item or item.status != "active":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="備品が利用不可です")

        # 期間バリデーション（最大7日、start<=end はスキーマで検証済み）
        if (data.end_date - data.start_date).days > 6:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="最大7日までです")

        reservation = Reservation(
            item_id=data.item_id,
            user_id=user_id,
            start_date=data.start_date,
            end_date=data.end_date,
            status="reserved",
        )
        try:
            await self.repo.add(reservation)
            await self.session.commit()
        except Exception as exc:  # 排他制約違反など
            await self.session.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="選択期間は予約済みです") from exc

        await self.session.refresh(reservation)
        await self.log.record(user_id, "create_reservation", "reservation", reservation.id, "予約作成")
        await self.session.commit()
        return reservation

    async def cancel(self, reservation_id, user_id):
        reservation = await self.repo.get(reservation_id)
        if not reservation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="予約が見つかりません")
        # 自分の予約か管理者用のチェックは API 層で current_user を見て実施する想定
        today = date.today()
        if today >= reservation.start_date:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="開始日当日はキャンセル不可です")
        reservation.status = "cancelled"
        await self.log.record(user_id, "cancel_reservation", "reservation", reservation.id, "予約キャンセル")
        await self.session.commit()
        await self.session.refresh(reservation)
        return reservation

    async def list_my(self, user_id):
        return await self.repo.list_by_user(user_id)

    async def list_all(self):
        return await self.repo.list()
