import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret")

from app.db import get_db
from app.main import app
from app.models import Base, Item, LoanRecord, User
from app.security import hash_password

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database() -> Generator[None, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        admin = User(
            email="admin@example.com",
            hashed_password=hash_password("admin1234"),
            name="Admin",
            role="admin",
            status="active",
        )
        employee = User(
            email="employee@example.com",
            hashed_password=hash_password("employee1234"),
            name="Employee",
            role="employee",
            status="active",
        )
        db.add_all([admin, employee])
        db.flush()

        item_a = Item(asset_number="PC-001", name="Surface 3", state="available")
        item_b = Item(
            asset_number="PC-002",
            name="MacBook",
            state="lent",
            current_user_id=employee.id,
        )
        db.add_all([item_a, item_b])
        db.flush()
        db.add(LoanRecord(item_id=item_b.id, user_id=employee.id))
        db.commit()

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def admin_token(client: TestClient) -> str:
    response = client.post(
        "/api/auth/login", json={"email": "admin@example.com", "password": "admin1234"}
    )
    return response.json()["access_token"]


@pytest.fixture
def employee_token(client: TestClient) -> str:
    response = client.post(
        "/api/auth/login",
        json={"email": "employee@example.com", "password": "employee1234"},
    )
    return response.json()["access_token"]
