"""Tests for the gateway dry-run API endpoint."""

import pytest


@pytest.fixture
def gateway_token(auth_token):
    return auth_token


def test_gateway_dry_run_command_only(api_client, gateway_token):
    response = api_client.post("/api/v1/gateway/dry_run", headers={
        "Authorization": f"Bearer {gateway_token}",
    }, json={
        "message": "/scribe review June expenses",
        "user_id": "user_123",
        "chat_id": "chat_456",
        "is_group": False,
        "bot_username": "partenon_bot",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["command"]["profile"] == "partenon-scribe"
    assert data["command"]["action"] == "review"
    assert data["command"]["args"] == ["June", "expenses"]


def test_gateway_dry_run_with_alias(api_client, gateway_token):
    response = api_client.post("/api/v1/gateway/dry_run", headers={
        "Authorization": f"Bearer {gateway_token}",
    }, json={
        "message": "/c status",
        "user_id": "user_123",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["command"]["profile"] == "partenon-collector"
    assert data["command"]["action"] == "status"


def test_gateway_dry_run_fallback_intent(api_client, gateway_token):
    response = api_client.post("/api/v1/gateway/dry_run", headers={
        "Authorization": f"Bearer {gateway_token}",
    }, json={
        "message": "Organize my numbers",
        "user_id": "user_123",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["command"]["profile"] == "partenon-scribe"
    assert data["command"]["prefix_used"] is False


def test_gateway_dry_run_attachment(api_client, gateway_token):
    response = api_client.post("/api/v1/gateway/dry_run", headers={
        "Authorization": f"Bearer {gateway_token}",
    }, json={
        "message": "/scribe review expenses",
        "user_id": "user_123",
        "file_name": "june_expenses.csv",
        "mime_type": "text/csv",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["attachment"]["profile"] == "partenon-scribe"


def test_gateway_dry_run_guard_denies_unknown_user(api_client, gateway_token, monkeypatch):
    monkeypatch.setenv("GATEWAY_ALLOWED_USERS", "12345")
    response = api_client.post("/api/v1/gateway/dry_run", headers={
        "Authorization": f"Bearer {gateway_token}",
    }, json={
        "message": "/status",
        "user_id": "99999",
    })
    assert response.status_code == 200
    assert response.json()["guard"]["allowed"] is False


def test_gateway_dry_run_guard_allows_known_user(api_client, gateway_token, monkeypatch):
    monkeypatch.setenv("GATEWAY_ALLOWED_USERS", "user_123")
    response = api_client.post("/api/v1/gateway/dry_run", headers={
        "Authorization": f"Bearer {gateway_token}",
    }, json={
        "message": "/status",
        "user_id": "user_123",
    })
    assert response.status_code == 200
    assert response.json()["guard"]["allowed"] is True
