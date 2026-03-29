import pytest
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
    db.add(admin)
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
def auth_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


def test_login_success(client):
    res = client.post("/api/auth/login", json={"login_id": "admin", "password": "admin1234"})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["role"] == "admin"


def test_login_failure(client):
    res = client.post("/api/auth/login", json={"login_id": "admin", "password": "wrong"})
    assert res.status_code == 401


def test_list_equipment_requires_auth(client):
    res = client.get("/api/equipment/")
    assert res.status_code == 403


def test_create_and_list_equipment(client, auth_headers):
    res = client.post(
        "/api/equipment/",
        json={"name": "テストPC", "category": "ノートPC"},
        headers=auth_headers,
    )
    assert res.status_code == 201
    assert res.json()["name"] == "テストPC"

    res2 = client.get("/api/equipment/", headers=auth_headers)
    assert res2.status_code == 200
    assert len(res2.json()) == 1


def test_delete_equipment_on_loan_fails(client, auth_headers):
    # 備品作成
    eq_res = client.post(
        "/api/equipment/",
        json={"name": "貸出PC", "category": "ノートPC"},
        headers=auth_headers,
    )
    eq_id = eq_res.json()["id"]

    # ユーザー取得 (adminのid)
    users_res = client.get("/api/users/", headers=auth_headers)
    user_id = users_res.json()[0]["id"]

    # 貸出登録
    client.post(
        "/api/loans/",
        json={"equipment_id": eq_id, "user_id": user_id, "loan_date": "2026-03-29"},
        headers=auth_headers,
    )

    # 貸出中は削除不可
    del_res = client.delete(f"/api/equipment/{eq_id}", headers=auth_headers)
    assert del_res.status_code == 400


def test_create_and_return_loan(client, auth_headers):
    eq_res = client.post(
        "/api/equipment/",
        json={"name": "カメラ", "category": "カメラ"},
        headers=auth_headers,
    )
    eq_id = eq_res.json()["id"]
    users_res = client.get("/api/users/", headers=auth_headers)
    user_id = users_res.json()[0]["id"]

    loan_res = client.post(
        "/api/loans/",
        json={"equipment_id": eq_id, "user_id": user_id, "loan_date": "2026-03-29"},
        headers=auth_headers,
    )
    assert loan_res.status_code == 201
    loan_id = loan_res.json()["id"]

    return_res = client.put(
        f"/api/loans/{loan_id}/return",
        json={"return_date": "2026-03-30"},
        headers=auth_headers,
    )
    assert return_res.status_code == 200
    assert return_res.json()["status"] == "returned"
