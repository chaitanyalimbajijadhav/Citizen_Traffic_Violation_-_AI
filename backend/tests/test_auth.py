import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from jose import jwt

from app.core.config import settings
from app.core.security import hash_password, verify_password
from app.db.database import Base, get_db
from app.main import app
from app.models.user import User


@pytest.fixture
def auth_session_factory():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    yield session_factory
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def client(auth_session_factory):
    previous_override = app.dependency_overrides.get(get_db)

    def override_get_db():
        db = auth_session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        if previous_override is None:
            app.dependency_overrides.pop(get_db, None)
        else:
            app.dependency_overrides[get_db] = previous_override


def test_invalid_login(client):
    response = client.post(
        "/api/auth/login",
        json={"username": "missing", "password": "wrong123"},
    )
    assert response.status_code == 401


def test_register_persists_hashed_password_and_login_succeeds(
    client,
    auth_session_factory,
):
    password = "Citizen@123"
    response = client.post(
        "/api/auth/register",
        json={
            "name": "  New Citizen  ",
            "email": "New.Citizen@example.com",
            "password": password,
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "New Citizen",
        "email": "new.citizen@example.com",
        "role": "CITIZEN",
    }
    assert "password" not in response.json()
    assert "password_hash" not in response.json()

    with auth_session_factory() as db:
        user = db.query(User).filter_by(username="new.citizen@example.com").one()
        assert user.password_hash != password
        assert verify_password(password, user.password_hash)

    login_response = client.post(
        "/api/auth/login",
        json={
            "username": "NEW.CITIZEN@example.com",
            "password": password,
        },
    )
    assert login_response.status_code == 200
    assert login_response.json()["token_type"] == "bearer"
    assert login_response.json()["access_token"]
    token_payload = jwt.decode(
        login_response.json()["access_token"],
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )
    assert token_payload["sub"] == "1"

    invalid_password_login = client.post(
        "/api/auth/login",
        json={
            "username": "new.citizen@example.com",
            "password": "Incorrect@123",
        },
    )
    assert invalid_password_login.status_code == 401


def test_login_accepts_existing_username_case_sensitively(
    client,
    auth_session_factory,
):
    with auth_session_factory() as db:
        db.add(
            User(
                name="Legacy Citizen",
                username="citizen01",
                password_hash=hash_password("Citizen@123"),
                role="CITIZEN",
                status="ACTIVE",
            )
        )
        db.commit()

    response = client.post(
        "/api/auth/login",
        json={"username": "citizen01", "password": "Citizen@123"},
    )
    assert response.status_code == 200


def test_web_login_cors_preflight(client):
    response = client.options(
        "/api/auth/login",
        headers={
            "Origin": "http://127.0.0.1:8080",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:8080"
    assert "POST" in response.headers["access-control-allow-methods"]


def test_duplicate_registration_is_rejected_case_insensitively(client):
    request = {
        "name": "New Citizen",
        "email": "new.citizen@example.com",
        "password": "Citizen@123",
    }
    assert client.post("/api/auth/register", json=request).status_code == 201

    duplicate = client.post(
        "/api/auth/register",
        json={**request, "email": "NEW.CITIZEN@example.com"},
    )
    assert duplicate.status_code == 409
    assert duplicate.json()["detail"] == "An account with this email already exists"


@pytest.mark.parametrize(
    "payload",
    [
        {"email": "citizen@example.com", "password": "Citizen@123"},
        {"name": "   ", "email": "citizen@example.com", "password": "Citizen@123"},
        {"name": "Citizen", "email": "not-an-email", "password": "Citizen@123"},
        {"name": "Citizen", "email": "citizen@example.com", "password": "short"},
    ],
)
def test_registration_rejects_invalid_fields(client, payload):
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 422
