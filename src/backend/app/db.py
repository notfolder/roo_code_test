import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from app.models import Base, Item, LoanRecord, User
from app.security import hash_password


DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://app:app@db:5432/equipment"
)

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)


engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    with Session(engine) as db:
        _seed_initial_data(db)


def _seed_initial_data(db: Session) -> None:
    admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin1234")
    admin_name = os.getenv("ADMIN_NAME", "総務 太郎")

    existing_admin = db.scalar(select(User).where(User.email == admin_email))
    if not existing_admin:
        db.add(
            User(
                email=admin_email,
                hashed_password=hash_password(admin_password),
                name=admin_name,
                role="admin",
                status="active",
            )
        )

    default_employee = db.scalar(
        select(User).where(User.email == "employee@example.com")
    )
    if not default_employee:
        default_employee = User(
            email="employee@example.com",
            hashed_password=hash_password("employee1234"),
            name="社員 花子",
            role="employee",
            status="active",
        )
        db.add(default_employee)

    has_item = db.scalar(select(Item.id).limit(1))
    if not has_item:
        db.flush()
        items = [
            Item(asset_number="PC-001", name="Surface 3", state="available"),
            Item(
                asset_number="PC-002",
                name="MacBook",
                state="lent",
                current_user_id=default_employee.id,
            ),
            Item(asset_number="MON-010", name="モニターC", state="available"),
        ]
        db.add_all(items)
        db.flush()
        db.add(LoanRecord(item_id=items[1].id, user_id=default_employee.id))

    db.commit()
