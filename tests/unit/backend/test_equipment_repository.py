import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.equipment import Equipment
from app.repositories.equipment import EquipmentRepository

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_add_and_get_equipment(db):
    repo = EquipmentRepository(db)
    eq = Equipment(name="テストPC", category="ノートPC", status="available")
    repo.add(eq)
    db.commit()

    found = repo.get(eq.id)
    assert found is not None
    assert found.name == "テストPC"


def test_list_equipment(db):
    repo = EquipmentRepository(db)
    for i in range(3):
        repo.add(Equipment(name=f"PC{i}", category="ノートPC", status="available"))
    db.commit()
    assert len(repo.list()) == 3


def test_delete_equipment(db):
    repo = EquipmentRepository(db)
    eq = Equipment(name="削除PC", category="ノートPC", status="available")
    repo.add(eq)
    db.commit()
    eq_id = eq.id
    repo.delete(eq)
    db.commit()
    assert repo.get(eq_id) is None
