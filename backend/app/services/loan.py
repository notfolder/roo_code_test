from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.loan_record import LoanRecordRepository
from app.repositories.equipment import EquipmentRepository
from app.repositories.user import UserRepository
from app.models.loan_record import LoanRecord
from app.schemas.loan_record import LoanCreate, ReturnUpdate, LoanRecordResponse


class LoanService:
    def __init__(self, db: Session):
        self.loan_repo = LoanRecordRepository(db)
        self.equipment_repo = EquipmentRepository(db)
        self.user_repo = UserRepository(db)
        self.db = db

    def list_loans(self) -> List[LoanRecordResponse]:
        loans = self.loan_repo.list()
        return [self._to_response(loan) for loan in loans]

    def list_active_loans(self) -> List[LoanRecordResponse]:
        loans = self.loan_repo.list_active()
        return [self._to_response(loan) for loan in loans]

    def create_loan(self, data: LoanCreate) -> LoanRecordResponse:
        # pessimistic lock on equipment
        eq = self.equipment_repo.get_for_update(data.equipment_id)
        if not eq:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found")
        if eq.status != "available":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Equipment is not available",
            )
        user = self.user_repo.get(data.user_id)
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        loan = LoanRecord(
            equipment_id=data.equipment_id,
            user_id=data.user_id,
            loan_date=data.loan_date,
            status="active",
            purpose=data.purpose,
        )
        eq.status = "on_loan"
        self.loan_repo.add(loan)
        self.db.commit()
        self.db.refresh(loan)
        return self._to_response(loan)

    def return_loan(self, loan_id: int, data: ReturnUpdate) -> LoanRecordResponse:
        loan = self.loan_repo.get(loan_id)
        if not loan:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan record not found")
        if loan.status != "active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Loan is already returned",
            )
        # pessimistic lock on equipment
        eq = self.equipment_repo.get_for_update(loan.equipment_id)
        loan.return_date = data.return_date
        loan.status = "returned"
        eq.status = "available"
        self.db.commit()
        self.db.refresh(loan)
        return self._to_response(loan)

    def _to_response(self, loan: LoanRecord) -> LoanRecordResponse:
        eq = self.equipment_repo.get(loan.equipment_id)
        user = self.user_repo.get(loan.user_id)
        return LoanRecordResponse(
            id=loan.id,
            equipment_id=loan.equipment_id,
            user_id=loan.user_id,
            loan_date=loan.loan_date,
            return_date=loan.return_date,
            status=loan.status,
            purpose=loan.purpose,
            equipment_name=eq.name if eq else None,
            user_name=user.name if user else None,
        )
