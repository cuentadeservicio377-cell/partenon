"""Tests for workflow event API endpoints."""


def test_list_events_empty(api_client, auth_token):
    response = api_client.get("/api/v1/events", headers={
        "Authorization": f"Bearer {auth_token}",
    })
    assert response.status_code == 200
    assert response.json()["events"] == []


def test_emit_event(api_client, auth_token):
    response = api_client.post("/api/v1/events", headers={
        "Authorization": f"Bearer {auth_token}",
    }, json={
        "type": "new_client",
        "source": "test",
        "entity_id": "CLI-TEST",
        "entity_type": "client",
        "data": {"name": "Test Client"},
    })
    assert response.status_code == 201
    event = response.json()["event"]
    assert event["type"] == "new_client"
    assert event["workspace_id"] == "default"


def test_emit_event_creates_follow_up_task(api_client, auth_token):
    response = api_client.post("/api/v1/events", headers={
        "Authorization": f"Bearer {auth_token}",
    }, json={
        "type": "new_client",
        "source": "test",
        "entity_id": "CLI-002",
        "entity_type": "client",
        "data": {"name": "Another Client"},
    })
    assert response.status_code == 201

    missions = api_client.get("/api/v1/missions", headers={
        "Authorization": f"Bearer {auth_token}",
    }).json()["missions"]
    assert any("Follow up" in m["title"] for m in missions)
