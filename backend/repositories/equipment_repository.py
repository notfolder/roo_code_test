import sqlite3
from datetime import datetime, timezone
from typing import Optional

from database import DatabaseManager


class EquipmentRepository:
    """備品テーブルのCRUD操作を担うリポジトリ"""

    def __init__(self):
        self._db = DatabaseManager()

    def find_all(self) -> list[dict]:
        """全備品を取得する。貸出中の場合は借用者名も結合して返す"""
        conn = self._db.get_connection()
        try:
            rows = conn.execute(
                """
                SELECT
                    e.id,
                    e.management_number,
                    e.name,
                    e.equipment_type,
                    e.status,
                    e.created_at,
                    e.updated_at,
                    lr.borrower_name
                FROM equipments e
                LEFT JOIN lending_records lr
                    ON lr.equipment_id = e.id AND lr.returned_at IS NULL
                ORDER BY e.id
                """
            ).fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def find_by_id(self, equipment_id: int) -> Optional[dict]:
        """IDで備品を取得する。存在しない場合はNoneを返す"""
        conn = self._db.get_connection()
        try:
            row = conn.execute(
                """
                SELECT
                    e.id,
                    e.management_number,
                    e.name,
                    e.equipment_type,
                    e.status,
                    e.created_at,
                    e.updated_at,
                    lr.borrower_name
                FROM equipments e
                LEFT JOIN lending_records lr
                    ON lr.equipment_id = e.id AND lr.returned_at IS NULL
                WHERE e.id = ?
                """,
                (equipment_id,),
            ).fetchone()
            if row is None:
                return None
            return dict(row)
        finally:
            conn.close()

    def find_by_management_number(self, management_number: str) -> Optional[dict]:
        """管理番号で備品を取得する。存在しない場合はNoneを返す"""
        conn = self._db.get_connection()
        try:
            row = conn.execute(
                "SELECT id, management_number, name, equipment_type, status FROM equipments WHERE management_number = ?",
                (management_number,),
            ).fetchone()
            if row is None:
                return None
            return dict(row)
        finally:
            conn.close()

    def create(self, data: dict) -> dict:
        """備品を登録し、登録した備品を返す"""
        now = datetime.now(timezone.utc).isoformat()
        conn = self._db.get_connection()
        try:
            with conn:
                cursor = conn.execute(
                    """
                    INSERT INTO equipments (management_number, name, equipment_type, status, created_at, updated_at)
                    VALUES (?, ?, ?, 'available', ?, ?)
                    """,
                    (data["management_number"], data["name"], data["equipment_type"], now, now),
                )
                new_id = cursor.lastrowid
            # with conn: を抜けてコミット後に読み取ることで、別接続から確実に参照できる
            return self.find_by_id(new_id)
        finally:
            conn.close()

    def update(self, equipment_id: int, data: dict) -> Optional[dict]:
        """備品を更新し、更新後の備品を返す"""
        now = datetime.now(timezone.utc).isoformat()
        conn = self._db.get_connection()
        try:
            with conn:
                conn.execute(
                    """
                    UPDATE equipments
                    SET management_number = ?, name = ?, equipment_type = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (data["management_number"], data["name"], data["equipment_type"], now, equipment_id),
                )
            return self.find_by_id(equipment_id)
        finally:
            conn.close()

    def delete(self, equipment_id: int) -> None:
        """備品を削除する"""
        conn = self._db.get_connection()
        try:
            with conn:
                conn.execute("DELETE FROM equipments WHERE id = ?", (equipment_id,))
        finally:
            conn.close()

    def update_status(self, equipment_id: int, status: str, conn: sqlite3.Connection) -> None:
        """備品ステータスを更新する（トランザクション内で使用する）"""
        now = datetime.now(timezone.utc).isoformat()
        conn.execute(
            "UPDATE equipments SET status = ?, updated_at = ? WHERE id = ?",
            (status, now, equipment_id),
        )
