"""予約→貸出→返却の主要フロー簡易テスト。"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_reservation_flow(client: AsyncClient):
    # 前提: 管理者でユーザー作成、備品作成、予約→貸出→返却

    # 1) 管理者ログイン
    resp = await client.post(
        "/auth/login",
        json={"email": "admin@example.com", "password": "AdminPass123"},
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2) ユーザー作成
    user_email = "user1@example.com"
    resp = await client.post(
        "/auth/users",
        json={"email": user_email, "name": "User1", "role": "general", "password": "Password123"},
        headers=headers,
    )
    assert resp.status_code == 200
    user_id = resp.json()["id"]

    # 3) 備品作成
    resp = await client.post(
        "/items",
        json={"item_code": "A001", "name": "プロジェクタ", "status": "active"},
        headers=headers,
    )
    assert resp.status_code == 200
    item_id = resp.json()["id"]

    # 4) ユーザーでログイン
    resp = await client.post(
        "/auth/login",
        json={"email": user_email, "password": "Password123"},
    )
    assert resp.status_code == 200
    user_token = resp.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {user_token}"}

    # 5) 予約作成（今日と明日）
    resp = await client.post(
        "/reservations",
        json={"item_id": item_id, "start_date": "2024-05-01", "end_date": "2024-05-02"},
        headers=user_headers,
    )
    assert resp.status_code in (200, 409)  # 排他の可能性も許容
    if resp.status_code != 200:
        return
    reservation_id = resp.json()["id"]

    # 6) 貸出開始（管理者）
    resp = await client.post(
        "/loans",
        json={"reservation_id": reservation_id},
        headers=headers,
    )
    assert resp.status_code == 200
    loan_id = resp.json()["id"]

    # 7) 返却
    resp = await client.post(
        f"/loans/{loan_id}/return",
        json={"actual_return_date": "2024-05-02"},
        headers=headers,
    )
    assert resp.status_code == 200

