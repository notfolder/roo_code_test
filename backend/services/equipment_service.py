from common.errors import ConflictError, NotFoundError
from repositories.equipment_repository import EquipmentRepository


class EquipmentService:
    """備品に関する業務ロジックを担うサービス"""

    def __init__(self):
        self._equipment_repo = EquipmentRepository()

    def get_all(self) -> list[dict]:
        """全備品一覧を返す"""
        return self._equipment_repo.find_all()

    def create(self, data: dict) -> dict:
        """バリデーション後に備品を登録する"""
        existing = self._equipment_repo.find_by_management_number(data["management_number"])
        if existing is not None:
            raise ConflictError("この管理番号はすでに登録されています")
        return self._equipment_repo.create(data)

    def update(self, equipment_id: int, data: dict) -> dict:
        """バリデーション後に備品を更新する"""
        existing = self._equipment_repo.find_by_id(equipment_id)
        if existing is None:
            raise NotFoundError("指定された備品が見つかりません")
        # 自分以外と管理番号が重複しないことを確認する
        dup = self._equipment_repo.find_by_management_number(data["management_number"])
        if dup is not None and dup["id"] != equipment_id:
            raise ConflictError("この管理番号はすでに登録されています")
        return self._equipment_repo.update(equipment_id, data)

    def delete(self, equipment_id: int) -> None:
        """貸出中チェック後に備品を削除する"""
        existing = self._equipment_repo.find_by_id(equipment_id)
        if existing is None:
            raise NotFoundError("指定された備品が見つかりません")
        if existing["status"] == "lending":
            raise ConflictError("貸出中の備品は削除できません")
        self._equipment_repo.delete(equipment_id)
