import sqlite3
from datetime import datetime, timezone
from typing import Optional

from database import DatabaseManager


class LendingRepository:
    """貸出記録テーブルのCRUD操作を担うリポジトリ"""

    def __init__(self):
        self._db = DatabaseManager()

    def find_all(self) -> list[dict]:
        """全貸出記録を取得する（備品情報を結合、降順）"""
        conn = self._db.get_connection()
        try:
            rows = conn.execute(
                """
                SELECT
                    lr.id,
                    lr.equipment_id,
                    e.management_number,
                    e.name,
                    lr.borrower_name,
                    lr.lent_at,
                    lr.returned_at,
                    lr.created_at
                FROM lending_records lr
                JOIN equipments e ON e.id = lr.equipment_id
                ORDER BY lr.id DESC
                """
            ).fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def find_active_by_equipment_id(self, equipment_id: int) -> Optional[dict]:
        """指定備品の貸出中レコードを取得する（returned_at が NULL のもの）"""
        conn = self._db.get_connection()
        try:
            row = conn.execute(
                """
                SELECT
                    lr.id,
                    lr.equipment_id,
                    e.management_number,
                    e.name,
                    lr.borrower_name,
                    lr.lent_at,
                    lr.returned_at,
                    lr.created_at
                FROM lending_records lr
                JOIN equipments e ON e.id = lr.equipment_id
                WHERE lr.equipment_id = ? AND lr.returned_at IS NULL
                """,
                (equipment_id,),
            ).fetchone()
            if row is None:
                return None
            return dict(row)
        finally:
            conn.close()

    def find_active_all(self) -> list[dict]:
        """全貸出中レコードを取得する（returned_at が NULL のもの）"""
        conn = self._db.get_connection()
        try:
            rows = conn.execute(
                """
                SELECT
                    lr.id,
                    lr.equipment_id,
                    e.management_number,
                    e.name,
                    lr.borrower_name,
                    lr.lent_at,
                    lr.returned_at,
                    lr.created_at
                FROM lending_records lr
                JOIN equipments e ON e.id = lr.equipment_id
                WHERE lr.returned_at IS NULL
                ORDER BY lr.id DESC
                """
            ).fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def find_by_id(self, record_id: int) -> Optional[dict]:
        """IDで貸出記録を取得する"""
        conn = self._db.get_connection()
        try:
            row = conn.execute(
                """
                SELECT
                    lr.id,
                    lr.equipment_id,
                    e.management_number,
                    e.name,
                    lr.borrower_name,
                    lr.lent_at,
                    lr.returned_at,
                    lr.created_at
                FROM lending_records lr
                JOIN equipments e ON e.id = lr.equipment_id
                WHERE lr.id = ?
                """,
                (record_id,),
            ).fetchone()
            if row is None:
                return None
            return dict(row)
        finally:
            conn.close()

    def create(self, data: dict, conn: sqlite3.Connection) -> dict:
        """貸出記録を登録し、登録した記録を返す（トランザクション内で使用する）"""
        now = datetime.now(timezone.utc).isoformat()
        cursor = conn.execute(
            """
            INSERT INTO lending_records (equipment_id, borrower_name, lent_at, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (data["equipment_id"], data["borrower_name"], data["lent_at"], now),
        )
        return {"id": cursor.lastrowid, **data, "returned_at": None, "created_at": now}

    def set_returned(self, record_id: int, returned_at: str, conn: sqlite3.Connection) -> None:
        """返却日をセットする（トランザクション内で使用する）"""
        conn.execute(
            "UPDATE lending_records SET returned_at = ? WHERE id = ?",
            (returned_at, record_id),
        )
