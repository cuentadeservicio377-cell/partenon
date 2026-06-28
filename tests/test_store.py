"""Tests for the atomic JSON store."""

import json

from partenon_api.store import JsonStore, _migrate_legacy_tasks


def test_store_read_write_list(temp_data_dir):
    store = JsonStore(temp_data_dir / "test.json")
    store.write_list([{"id": "a", "value": 1}])
    items = store.read_list()
    assert items == [{"id": "a", "value": 1}]


def test_store_update_in_list(temp_data_dir):
    store = JsonStore(temp_data_dir / "test.json")
    store.write_list([{"id": "a", "value": 1}])
    updated = store.update_in_list("a", {"value": 2})
    assert updated == {"id": "a", "value": 2}
    assert store.read_list()[0]["value"] == 2


def test_store_delete_from_list(temp_data_dir):
    store = JsonStore(temp_data_dir / "test.json")
    store.write_list([{"id": "a"}, {"id": "b"}])
    assert store.delete_from_list("a") is True
    assert store.read_list() == [{"id": "b"}]


def test_migrate_legacy_tasks(temp_data_dir):
    legacy = temp_data_dir / "tasks.json"
    legacy.write_text(json.dumps([{
        "id": "mission-legacy",
        "profile": "partenon-scribe",
        "title": "Legacy",
        "status": "backlog",
        "priority": "medium",
        "description": "",
    }]))
    missions = _migrate_legacy_tasks()
    assert len(missions) == 1
    assert missions[0]["workspace_id"] == "default"
    assert "created_at" in missions[0]
