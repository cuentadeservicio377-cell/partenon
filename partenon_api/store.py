"""Atomic JSON file store with workspace-aware migration helpers."""

import fcntl
import json
import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from partenon_api.config import DEFAULT_WORKSPACE_ID, get_data_dir


def _acquire_lock(file_obj, exclusive: bool = True) -> None:
    """Acquire an advisory file lock (Unix-only)."""
    try:
        flag = fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH
        fcntl.flock(file_obj.fileno(), flag)
    except (AttributeError, OSError):
        pass


def _release_lock(file_obj) -> None:
    """Release an advisory file lock."""
    try:
        fcntl.flock(file_obj.fileno(), fcntl.LOCK_UN)
    except (AttributeError, OSError):
        pass


class JsonStore:
    """Persistent JSON store with atomic writes and advisory locking."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _atomic_write(self, data: Any) -> None:
        """Write JSON atomically via a temporary file and rename."""
        raw = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
        fd, tmp_path = tempfile.mkstemp(
            dir=str(self.path.parent), prefix=f".{self.path.name}.", suffix=".tmp"
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                _acquire_lock(f, exclusive=True)
                try:
                    f.write(raw)
                    f.flush()
                    os.fsync(f.fileno())
                finally:
                    _release_lock(f)
            shutil.move(tmp_path, self.path)
        except Exception:
            try:
                os.unlink(tmp_path)
            except FileNotFoundError:
                pass
            raise

    def read_list(self) -> List[dict]:
        """Read the file as a list of objects."""
        if not self.path.exists():
            return []
        with open(self.path, "r", encoding="utf-8") as f:
            _acquire_lock(f, exclusive=False)
            try:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    return []
            finally:
                _release_lock(f)
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "items" in data:
            return list(data.get("items", []))
        return []

    def write_list(self, items: List[dict]) -> None:
        """Write a list of objects atomically."""
        self._atomic_write(items)

    def read_dict(self) -> Dict[str, Any]:
        """Read the file as a dictionary."""
        if not self.path.exists():
            return {}
        with open(self.path, "r", encoding="utf-8") as f:
            _acquire_lock(f, exclusive=False)
            try:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
            finally:
                _release_lock(f)

    def write_dict(self, data: Dict[str, Any]) -> None:
        """Write a dictionary atomically."""
        self._atomic_write(data)

    def update_in_list(self, item_id: str, patch: dict, id_key: str = "id") -> Optional[dict]:
        """Update an item inside a list by id and persist."""
        items = self.read_list()
        for i, item in enumerate(items):
            if item.get(id_key) == item_id:
                items[i] = {**item, **patch, id_key: item_id}
                self.write_list(items)
                return items[i]
        return None

    def delete_from_list(self, item_id: str, id_key: str = "id") -> bool:
        """Delete an item from a list by id and persist."""
        items = self.read_list()
        filtered = [item for item in items if item.get(id_key) != item_id]
        if len(filtered) == len(items):
            return False
        self.write_list(filtered)
        return True


def _migrate_legacy_tasks() -> List[dict]:
    """Migrate data/tasks.json to missions schema with workspace_id."""
    legacy_path = get_data_dir() / "tasks.json"
    store = JsonStore(get_data_dir() / "missions.json")
    if store.path.exists():
        return store.read_list()
    if not legacy_path.exists():
        return []

    with open(legacy_path, "r", encoding="utf-8") as f:
        try:
            tasks = json.load(f)
        except json.JSONDecodeError:
            tasks = []
    if not isinstance(tasks, list):
        tasks = []

    missions = []
    for task in tasks:
        mission = dict(task)
        mission.setdefault("workspace_id", DEFAULT_WORKSPACE_ID)
        mission.setdefault("created_at", datetime.now().isoformat())
        mission.setdefault("updated_at", datetime.now().isoformat())
        missions.append(mission)

    store.write_list(missions)
    return missions


def _migrate_legacy_cron() -> List[dict]:
    """Migrate data/cron.json to workspace-aware schema."""
    legacy_path = get_data_dir() / "cron.json"
    store = JsonStore(legacy_path)
    jobs = store.read_list()
    if not jobs:
        return []

    needs_write = False
    for job in jobs:
        if "workspace_id" not in job:
            job["workspace_id"] = DEFAULT_WORKSPACE_ID
            needs_write = True
        if "created_at" not in job:
            job["created_at"] = datetime.now().isoformat()
            needs_write = True
        if "updated_at" not in job:
            job["updated_at"] = datetime.now().isoformat()
            needs_write = True
    if needs_write:
        store.write_list(jobs)
    return jobs


def get_mission_store() -> JsonStore:
    """Return the mission store, migrating legacy data if needed."""
    _migrate_legacy_tasks()
    return JsonStore(get_data_dir() / "missions.json")


def get_cron_store() -> JsonStore:
    """Return the cron job store, migrating legacy data if needed."""
    _migrate_legacy_cron()
    return JsonStore(get_data_dir() / "cron.json")


def get_event_store() -> JsonStore:
    return JsonStore(get_data_dir() / "events.json")


def get_nudge_store() -> JsonStore:
    return JsonStore(get_data_dir() / "nudges.json")
