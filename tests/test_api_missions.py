"""Tests for mission API endpoints."""

import pytest


@pytest.fixture
def mission(api_client, auth_token):
    response = api_client.post("/api/v1/missions", headers={
        "Authorization": f"Bearer {auth_token}",
    }, json={
        "profile": "partenon-scribe",
        "title": "Test mission",
        "status": "backlog",
        "priority": "high",
        "description": "Test description",
    })
    assert response.status_code == 201
    return response.json()["mission"]


def test_list_missions_empty(api_client, auth_token):
    response = api_client.get("/api/v1/missions", headers={
        "Authorization": f"Bearer {auth_token}",
    })
    assert response.status_code == 200
    assert response.json()["missions"] == []


def test_create_mission(api_client, auth_token):
    response = api_client.post("/api/v1/missions", headers={
        "Authorization": f"Bearer {auth_token}",
    }, json={
        "profile": "partenon-herald",
        "title": "Content calendar",
        "status": "ideas",
        "priority": "medium",
        "description": "Plan content",
    })
    assert response.status_code == 201
    data = response.json()["mission"]
    assert data["title"] == "Content calendar"
    assert data["workspace_id"] == "default"


def test_update_mission_status(api_client, auth_token, mission):
    response = api_client.patch(f"/api/v1/missions/{mission['id']}", headers={
        "Authorization": f"Bearer {auth_token}",
    }, json={"status": "in_progress"})
    assert response.status_code == 200
    assert response.json()["mission"]["status"] == "in_progress"


def test_delete_mission(api_client, auth_token, mission):
    response = api_client.delete(f"/api/v1/missions/{mission['id']}", headers={
        "Authorization": f"Bearer {auth_token}",
    })
    assert response.status_code == 200
    assert response.json()["deleted"] is True

    response = api_client.get("/api/v1/missions", headers={
        "Authorization": f"Bearer {auth_token}",
    })
    assert len(response.json()["missions"]) == 0


def test_workspace_isolation(api_client, auth_token):
    from partenon_api.auth import create_access_token

    other_token = create_access_token("admin", "other")

    api_client.post("/api/v1/missions", headers={
        "Authorization": f"Bearer {auth_token}",
    }, json={
        "profile": "partenon-scribe",
        "title": "Default mission",
        "status": "backlog",
        "priority": "low",
        "description": "",
    })

    response = api_client.get("/api/v1/missions", headers={
        "Authorization": f"Bearer {other_token}",
    })
    assert response.status_code == 200
    assert len(response.json()["missions"]) == 0


def test_mission_not_found_in_other_workspace(api_client, auth_token):
    from partenon_api.auth import create_access_token

    other_token = create_access_token("admin", "other")
    response = api_client.patch("/api/v1/missions/mission-does-not-exist", headers={
        "Authorization": f"Bearer {other_token}",
    }, json={"status": "done"})
    assert response.status_code == 404
