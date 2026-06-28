"""Tests for cron job API endpoints."""

import pytest


@pytest.fixture
def cron_job(api_client, auth_token):
    response = api_client.post("/api/v1/cron", headers={
        "Authorization": f"Bearer {auth_token}",
    }, json={
        "profile": "partenon-scribe",
        "schedule": "0 9 * * *",
        "command": "python -m partenon.scribe report",
        "enabled": True,
        "note": "Test job",
    })
    assert response.status_code == 201
    return response.json()["cron"]


def test_list_cron_empty(api_client, auth_token):
    response = api_client.get("/api/v1/cron", headers={
        "Authorization": f"Bearer {auth_token}",
    })
    assert response.status_code == 200
    assert response.json()["cron"] == []


def test_create_cron_job(api_client, auth_token):
    response = api_client.post("/api/v1/cron", headers={
        "Authorization": f"Bearer {auth_token}",
    }, json={
        "profile": "partenon-guardian",
        "schedule": "0 2 * * 0",
        "command": "python -m partenon.guardian audit",
        "enabled": False,
    })
    assert response.status_code == 201
    data = response.json()["cron"]
    assert data["command"] == "python -m partenon.guardian audit"
    assert data["workspace_id"] == "default"


def test_toggle_cron_job(api_client, auth_token, cron_job):
    response = api_client.patch(f"/api/v1/cron/{cron_job['id']}", headers={
        "Authorization": f"Bearer {auth_token}",
    }, json={"enabled": False})
    assert response.status_code == 200
    assert response.json()["cron"]["enabled"] is False


def test_delete_cron_job(api_client, auth_token, cron_job):
    response = api_client.delete(f"/api/v1/cron/{cron_job['id']}", headers={
        "Authorization": f"Bearer {auth_token}",
    })
    assert response.status_code == 200
    assert response.json()["deleted"] is True
