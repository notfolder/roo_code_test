from typing import Optional

from database import DatabaseManager


class AdminUserRepository:
    """管理者アカウントテーブルの照合を担うリポジトリ"""

    def __init__(self):
        self._db = DatabaseManager()

    def find_by_login_id(self, login_id: str) -> Optional[dict]:
        """ログインIDで管理者アカウントを取得する。存在しない場合はNoneを返す"""
        conn = self._db.get_connection()
        try:
            row = conn.execute(
                "SELECT id, login_id, password_hash, created_at FROM admin_users WHERE login_id = ?",
                (login_id,),
            ).fetchone()
            if row is None:
                return None
            return dict(row)
        finally:
            conn.close()
