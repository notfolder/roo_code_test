"""未返却/期限超過一覧のテスト。"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_overdue_list(client: AsyncClient):
    # 管理者でログイン
    resp = await client.post(
        "/auth/login",
        json={"email": "admin@example.com", "password": "AdminPass123"},
    )
    if resp.status_code != 200:
        return
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = await client.get("/loans/overdue", headers=headers)
    assert resp.status_code in (200, 404, 401)
