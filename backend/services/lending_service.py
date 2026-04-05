from common.errors import ConflictError, NotFoundError
from database import DatabaseManager
from repositories.equipment_repository import EquipmentRepository
from repositories.lending_repository import LendingRepository


class LendingService:
    """貸出・返却に関する業務ロジックを担うサービス"""

    def __init__(self):
        self._lending_repo = LendingRepository()
        self._equipment_repo = EquipmentRepository()
        self._db = DatabaseManager()

    def get_history(self) -> list[dict]:
        """全貸出履歴を返す"""
        return self._lending_repo.find_all()

    def get_active(self) -> list[dict]:
        """全貸出中レコードを返す"""
        return self._lending_repo.find_active_all()

    def lend(self, data: dict) -> dict:
        """貸出可能チェック後にトランザクションで貸出記録を登録し、備品ステータスを更新する"""
        equipment = self._equipment_repo.find_by_id(data["equipment_id"])
        if equipment is None:
            raise NotFoundError("指定された備品が見つかりません")
        if equipment["status"] != "available":
            raise ConflictError("この備品はすでに貸出中です")

        conn = self._db.get_connection()
        try:
            with conn:
                record = self._lending_repo.create(data, conn)
                self._equipment_repo.update_status(data["equipment_id"], "lending", conn)
        finally:
            conn.close()

        # 備品情報を結合した完全なレコードを返す
        return self._lending_repo.find_by_id(record["id"])

    def return_item(self, record_id: int, returned_at: str) -> dict:
        """返却済みチェック後にトランザクションで返却記録を登録し、備品ステータスを更新する"""
        record = self._lending_repo.find_by_id(record_id)
        if record is None:
            raise NotFoundError("指定された貸出記録が見つかりません")
        if record["returned_at"] is not None:
            raise ConflictError("この貸出記録はすでに返却済みです")
        # 返却日が貸出日以降であることを確認する
        if returned_at < record["lent_at"]:
            raise ConflictError("返却日は貸出日以降の日付を指定してください")

        conn = self._db.get_connection()
        try:
            with conn:
                self._lending_repo.set_returned(record_id, returned_at, conn)
                self._equipment_repo.update_status(record["equipment_id"], "available", conn)
        finally:
            conn.close()

        return self._lending_repo.find_by_id(record_id)
