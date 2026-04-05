import os
import sqlite3
from datetime import datetime, timezone

from passlib.context import CryptContext

# パスワードハッシュコンテキスト（bcrypt）
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class DatabaseManager:
    """SQLite接続管理クラス（シングルトン）"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db_path = os.environ.get(
                "DB_PATH", "/app/db/equipment.db"
            )
        return cls._instance

    def get_connection(self) -> sqlite3.Connection:
        """DBコネクションを返す。row_factoryでdict形式アクセスを有効にする"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    def init_db(self) -> None:
        """テーブル作成・初期管理者データ投入を行う（起動時に1回実行）"""
        conn = self.get_connection()
        try:
            with conn:
                # 備品マスタテーブル
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS equipments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        management_number TEXT NOT NULL UNIQUE,
                        name TEXT NOT NULL,
                        equipment_type TEXT NOT NULL,
                        status TEXT NOT NULL DEFAULT 'available',
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                    """
                )
                # 貸出記録テーブル
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS lending_records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        equipment_id INTEGER NOT NULL,
                        borrower_name TEXT NOT NULL,
                        lent_at TEXT NOT NULL,
                        returned_at TEXT,
                        created_at TEXT NOT NULL,
                        FOREIGN KEY (equipment_id) REFERENCES equipments(id)
                    )
                    """
                )
                # 管理者アカウントテーブル
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS admin_users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        login_id TEXT NOT NULL UNIQUE,
                        password_hash TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    )
                    """
                )

                # 初期管理者アカウント投入（レコードが0件の場合のみ）
                row = conn.execute(
                    "SELECT COUNT(*) as cnt FROM admin_users"
                ).fetchone()
                if row["cnt"] == 0:
                    login_id = os.environ.get("ADMIN_LOGIN_ID", "admin")
                    password = os.environ.get("ADMIN_PASSWORD", "AdminPass123")
                    password_hash = _pwd_context.hash(password)
                    now = datetime.now(timezone.utc).isoformat()
                    conn.execute(
                        "INSERT INTO admin_users (login_id, password_hash, created_at) VALUES (?, ?, ?)",
                        (login_id, password_hash, now),
                    )
        finally:
            conn.close()
