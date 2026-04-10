from fastapi.testclient import TestClient


def test_list_items(client: TestClient, employee_token: str):
    response = client.get(
        "/api/items", headers={"Authorization": f"Bearer {employee_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_create_item_admin_only(client: TestClient, employee_token: str):
    response = client.post(
        "/api/items",
        json={"asset_number": "NEW-001", "name": "New Device", "state": "available"},
        headers={"Authorization": f"Bearer {employee_token}"},
    )
    assert response.status_code == 403


def test_create_item_success(client: TestClient, admin_token: str):
    response = client.post(
        "/api/items",
        json={"asset_number": "NEW-001", "name": "New Device", "state": "available"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json()["asset_number"] == "NEW-001"


def test_lend_and_return_item(client: TestClient, admin_token: str):
    items = client.get(
        "/api/items", headers={"Authorization": f"Bearer {admin_token}"}
    ).json()
    available_item = next(i for i in items if i["state"] == "available")

    users = client.get(
        "/api/users", headers={"Authorization": f"Bearer {admin_token}"}
    ).json()
    employee = next(
        u for u in users if u["role"] == "employee" and u["status"] == "active"
    )

    lend_response = client.post(
        f"/api/items/{available_item['id']}/loan",
        json={"user_id": employee["id"]},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert lend_response.status_code == 200

    conflict_response = client.post(
        f"/api/items/{available_item['id']}/loan",
        json={"user_id": employee["id"]},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert conflict_response.status_code == 409

    return_response = client.post(
        f"/api/items/{available_item['id']}/return",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert return_response.status_code == 200
