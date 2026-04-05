"""
テスト共通フィクスチャ定義
"""
import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def setup_test_db(tmp_path):
    """各テストで独立したSQLiteデータベースを使用する。
    モジュールキャッシュによりルーターのサービス/リポジトリインスタンスが保持する
    DatabaseManager参照は同一オブジェクトのままにし、db_pathのみ更新する。
    """
    db_file = str(tmp_path / "test.db")
    os.environ["DB_PATH"] = db_file
    os.environ["JWT_SECRET_KEY"] = "test-secret-key-for-testing"
    os.environ["ADMIN_LOGIN_ID"] = "admin"
    os.environ["ADMIN_PASSWORD"] = "TestPass123"

    from database import DatabaseManager

    # 既存シングルトンがある場合はdb_pathだけ更新してすべての参照先に反映する
    if DatabaseManager._instance is None:
        DatabaseManager._instance = None
        manager = DatabaseManager()
    else:
        manager = DatabaseManager._instance
        manager.db_path = db_file

    manager.init_db()
    yield manager


@pytest.fixture
def client(setup_test_db):
    """FastAPI TestClientフィクスチャ"""
    from main import app

    with TestClient(app) as c:
        yield c


@pytest.fixture
def auth_token(client):
    """認証済みJWTトークンを取得するフィクスチャ"""
    resp = client.post(
        "/api/auth/login",
        json={"login_id": "admin", "password": "TestPass123"},
    )
    return resp.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    """認証ヘッダーフィクスチャ"""
    return {"Authorization": f"Bearer {auth_token}"}
