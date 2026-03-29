import pytest
from datetime import date, timedelta
from unittest.mock import MagicMock, patch
from app.services.loan import LoanService
from app.models.equipment import Equipment
from app.models.loan_record import LoanRecord
from app.models.user import User
from app.schemas.loan_record import LoanCreate


def _make_equipment(eq_id=1, status="available"):
    e = Equipment()
    e.id = eq_id
    e.name = "テストPC"
    e.status = status
    return e


def _make_user(user_id=1):
    u = User()
    u.id = user_id
    u.name = "テストユーザー"
    u.role = "general"
    return u


def _make_loan(loan_id=1, equipment_id=1):
    from datetime import datetime
    l = LoanRecord()
    l.id = loan_id
    l.equipment_id = equipment_id
    l.user_id = 1
    l.loan_date = date.today()
    l.status = "active"
    l.created_at = datetime.now()
    return l


def _make_service():
    db = MagicMock()
    service = LoanService.__new__(LoanService)
    service.db = db
    service.loan_repo = MagicMock()
    service.equipment_repo = MagicMock()
    service.user_repo = MagicMock()
    service.reservation_repo = MagicMock()
    return service, db


# UT-37: 貸出登録成功時に対応するpending予約がloaned状態に更新されること
def test_create_loan_marks_pending_reservation_as_loaned():
    service, db = _make_service()
    equipment = _make_equipment()
    user = _make_user()
    loan = _make_loan()

    service.equipment_repo.get_for_update.return_value = equipment
    service.user_repo.get.return_value = user
    service.loan_repo.add = MagicMock()
    service.reservation_repo.mark_as_loaned = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()

    with patch("app.services.loan.LoanRecord") as MockLoanRecord:
        MockLoanRecord.return_value = loan

        with patch.object(service, "_to_response") as mock_response:
            mock_response.return_value = MagicMock()
            service.create_loan(LoanCreate(equipment_id=1, borrower_user_id=1, loan_date=date.today()))

    service.reservation_repo.mark_as_loaned.assert_called_once_with(1)


# UT-38: 対応するpending予約がない場合でも貸出登録が正常に完了すること
def test_create_loan_no_pending_reservation_succeeds():
    service, db = _make_service()
    equipment = _make_equipment()
    user = _make_user()
    loan = _make_loan()

    service.equipment_repo.get_for_update.return_value = equipment
    service.user_repo.get.return_value = user
    service.loan_repo.add = MagicMock()
    # mark_as_loaned がNoneを返す（pending予約なし）
    service.reservation_repo.mark_as_loaned.return_value = None
    db.commit = MagicMock()
    db.refresh = MagicMock()

    with patch("app.services.loan.LoanRecord") as MockLoanRecord:
        MockLoanRecord.return_value = loan

        with patch.object(service, "_to_response") as mock_response:
            mock_response.return_value = MagicMock()
            # 例外が発生しないことを確認
            service.create_loan(LoanCreate(equipment_id=1, borrower_user_id=1, loan_date=date.today()))

    service.reservation_repo.mark_as_loaned.assert_called_once_with(1)
    db.commit.assert_called_once()
