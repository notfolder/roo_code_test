from fastapi.testclient import TestClient


def test_users_forbidden_for_employee(client: TestClient, employee_token: str):
    response = client.get(
        "/api/users", headers={"Authorization": f"Bearer {employee_token}"}
    )
    assert response.status_code == 403


def test_user_crud(client: TestClient, admin_token: str):
    create_response = client.post(
        "/api/users",
        json={
            "email": "new-user@example.com",
            "name": "New User",
            "password": "password1234",
            "role": "employee",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert create_response.status_code == 200
    user_id = create_response.json()["id"]

    detail_response = client.get(
        f"/api/users/{user_id}", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert detail_response.status_code == 200

    update_response = client.put(
        f"/api/users/{user_id}",
        json={
            "email": "updated-user@example.com",
            "name": "Updated User",
            "role": "admin",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["role"] == "admin"

    delete_response = client.delete(
        f"/api/users/{user_id}", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert delete_response.status_code == 200
    assert delete_response.json()["status"] == "deleted"
