from app.database import engine, SessionLocal, Base
import app.models  # noqa: F401 – register all models before create_all


def create_tables():
    Base.metadata.create_all(bind=engine)


def create_initial_data():
    from app.models.user import User
    from app.dependencies import hash_password

    db = SessionLocal()
    try:
        if not db.query(User).filter(User.login_id == "admin").first():
            admin = User(
                login_id="admin",
                name="管理者",
                hashed_password=hash_password("admin1234"),
                role="admin",
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()
