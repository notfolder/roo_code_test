"""貸出サービス。"""

from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models import Loan, Reservation
from backend.app.repositories.loan import LoanRepository
from backend.app.repositories.reservation import ReservationRepository
from backend.app.services.log import LogService


class LoanService:
    """貸出/返却のビジネスロジック。"""

    def __init__(self, session: AsyncSession):
        self.repo = LoanRepository(session)
        self.resv_repo = ReservationRepository(session)
        self.log = LogService(session)
        self.session = session

    async def start_loan(self, reservation_id) -> Loan:
        reservation = await self.resv_repo.get(reservation_id)
        if not reservation or reservation.status != "reserved":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="予約が開始可能ではありません")

        today = date.today()
        if today < reservation.start_date:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="開始日前です")

        loan = Loan(
            reservation_id=reservation.id,
            loan_start_date=today,
            planned_return_date=reservation.end_date,
            status="lent",
        )
        await self.repo.add(loan)
        reservation.status = "reserved"  # ステータス維持
        await self.log.record(None, "start_loan", "loan", loan.id, "貸出開始")
        await self.session.commit()
        await self.session.refresh(loan)
        return loan

    async def finish_loan(self, loan_id, actual_return_date: date) -> Loan:
        loan = await self.repo.get(loan_id)
        if not loan:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="貸出が見つかりません")
        loan.actual_return_date = actual_return_date
        loan.status = "returned"
        await self.log.record(None, "finish_loan", "loan", loan.id, "返却完了")
        await self.session.commit()
        await self.session.refresh(loan)
        return loan

    async def list_overdue(self):
        loans = await self.repo.list_overdue()
        today = date.today()
        for loan in loans:
            if loan.status == "lent" and loan.planned_return_date < today:
                loan.status = "overdue"
        await self.session.commit()
        return loans
