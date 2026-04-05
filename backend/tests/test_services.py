"""
サービス層の単体テスト
設計書「12. テスト設計 - 単体テストケース一覧」に基づく
"""
import pytest

from common.auth import create_access_token, decode_token
from common.errors import ConflictError, NotFoundError, UnauthorizedError
from services.auth_service import AuthService
from services.equipment_service import EquipmentService
from services.lending_service import LendingService


# --- EquipmentService ---

class TestEquipmentServiceCreate:
    def test_正常な備品登録(self):
        """管理番号・備品名・種別を指定して備品を登録できること"""
        svc = EquipmentService()
        data = {"management_number": "PC-001", "name": "ノートPC A", "equipment_type": "ノートPC"}
        result = svc.create(data)
        assert result["management_number"] == "PC-001"
        assert result["status"] == "available"

    def test_管理番号重複登録(self):
        """同じ管理番号を2回登録するとConflictErrorが発生すること"""
        svc = EquipmentService()
        data = {"management_number": "PC-001", "name": "ノートPC A", "equipment_type": "ノートPC"}
        svc.create(data)
        with pytest.raises(ConflictError):
            svc.create(data)


class TestEquipmentServiceDelete:
    def test_利用可能な備品の削除(self):
        """status=available の備品は削除できること"""
        svc = EquipmentService()
        eq = svc.create({"management_number": "PC-002", "name": "ノートPC B", "equipment_type": "ノートPC"})
        svc.delete(eq["id"])
        assert svc.get_all() == []

    def test_貸出中備品の削除(self):
        """status=lending の備品を削除しようとするとConflictErrorが発生すること"""
        eq_svc = EquipmentService()
        lending_svc = LendingService()
        eq = eq_svc.create({"management_number": "PC-003", "name": "ノートPC C", "equipment_type": "ノートPC"})
        lending_svc.lend(
            {"equipment_id": eq["id"], "borrower_name": "山田太郎", "lent_at": "2026-04-01"}
        )
        with pytest.raises(ConflictError):
            eq_svc.delete(eq["id"])

    def test_存在しない備品の削除(self):
        """存在しないIDを指定するとNotFoundErrorが発生すること"""
        svc = EquipmentService()
        with pytest.raises(NotFoundError):
            svc.delete(9999)


# --- LendingService ---

class TestLendingServiceLend:
    def test_利用可能な備品への貸出(self):
        """status=available の備品に貸出記録を登録できること"""
        eq_svc = EquipmentService()
        lending_svc = LendingService()
        eq = eq_svc.create({"management_number": "PC-010", "name": "ノートPC X", "equipment_type": "ノートPC"})
        record = lending_svc.lend(
            {"equipment_id": eq["id"], "borrower_name": "鈴木花子", "lent_at": "2026-04-01"}
        )
        assert record["borrower_name"] == "鈴木花子"
        # 備品のステータスが lending に変わること
        updated = eq_svc.get_all()
        eq_updated = next(e for e in updated if e["id"] == eq["id"])
        assert eq_updated["status"] == "lending"

    def test_貸出中備品への貸出(self):
        """既に貸出中の備品に貸出しようとするとConflictErrorが発生すること"""
        eq_svc = EquipmentService()
        lending_svc = LendingService()
        eq = eq_svc.create({"management_number": "PC-011", "name": "ノートPC Y", "equipment_type": "ノートPC"})
        lending_svc.lend(
            {"equipment_id": eq["id"], "borrower_name": "田中一郎", "lent_at": "2026-04-01"}
        )
        with pytest.raises(ConflictError):
            lending_svc.lend(
                {"equipment_id": eq["id"], "borrower_name": "佐藤次郎", "lent_at": "2026-04-02"}
            )

    def test_存在しない備品への貸出(self):
        """存在しないequipment_idを指定するとNotFoundErrorが発生すること"""
        lending_svc = LendingService()
        with pytest.raises(NotFoundError):
            lending_svc.lend(
                {"equipment_id": 9999, "borrower_name": "山田", "lent_at": "2026-04-01"}
            )


class TestLendingServiceReturnItem:
    def test_貸出中の返却(self):
        """貸出中の記録に返却日を登録できること"""
        eq_svc = EquipmentService()
        lending_svc = LendingService()
        eq = eq_svc.create({"management_number": "PC-020", "name": "ノートPC Z", "equipment_type": "ノートPC"})
        record = lending_svc.lend(
            {"equipment_id": eq["id"], "borrower_name": "山田太郎", "lent_at": "2026-04-01"}
        )
        returned = lending_svc.return_item(record["id"], "2026-04-05")
        assert returned["returned_at"] == "2026-04-05"
        # 備品のステータスが available に戻ること
        updated = eq_svc.get_all()
        eq_updated = next(e for e in updated if e["id"] == eq["id"])
        assert eq_updated["status"] == "available"

    def test_既に返却済みの再返却(self):
        """returned_at が設定済みの記録に再返却するとConflictErrorが発生すること"""
        eq_svc = EquipmentService()
        lending_svc = LendingService()
        eq = eq_svc.create({"management_number": "PC-021", "name": "ノートPC W", "equipment_type": "ノートPC"})
        record = lending_svc.lend(
            {"equipment_id": eq["id"], "borrower_name": "山田太郎", "lent_at": "2026-04-01"}
        )
        lending_svc.return_item(record["id"], "2026-04-05")
        with pytest.raises(ConflictError):
            lending_svc.return_item(record["id"], "2026-04-06")

    def test_存在しない貸出記録の返却(self):
        """存在しないIDを指定するとNotFoundErrorが発生すること"""
        lending_svc = LendingService()
        with pytest.raises(NotFoundError):
            lending_svc.return_item(9999, "2026-04-05")


# --- AuthService ---

class TestAuthServiceLogin:
    def test_正しいIDとパスワードでログイン(self):
        """正しい認証情報でJWTトークンが返ること"""
        svc = AuthService()
        token = svc.login("admin", "TestPass123")
        assert isinstance(token, str)
        assert len(token) > 0

    def test_誤ったパスワードでログイン(self):
        """パスワードが誤っているとUnauthorizedErrorが発生すること"""
        svc = AuthService()
        with pytest.raises(UnauthorizedError):
            svc.login("admin", "WrongPassword")

    def test_存在しないIDでログイン(self):
        """存在しないlogin_idを指定するとUnauthorizedErrorが発生すること"""
        svc = AuthService()
        with pytest.raises(UnauthorizedError):
            svc.login("no_such_user", "TestPass123")


# --- JWTトークン検証（common/auth.py の decode_token） ---

class TestDecodeToken:
    def test_有効なJWTを検証(self):
        """有効なJWTトークンはペイロードを返すこと"""
        token = create_access_token({"sub": "admin"})
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "admin"

    def test_無効なJWTを検証(self):
        """不正なトークン文字列はNoneを返すこと"""
        result = decode_token("invalid.token.string")
        assert result is None

    def test_期限切れJWTを検証(self):
        """期限切れのJWTはNoneを返すこと"""
        import os
        from datetime import datetime, timedelta, timezone

        from jose import jwt

        secret = os.environ.get("JWT_SECRET_KEY", "change-me-in-production")
        expired_payload = {
            "sub": "admin",
            "exp": datetime.now(timezone.utc) - timedelta(hours=1),
        }
        expired_token = jwt.encode(expired_payload, secret, algorithm="HS256")
        result = decode_token(expired_token)
        assert result is None
