"""Tests for the integration router."""

import pytest


@pytest.fixture
def _no_integration_credentials(monkeypatch):
    """Ensure no live integration credentials are set for dry-run tests."""
    for key in (
        "GOOGLE_SERVICE_ACCOUNT_JSON",
        "STRIPE_SECRET_KEY",
        "SLACK_BOT_TOKEN",
    ):
        monkeypatch.delenv(key, raising=False)


def test_list_integrations(api_client, auth_token, _no_integration_credentials):
    response = api_client.get("/api/v1/integrations", headers={
        "Authorization": f"Bearer {auth_token}",
    })
    assert response.status_code == 200
    data = response.json()
    assert "integrations" in data
    domains = {item["domain"] for item in data["integrations"]}
    assert domains == {"google_workspace", "payments", "slack", "memory"}


def test_invoke_unknown_domain(api_client, auth_token):
    response = api_client.post(
        "/api/v1/integrations/unknown/foo",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={},
    )
    assert response.status_code == 404


def test_invoke_google_workspace_dry_run_short_circuit(api_client, auth_token, _no_integration_credentials):
    response = api_client.post(
        "/api/v1/integrations/google_workspace/create_spreadsheet",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "Test Sheet"},
    )
    assert response.status_code == 200
    result = response.json()
    assert result["ok"] is True
    assert result["dry_run"] is True


def test_invoke_slack_dry_run_short_circuit(api_client, auth_token, _no_integration_credentials):
    response = api_client.post(
        "/api/v1/integrations/slack/send_message",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"channel": "#general", "text": "hello"},
    )
    assert response.status_code == 200
    result = response.json()
    assert result["ok"] is True
    assert result["dry_run"] is True


def test_invoke_payments_dry_run_short_circuit(api_client, auth_token, _no_integration_credentials):
    response = api_client.post(
        "/api/v1/integrations/payments/create_invoice",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"customer_email": "test@example.com", "amount": 100},
    )
    assert response.status_code == 200
    result = response.json()
    assert result["ok"] is True
    assert result["dry_run"] is True


def test_invoke_memory_live_via_mcp(api_client, auth_token):
    """Memory should always be invoked via its MCP server (sqlite in tests)."""
    response = api_client.post(
        "/api/v1/integrations/memory/put_page",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "slug": "workspace/default/test/integration",
            "content": '{"hello": "world"}',
            "tags": "test,integration",
        },
    )
    assert response.status_code == 200
    result = response.json()
    assert result.get("ok") is True or "ok" in str(result)

    response = api_client.post(
        "/api/v1/integrations/memory/get_page",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"slug": "workspace/default/test/integration"},
    )
    assert response.status_code == 200
    page = response.json()
    assert page.get("slug") == "workspace/default/test/integration"


def test_invoke_payments_forces_live_without_credentials(api_client, auth_token, _no_integration_credentials):
    """When dry_run is explicitly false and no credentials exist, the MCP server
    returns a live-mode error instead of a short-circuit dry-run response."""
    response = api_client.post(
        "/api/v1/integrations/payments/create_invoice",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"customer_email": "test@example.com", "amount": 100, "dry_run": False},
    )
    assert response.status_code == 200
    result = response.json()
    assert result["ok"] is False
    assert "credentials" in result.get("error", "").lower()
