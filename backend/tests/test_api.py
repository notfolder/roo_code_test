"""
FastAPI エンドポイントの結合テスト（TestClient使用）
設計書「12. テスト設計 - 結合テストケース一覧」に基づく
"""


# --- 認証API ---

class TestAuthLogin:
    def test_正常ログイン(self, client):
        """正しい認証情報でaccess_tokenが返ること"""
        resp = client.post(
            "/api/auth/login",
            json={"login_id": "admin", "password": "TestPass123"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"

    def test_認証失敗(self, client):
        """誤ったパスワードで401が返ること"""
        resp = client.post(
            "/api/auth/login",
            json={"login_id": "admin", "password": "WrongPass"},
        )
        assert resp.status_code == 401


# --- 備品API ---

class TestEquipmentGet:
    def test_未認証で備品一覧取得(self, client):
        """認証なしでGET /api/equipment が200を返すこと"""
        resp = client.get("/api/equipment")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)


class TestEquipmentPost:
    def test_認証済みで備品登録(self, client, auth_headers):
        """認証済みでPOST /api/equipment が201を返すこと"""
        resp = client.post(
            "/api/equipment",
            json={"management_number": "PC-001", "name": "ノートPC A", "equipment_type": "ノートPC"},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        assert resp.json()["management_number"] == "PC-001"

    def test_未認証で備品登録(self, client):
        """認証なしでPOST /api/equipment が401を返すこと"""
        resp = client.post(
            "/api/equipment",
            json={"management_number": "PC-001", "name": "ノートPC A", "equipment_type": "ノートPC"},
        )
        assert resp.status_code == 401

    def test_管理番号重複(self, client, auth_headers):
        """同じ管理番号を2回登録すると409が返ること"""
        payload = {"management_number": "PC-DUP", "name": "重複PC", "equipment_type": "ノートPC"}
        client.post("/api/equipment", json=payload, headers=auth_headers)
        resp = client.post("/api/equipment", json=payload, headers=auth_headers)
        assert resp.status_code == 409


class TestEquipmentDelete:
    def test_貸出中備品の削除(self, client, auth_headers):
        """貸出中の備品をDELETE すると409が返ること"""
        # 備品登録
        eq_resp = client.post(
            "/api/equipment",
            json={"management_number": "PC-L01", "name": "貸出中PC", "equipment_type": "ノートPC"},
            headers=auth_headers,
        )
        eq_id = eq_resp.json()["id"]
        # 貸出記録登録
        client.post(
            "/api/lending",
            json={"equipment_id": eq_id, "borrower_name": "山田太郎", "lent_at": "2026-04-01"},
            headers=auth_headers,
        )
        # 削除試行
        resp = client.delete(f"/api/equipment/{eq_id}", headers=auth_headers)
        assert resp.status_code == 409

    def test_利用可能な備品の削除(self, client, auth_headers):
        """status=available の備品をDELETE すると204が返ること"""
        eq_resp = client.post(
            "/api/equipment",
            json={"management_number": "PC-DEL", "name": "削除用PC", "equipment_type": "ノートPC"},
            headers=auth_headers,
        )
        eq_id = eq_resp.json()["id"]
        resp = client.delete(f"/api/equipment/{eq_id}", headers=auth_headers)
        assert resp.status_code == 204


# --- 貸出・返却API ---

class TestLendingPost:
    def _create_equipment(self, client, auth_headers, mgmt_no="PC-T01"):
        resp = client.post(
            "/api/equipment",
            json={"management_number": mgmt_no, "name": "テストPC", "equipment_type": "ノートPC"},
            headers=auth_headers,
        )
        return resp.json()["id"]

    def test_利用可能備品の貸出(self, client, auth_headers):
        """available な備品にPOST /api/lending すると201が返ること"""
        eq_id = self._create_equipment(client, auth_headers)
        resp = client.post(
            "/api/lending",
            json={"equipment_id": eq_id, "borrower_name": "鈴木花子", "lent_at": "2026-04-01"},
            headers=auth_headers,
        )
        assert resp.status_code == 201

    def test_貸出中備品の貸出(self, client, auth_headers):
        """lending な備品にPOST /api/lending すると409が返ること"""
        eq_id = self._create_equipment(client, auth_headers, "PC-T02")
        client.post(
            "/api/lending",
            json={"equipment_id": eq_id, "borrower_name": "田中一郎", "lent_at": "2026-04-01"},
            headers=auth_headers,
        )
        resp = client.post(
            "/api/lending",
            json={"equipment_id": eq_id, "borrower_name": "佐藤次郎", "lent_at": "2026-04-02"},
            headers=auth_headers,
        )
        assert resp.status_code == 409


class TestLendingReturn:
    def _setup_lending(self, client, auth_headers):
        """備品登録→貸出記録登録してrecord_idを返す"""
        eq_resp = client.post(
            "/api/equipment",
            json={"management_number": "PC-R01", "name": "返却テストPC", "equipment_type": "ノートPC"},
            headers=auth_headers,
        )
        eq_id = eq_resp.json()["id"]
        lending_resp = client.post(
            "/api/lending",
            json={"equipment_id": eq_id, "borrower_name": "山田太郎", "lent_at": "2026-04-01"},
            headers=auth_headers,
        )
        return lending_resp.json()["id"]

    def test_正常返却(self, client, auth_headers):
        """貸出中の記録にPUT /api/lending/{id}/return すると200が返ること"""
        record_id = self._setup_lending(client, auth_headers)
        resp = client.put(
            f"/api/lending/{record_id}/return",
            json={"returned_at": "2026-04-05"},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["returned_at"] == "2026-04-05"

    def test_返却済みへの再返却(self, client, auth_headers):
        """既に返却済みの記録に再度PUT すると409が返ること"""
        record_id = self._setup_lending(client, auth_headers)
        client.put(
            f"/api/lending/{record_id}/return",
            json={"returned_at": "2026-04-05"},
            headers=auth_headers,
        )
        resp = client.put(
            f"/api/lending/{record_id}/return",
            json={"returned_at": "2026-04-06"},
            headers=auth_headers,
        )
        assert resp.status_code == 409


class TestLendingHistory:
    def test_認証済みで履歴取得(self, client, auth_headers):
        """認証済みでGET /api/lending が200を返すこと"""
        resp = client.get("/api/lending", headers=auth_headers)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_未認証で履歴取得(self, client):
        """認証なしでGET /api/lending が401を返すこと"""
        resp = client.get("/api/lending")
        assert resp.status_code == 401
