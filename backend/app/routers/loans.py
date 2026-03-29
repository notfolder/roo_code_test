from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user, require_admin
from app.services.loan import LoanService
from app.schemas.loan_record import LoanCreate, ReturnUpdate, LoanRecordResponse
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[LoanRecordResponse])
def list_loans(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return LoanService(db).list_loans()


@router.get("/active", response_model=List[LoanRecordResponse])
def list_active_loans(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return LoanService(db).list_active_loans()


@router.post("/", response_model=LoanRecordResponse, status_code=201)
def create_loan(data: LoanCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return LoanService(db).create_loan(data)


@router.put("/{loan_id}/return", response_model=LoanRecordResponse)
def return_loan(loan_id: int, data: ReturnUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return LoanService(db).return_loan(loan_id, data)
