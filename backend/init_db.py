"""DBスキーマ作成・初期ユーザー投入"""
import sys
import time
from sqlalchemy.exc import OperationalError
from database import engine, SessionLocal, Base
import models  # noqa: F401 - モデルをインポートしてBaseに登録する
from utils.password_util import PasswordUtil


def wait_for_db(max_retries: int = 10) -> None:
    """DBが起動するまでリトライする"""
    for i in range(max_retries):
        try:
            with engine.connect():
                print("DB接続成功")
                return
        except OperationalError:
            print(f"DB接続待機中... ({i + 1}/{max_retries})")
            time.sleep(2)
    print("DBへの接続に失敗しました")
    sys.exit(1)


def init_db() -> None:
    """スキーマ作成と初期ユーザー投入"""
    # テーブル作成
    Base.metadata.create_all(bind=engine)
    print("テーブル作成完了")

    # 初期ユーザー投入（既存の場合はスキップ）
    db = SessionLocal()
    try:
        from models.user import User
        existing = db.query(User).filter(User.login_id == "admin").first()
        if existing is None:
            admin = User(
                login_id="admin",
                username="管理者",
                password_hash=PasswordUtil.hash("admin"),
                role="admin",
            )
            db.add(admin)
            db.commit()
            print("初期ユーザー（admin）を作成しました")
        else:
            print("初期ユーザーは既に存在します")
    finally:
        db.close()


if __name__ == "__main__":
    wait_for_db()
    init_db()
