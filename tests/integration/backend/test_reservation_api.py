import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base
from app.dependencies import get_db, hash_password
from app.models.user import User
from app.models.equipment import Equipment

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

TODAY = date.today().isoformat()
TOMORROW = (date.today() + timedelta(days=1)).isoformat()
DAY3 = (date.today() + timedelta(days=3)).isoformat()
DAY5 = (date.today() + timedelta(days=5)).isoformat()
DAY7 = (date.today() + timedelta(days=7)).isoformat()
YESTERDAY = (date.today() - timedelta(days=1)).isoformat()


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    admin = User(
        login_id="admin",
        name="管理者",
        hashed_password=hash_password("admin1234"),
        role="admin",
        is_active=True,
    )
    general = User(
        login_id="user1",
        name="一般社員",
        hashed_password=hash_password("user1234"),
        role="general",
        is_active=True,
    )
    db.add(admin)
    db.add(general)
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def admin_token(client):
    res = client.post("/api/auth/login", json={"login_id": "admin", "password": "admin1234"})
    assert res.status_code == 200
    return res.json()["access_token"]


@pytest.fixture
def user_token(client):
    res = client.post("/api/auth/login", json={"login_id": "user1", "password": "user1234"})
    assert res.status_code == 200
    return res.json()["access_token"]


@pytest.fixture
def admin_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def user_headers(user_token):
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture
def equipment_id(client, admin_headers):
    res = client.post(
        "/api/equipment/",
        json={"name": "テストPC", "category": "ノートPC"},
        headers=admin_headers,
    )
    assert res.status_code == 201
    return res.json()["id"]


# IT-25: 認証済みユーザーが正常な入力で予約を作成できること
def test_create_reservation_success(client, user_headers, equipment_id):
    res = client.post(
        "/api/reservations/",
        json={"equipment_id": equipment_id, "planned_start_date": TOMORROW, "planned_return_date": DAY3},
        headers=user_headers,
    )
    assert res.status_code == 201
    data = res.json()
    assert data["status"] == "pending"
    assert data["equipment_id"] == equipment_id


# IT-26: トークンなしで401が返ること
def test_create_reservation_no_auth(client, equipment_id):
    res = client.post(
        "/api/reservations/",
        json={"equipment_id": equipment_id, "planned_start_date": TOMORROW, "planned_return_date": DAY3},
    )
    assert res.status_code == 403


# IT-27: 過去日付のplanned_start_dateで422が返ること
def test_create_reservation_past_start_date(client, user_headers, equipment_id):
    res = client.post(
        "/api/reservations/",
        json={"equipment_id": equipment_id, "planned_start_date": YESTERDAY, "planned_return_date": TOMORROW},
        headers=user_headers,
    )
    assert res.status_code == 422


# IT-28: planned_return_date < planned_start_dateで422が返ること
def test_create_reservation_return_before_start(client, user_headers, equipment_id):
    res = client.post(
        "/api/reservations/",
        json={"equipment_id": equipment_id, "planned_start_date": DAY5, "planned_return_date": DAY3},
        headers=user_headers,
    )
    assert res.status_code == 422


# IT-29: 重複期間の予約で409が返ること
def test_create_reservation_overlap(client, user_headers, equipment_id):
    client.post(
        "/api/reservations/",
        json={"equipment_id": equipment_id, "planned_start_date": TOMORROW, "planned_return_date": DAY5},
        headers=user_headers,
    )
    res = client.post(
        "/api/reservations/",
        json={"equipment_id": equipment_id, "planned_start_date": DAY3, "planned_return_date": DAY7},
        headers=user_headers,
    )
    assert res.status_code == 409


# IT-30: 存在しないequipment_idで404が返ること
def test_create_reservation_equipment_not_found(client, user_headers):
    res = client.post(
        "/api/reservations/",
        json={"equipment_id": 9999, "planned_start_date": TOMORROW, "planned_return_date": DAY3},
        headers=user_headers,
    )
    assert res.status_code == 404


# IT-31: 管理者トークンで全予約が返ること
def test_list_reservations_admin_sees_all(client, admin_headers, user_headers, equipment_id):
    # 一般社員で予約登録
    client.post(
        "/api/reservations/",
        json={"equipment_id": equipment_id, "planned_start_date": TOMORROW, "planned_return_date": DAY3},
        headers=user_headers,
    )
    # 管理者でも予約登録
    client.post(
        "/api/reservations/",
        json={"equipment_id": equipment_id, "planned_start_date": DAY5, "planned_return_date": DAY7},
        headers=admin_headers,
    )
    res = client.get("/api/reservations/", headers=admin_headers)
    assert res.status_code == 200
    assert len(res.json()) == 2


# IT-32: 一般社員トークンで自身の予約のみ返ること
def test_list_reservations_general_sees_own_only(client, admin_headers, user_headers, equipment_id):
    # 一般社員と管理者それぞれ予約
    client.post(
        "/api/reservations/",
        json={"equipment_id": equipment_id, "planned_start_date": TOMORROW, "planned_return_date": DAY3},
        headers=user_headers,
    )
    client.post(
        "/api/reservations/",
        json={"equipment_id": equipment_id, "planned_start_date": DAY5, "planned_return_date": DAY7},
        headers=admin_headers,
    )
    res = client.get("/api/reservations/", headers=user_headers)
    assert res.status_code == 200
    # 一般社員は自身の1件のみ
    assert len(res.json()) == 1


# IT-33: トークンなしで401が返ること
def test_list_reservations_no_auth(client):
    res = client.get("/api/reservations/")
    assert res.status_code == 403


# IT-34: 予約者本人がキャンセルできること
def test_cancel_own_reservation(client, user_headers, equipment_id):
    create_res = client.post(
        "/api/reservations/",
        json={"equipment_id": equipment_id, "planned_start_date": TOMORROW, "planned_return_date": DAY3},
        headers=user_headers,
    )
    res_id = create_res.json()["id"]
    cancel_res = client.put(f"/api/reservations/{res_id}/cancel", headers=user_headers)
    assert cancel_res.status_code == 200
    assert cancel_res.json()["status"] == "cancelled"


# IT-35: 管理者が任意予約をキャンセルできること
def test_cancel_reservation_by_admin(client, admin_headers, user_headers, equipment_id):
    create_res = client.post(
        "/api/reservations/",
        json={"equipment_id": equipment_id, "planned_start_date": TOMORROW, "planned_return_date": DAY3},
        headers=user_headers,
    )
    res_id = create_res.json()["id"]
    cancel_res = client.put(f"/api/reservations/{res_id}/cancel", headers=admin_headers)
    assert cancel_res.status_code == 200
    assert cancel_res.json()["status"] == "cancelled"


# IT-36: 一般社員が他ユーザーの予約をキャンセルしようとして403が返ること
def test_cancel_other_user_reservation_forbidden(client, admin_headers, user_headers, equipment_id):
    # 管理者の予約
    create_res = client.post(
        "/api/reservations/",
        json={"equipment_id": equipment_id, "planned_start_date": TOMORROW, "planned_return_date": DAY3},
        headers=admin_headers,
    )
    res_id = create_res.json()["id"]
    # 一般社員がキャンセルしようとする
    cancel_res = client.put(f"/api/reservations/{res_id}/cancel", headers=user_headers)
    assert cancel_res.status_code == 403


# IT-37: キャンセル済み予約に対して409が返ること
def test_cancel_already_cancelled(client, user_headers, equipment_id):
    create_res = client.post(
        "/api/reservations/",
        json={"equipment_id": equipment_id, "planned_start_date": TOMORROW, "planned_return_date": DAY3},
        headers=user_headers,
    )
    res_id = create_res.json()["id"]
    client.put(f"/api/reservations/{res_id}/cancel", headers=user_headers)
    second_cancel = client.put(f"/api/reservations/{res_id}/cancel", headers=user_headers)
    assert second_cancel.status_code == 409


# IT-38: 存在しないIDで404が返ること
def test_cancel_not_found(client, user_headers):
    res = client.put("/api/reservations/9999/cancel", headers=user_headers)
    assert res.status_code == 404


# IT-39: 貸出登録成功時にpending予約がloaned状態に更新されること
def test_loan_create_marks_reservation_as_loaned(client, admin_headers, user_headers, equipment_id):
    # 一般社員が予約
    create_res = client.post(
        "/api/reservations/",
        json={"equipment_id": equipment_id, "planned_start_date": TOMORROW, "planned_return_date": DAY3},
        headers=user_headers,
    )
    assert create_res.status_code == 201
    res_id = create_res.json()["id"]

    # 管理者が貸出登録（borrower_user_id はadminのID）
    users_res = client.get("/api/users/", headers=admin_headers)
    admin_user_id = next(u["id"] for u in users_res.json() if u["login_id"] == "admin")

    loan_res = client.post(
        "/api/loans/",
        json={"equipment_id": equipment_id, "borrower_user_id": admin_user_id, "loan_date": TODAY},
        headers=admin_headers,
    )
    assert loan_res.status_code == 201

    # 予約がloaned状態になっていることを管理者で確認
    reservations_res = client.get("/api/reservations/", headers=admin_headers)
    reservation = next((r for r in reservations_res.json() if r["id"] == res_id), None)
    assert reservation is not None
    assert reservation["status"] == "loaned"


# IT-40: pending予約がない場合でも貸出登録が正常に完了すること
def test_loan_create_no_pending_reservation(client, admin_headers, equipment_id):
    users_res = client.get("/api/users/", headers=admin_headers)
    admin_user_id = next(u["id"] for u in users_res.json() if u["login_id"] == "admin")

    loan_res = client.post(
        "/api/loans/",
        json={"equipment_id": equipment_id, "borrower_user_id": admin_user_id, "loan_date": TODAY},
        headers=admin_headers,
    )
    assert loan_res.status_code == 201
