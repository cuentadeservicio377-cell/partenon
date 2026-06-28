"""Tests for API authentication."""


import pytest


@pytest.fixture
def creds(monkeypatch):
    monkeypatch.setenv("DASHBOARD_APP_USERNAME", "admin")
    monkeypatch.setenv("DASHBOARD_APP_PASSWORD", "partenon")


def test_login_returns_token(api_client, creds):
    response = api_client.post("/api/v1/auth/token", json={
        "username": "admin",
        "password": "partenon",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_rejects_bad_credentials(api_client, creds):
    response = api_client.post("/api/v1/auth/token", json={
        "username": "admin",
        "password": "wrong",
    })
    assert response.status_code == 401


def test_protected_route_without_token(api_client):
    response = api_client.get("/api/v1/missions")
    assert response.status_code == 401


def test_protected_route_with_valid_token(api_client, auth_token):
    response = api_client.get("/api/v1/missions", headers={
        "Authorization": f"Bearer {auth_token}",
    })
    assert response.status_code == 200


def test_protected_route_with_expired_token(api_client, monkeypatch):
    monkeypatch.setenv("DASHBOARD_AUTH_SECRET", "test-secret-32-chars-long")
    import partenon_api.auth as auth

    original_ttl = auth.ACCESS_TOKEN_TTL_HOURS
    auth.ACCESS_TOKEN_TTL_HOURS = -1
    try:
        expired = auth.create_access_token("admin", "default")
    finally:
        auth.ACCESS_TOKEN_TTL_HOURS = original_ttl

    response = api_client.get("/api/v1/missions", headers={
        "Authorization": f"Bearer {expired}",
    })
    assert response.status_code == 401


def test_me_endpoint(api_client, auth_token):
    response = api_client.get("/api/v1/auth/me", headers={
        "Authorization": f"Bearer {auth_token}",
    })
    assert response.status_code == 200
    assert response.json()["username"] == "admin"
    assert response.json()["workspace_id"] == "default"
