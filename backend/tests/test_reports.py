from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_report_requires_auth():
    response = client.post(
        "/api/reports",
        json={
            "description": "No helmet",
            "latitude": 17.65,
            "longitude": 75.90,
        },
    )
    assert response.status_code in (401, 403)


def test_invalid_location():
    response = client.post(
        "/api/reports",
        json={
            "description": "No helmet",
            "latitude": 200,
            "longitude": 75.90,
        },
    )
    assert response.status_code == 422
