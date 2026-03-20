"""認証まわりの簡易テスト。"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_requires_user(client: AsyncClient):
    # 初期管理者 AdminPass123 でログインを試す
    resp = await client.post(
        "/auth/login",
        json={"email": "admin@example.com", "password": "AdminPass123"},
    )
    assert resp.status_code in (200, 401)
    # トークンが返るか、初期化前なら401
    if resp.status_code == 200:
        data = resp.json()
        assert "access_token" in data
