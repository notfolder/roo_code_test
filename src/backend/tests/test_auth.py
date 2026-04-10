from fastapi.testclient import TestClient


def test_login_success(client: TestClient):
    response = client.post(
        "/api/auth/login", json={"email": "admin@example.com", "password": "admin1234"}
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["role"] == "admin"
    assert payload["access_token"]


def test_login_invalid_credentials(client: TestClient):
    response = client.post(
        "/api/auth/login", json={"email": "admin@example.com", "password": "wrong"}
    )
    assert response.status_code == 401
