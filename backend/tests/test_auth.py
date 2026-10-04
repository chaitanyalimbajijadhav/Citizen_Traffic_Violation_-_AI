from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_invalid_login():
    response = client.post(
        "/api/auth/login",
        json={"username": "missing", "password": "wrong123"},
    )
    assert response.status_code == 401
