import pytest
from unittest.mock import MagicMock, patch
from datetime import date, timedelta
from fastapi import HTTPException
from app.services.reservation import ReservationService
from app.models.reservation import Reservation
from app.models.user import User
from app.models.equipment import Equipment
from app.schemas.reservation import ReservationCreate


def _make_user(role="general", user_id=1):
    u = User()
    u.id = user_id
    u.name = "テストユーザー"
    u.role = role
    return u


def _make_equipment(eq_id=1):
    e = Equipment()
    e.id = eq_id
    e.name = "テストPC"
    return e


def _make_reservation(res_id=1, user_id=1, equipment_id=1, status="pending"):
    from datetime import datetime
    r = Reservation()
    r.id = res_id
    r.user_id = user_id
    r.equipment_id = equipment_id
    r.planned_start_date = date.today() + timedelta(days=1)
    r.planned_return_date = date.today() + timedelta(days=3)
    r.status = status
    r.created_at = datetime.now()
    return r


def _make_service():
    db = MagicMock()
    service = ReservationService.__new__(ReservationService)
    service.db = db
    service.reservation_repo = MagicMock()
    service.equipment_repo = MagicMock()
    return service, db


# UT-23: 正常な入力で予約が作成されること
def test_create_reservation_success():
    service, db = _make_service()
    user = _make_user()
    equipment = _make_equipment()
    service.equipment_repo.get.return_value = equipment
    service.reservation_repo.check_overlap.return_value = False

    reservation = _make_reservation()
    service.reservation_repo.add.return_value = reservation

    # DB commit/refresh をモック
    db.commit = MagicMock()
    db.refresh = MagicMock()
    service.reservation_repo.add = MagicMock()

    # _to_response のためにユーザーリポジトリをモック
    with patch("app.services.reservation.UserRepository") as MockUserRepo:
        user_repo_instance = MagicMock()
        user_repo_instance.get.return_value = user
        MockUserRepo.return_value = user_repo_instance

        # db.query(Reservation)...for cancel は使わない
        data = ReservationCreate(
            equipment_id=1,
            planned_start_date=date.today() + timedelta(days=1),
            planned_return_date=date.today() + timedelta(days=3),
        )
        result = service.create_reservation(data, user)
    assert result is not None


# UT-24: planned_start_dateが過去日付で422例外が発生すること
def test_create_reservation_past_start_date():
    service, _ = _make_service()
    user = _make_user()
    data = ReservationCreate(
        equipment_id=1,
        planned_start_date=date.today() - timedelta(days=1),
        planned_return_date=date.today() + timedelta(days=1),
    )
    with pytest.raises(HTTPException) as exc:
        service.create_reservation(data, user)
    assert exc.value.status_code == 422


# UT-25: planned_return_date < planned_start_dateで422例外が発生すること
def test_create_reservation_return_before_start():
    service, _ = _make_service()
    user = _make_user()
    data = ReservationCreate(
        equipment_id=1,
        planned_start_date=date.today() + timedelta(days=3),
        planned_return_date=date.today() + timedelta(days=1),
    )
    with pytest.raises(HTTPException) as exc:
        service.create_reservation(data, user)
    assert exc.value.status_code == 422


# UT-26: 存在しないequipment_idで404例外が発生すること
def test_create_reservation_equipment_not_found():
    service, _ = _make_service()
    user = _make_user()
    service.equipment_repo.get.return_value = None
    data = ReservationCreate(
        equipment_id=999,
        planned_start_date=date.today() + timedelta(days=1),
        planned_return_date=date.today() + timedelta(days=3),
    )
    with pytest.raises(HTTPException) as exc:
        service.create_reservation(data, user)
    assert exc.value.status_code == 404


# UT-27: 重複する期間の予約が存在する場合に409例外が発生すること
def test_create_reservation_overlap():
    service, _ = _make_service()
    user = _make_user()
    service.equipment_repo.get.return_value = _make_equipment()
    service.reservation_repo.check_overlap.return_value = True
    data = ReservationCreate(
        equipment_id=1,
        planned_start_date=date.today() + timedelta(days=1),
        planned_return_date=date.today() + timedelta(days=3),
    )
    with pytest.raises(HTTPException) as exc:
        service.create_reservation(data, user)
    assert exc.value.status_code == 409


# UT-28: 重複しない期間の予約が存在する場合は正常に作成されること
def test_create_reservation_no_overlap():
    service, db = _make_service()
    user = _make_user()
    service.equipment_repo.get.return_value = _make_equipment()
    service.reservation_repo.check_overlap.return_value = False
    service.reservation_repo.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()

    with patch("app.services.reservation.UserRepository") as MockUserRepo:
        user_repo_instance = MagicMock()
        user_repo_instance.get.return_value = user
        MockUserRepo.return_value = user_repo_instance

        data = ReservationCreate(
            equipment_id=1,
            planned_start_date=date.today() + timedelta(days=5),
            planned_return_date=date.today() + timedelta(days=7),
        )
        result = service.create_reservation(data, user)
    assert result is not None


# UT-29: 予約者本人（一般社員）が自身の予約をキャンセルできること
def test_cancel_reservation_own_by_general():
    service, db = _make_service()
    user = _make_user(role="general", user_id=1)
    reservation = _make_reservation(user_id=1)

    db.query.return_value.filter.return_value.with_for_update.return_value.first.return_value = reservation
    db.commit = MagicMock()
    db.refresh = MagicMock()

    with patch("app.services.reservation.UserRepository") as MockUserRepo:
        user_repo_instance = MagicMock()
        user_repo_instance.get.return_value = user
        MockUserRepo.return_value = user_repo_instance

        result = service.cancel_reservation(1, user)
    assert result.status == "cancelled"


# UT-30: 管理者が任意の予約をキャンセルできること
def test_cancel_reservation_by_admin():
    service, db = _make_service()
    admin = _make_user(role="admin", user_id=99)
    reservation = _make_reservation(user_id=1)

    db.query.return_value.filter.return_value.with_for_update.return_value.first.return_value = reservation
    db.commit = MagicMock()
    db.refresh = MagicMock()

    with patch("app.services.reservation.UserRepository") as MockUserRepo:
        user_repo_instance = MagicMock()
        user_repo_instance.get.return_value = _make_user(user_id=1)
        MockUserRepo.return_value = user_repo_instance

        result = service.cancel_reservation(1, admin)
    assert result.status == "cancelled"


# UT-31: 一般社員が他ユーザーの予約のキャンセルで403例外が発生すること
def test_cancel_reservation_other_user_forbidden():
    service, db = _make_service()
    user = _make_user(role="general", user_id=2)
    reservation = _make_reservation(user_id=1)

    db.query.return_value.filter.return_value.with_for_update.return_value.first.return_value = reservation

    with pytest.raises(HTTPException) as exc:
        service.cancel_reservation(1, user)
    assert exc.value.status_code == 403


# UT-32: 存在しないIDで404例外が発生すること
def test_cancel_reservation_not_found():
    service, db = _make_service()
    user = _make_user()
    db.query.return_value.filter.return_value.with_for_update.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc:
        service.cancel_reservation(999, user)
    assert exc.value.status_code == 404


# UT-33: 既にキャンセル済みの予約で409例外が発生すること
def test_cancel_reservation_already_cancelled():
    service, db = _make_service()
    user = _make_user(user_id=1)
    reservation = _make_reservation(user_id=1, status="cancelled")

    db.query.return_value.filter.return_value.with_for_update.return_value.first.return_value = reservation

    with pytest.raises(HTTPException) as exc:
        service.cancel_reservation(1, user)
    assert exc.value.status_code == 409


# UT-34: 貸出済みの予約で409例外が発生すること
def test_cancel_reservation_already_loaned():
    service, db = _make_service()
    user = _make_user(user_id=1)
    reservation = _make_reservation(user_id=1, status="loaned")

    db.query.return_value.filter.return_value.with_for_update.return_value.first.return_value = reservation

    with pytest.raises(HTTPException) as exc:
        service.cancel_reservation(1, user)
    assert exc.value.status_code == 409


# UT-35: 管理者の場合は全予約が返ること
def test_get_reservations_admin_returns_all():
    service, _ = _make_service()
    admin = _make_user(role="admin")
    r1 = _make_reservation(res_id=1, user_id=1)
    r2 = _make_reservation(res_id=2, user_id=2)
    service.reservation_repo.list.return_value = [r1, r2]
    service.equipment_repo.get.return_value = _make_equipment()

    with patch("app.services.reservation.UserRepository") as MockUserRepo:
        user_repo_instance = MagicMock()
        user_repo_instance.get.return_value = _make_user()
        MockUserRepo.return_value = user_repo_instance

        result = service.get_reservations(admin)
    assert len(result) == 2


# UT-36: 一般社員の場合は自身の予約のみが返ること
def test_get_reservations_general_returns_own():
    service, _ = _make_service()
    user = _make_user(role="general", user_id=1)
    r1 = _make_reservation(res_id=1, user_id=1)
    service.reservation_repo.get_by_user_id.return_value = [r1]
    service.equipment_repo.get.return_value = _make_equipment()

    with patch("app.services.reservation.UserRepository") as MockUserRepo:
        user_repo_instance = MagicMock()
        user_repo_instance.get.return_value = user
        MockUserRepo.return_value = user_repo_instance

        result = service.get_reservations(user)
    assert len(result) == 1
    service.reservation_repo.get_by_user_id.assert_called_once_with(1)
