"""Memory-backed store for the Partenon API.

Production code uses the `partenon-memory` MCP server via `AsyncMemoryClient`.
A JSON-file fallback is available for tests and local scripts; it is selected
automatically when no MCP client is provided or when `PARTENON_STORE_MODE=json`
is set.
"""

import fcntl
import json
import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from partenon_api.config import DEFAULT_WORKSPACE_ID, get_data_dir
from partenon_api.mcp_client import AsyncMemoryClient
from partenon_api.utils import filter_by_workspace, new_id, now_iso

# ---------------------------------------------------------------------------
# Legacy atomic JSON store (used by the test fallback and migration)
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Legacy migration helpers (still used by tests and the JSON fallback)
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Slug/tag mapping
# ---------------------------------------------------------------------------


_COLLECTION_SLUG = {
    "mission": "missions",
    "cron": "cron",
    "event": "events",
    "nudge": "nudges",
}


def _slug(kind: str, workspace_id: str, item_id: str) -> str:
    return f"workspace/{workspace_id}/{_COLLECTION_SLUG[kind]}/{item_id}"


def _item_tags(kind: str, workspace_id: str, item: dict) -> List[str]:
    tags = [kind, f"workspace:{workspace_id}"]
    profile = item.get("profile") or item.get("target_profile")
    if profile:
        tags.append(profile)
    return tags


# ---------------------------------------------------------------------------
# JSON fallback backend
# ---------------------------------------------------------------------------


class _JsonBackend:
    """Synchronous JSON backend used when the MCP client is unavailable."""

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        _migrate_legacy_tasks()
        _migrate_legacy_cron()
        self.missions = JsonStore(data_dir / "missions.json")
        self.cron = JsonStore(data_dir / "cron.json")
        self.nudges = JsonStore(data_dir / "nudges.json")
        self.events = JsonStore(data_dir / "events.json")

    # Missions
    def list_missions(self, workspace_id: str, profile: Optional[str] = None) -> List[dict]:
        items = filter_by_workspace(self.missions.read_list(), workspace_id)
        if profile:
            items = [i for i in items if i.get("profile") == profile]
        return items

    def create_mission(self, workspace_id: str, mission: dict) -> dict:
        mission = dict(mission)
        mission.setdefault("id", new_id("mission"))
        mission.setdefault("workspace_id", workspace_id)
        mission.setdefault("created_at", now_iso())
        mission.setdefault("updated_at", now_iso())
        items = self.missions.read_list()
        items.append(mission)
        self.missions.write_list(items)
        return mission

    def update_mission(self, workspace_id: str, mission_id: str, patch: dict) -> Optional[dict]:
        items = self.missions.read_list()
        for i, item in enumerate(items):
            if item.get("id") == mission_id and item.get("workspace_id", DEFAULT_WORKSPACE_ID) == workspace_id:
                item.update(patch)
                item["id"] = mission_id
                item["updated_at"] = now_iso()
                items[i] = item
                self.missions.write_list(items)
                return item
        return None

    def delete_mission(self, workspace_id: str, mission_id: str) -> bool:
        items = self.missions.read_list()
        original_len = len(items)
        items = [
            i for i in items
            if not (i.get("id") == mission_id and i.get("workspace_id", DEFAULT_WORKSPACE_ID) == workspace_id)
        ]
        if len(items) == original_len:
            return False
        self.missions.write_list(items)
        return True

    # Cron
    def list_cron_jobs(self, workspace_id: str, profile: Optional[str] = None) -> List[dict]:
        items = filter_by_workspace(self.cron.read_list(), workspace_id)
        if profile:
            items = [i for i in items if i.get("profile") == profile]
        return items

    def create_cron_job(self, workspace_id: str, job: dict) -> dict:
        job = dict(job)
        job.setdefault("id", new_id("cron"))
        job.setdefault("workspace_id", workspace_id)
        job.setdefault("created_at", now_iso())
        job.setdefault("updated_at", now_iso())
        items = self.cron.read_list()
        items.append(job)
        self.cron.write_list(items)
        return job

    def update_cron_job(self, workspace_id: str, job_id: str, patch: dict) -> Optional[dict]:
        items = self.cron.read_list()
        for i, item in enumerate(items):
            if item.get("id") == job_id and item.get("workspace_id", DEFAULT_WORKSPACE_ID) == workspace_id:
                item.update(patch)
                item["id"] = job_id
                item["updated_at"] = now_iso()
                items[i] = item
                self.cron.write_list(items)
                return item
        return None

    def delete_cron_job(self, workspace_id: str, job_id: str) -> bool:
        items = self.cron.read_list()
        original_len = len(items)
        items = [
            i for i in items
            if not (i.get("id") == job_id and i.get("workspace_id", DEFAULT_WORKSPACE_ID) == workspace_id)
        ]
        if len(items) == original_len:
            return False
        self.cron.write_list(items)
        return True

    # Nudges
    def list_nudges(self, workspace_id: str, target_profile: Optional[str] = None) -> List[dict]:
        items = filter_by_workspace(self.nudges.read_list(), workspace_id)
        if target_profile:
            items = [i for i in items if i.get("target_profile") in (target_profile, "all")]
        return items

    # Events
    def list_events(self, workspace_id: str) -> List[dict]:
        data = self.events.read_dict()
        events = data.get("events", [])
        if not isinstance(events, list):
            return []
        return filter_by_workspace(events, workspace_id)

    def upsert_event(self, event: dict) -> dict:
        event = dict(event)
        data = self.events.read_dict()
        events = data.get("events", [])
        if not isinstance(events, list):
            events = []
        for i, existing in enumerate(events):
            if existing.get("id") == event.get("id"):
                events[i] = event
                break
        else:
            events.append(event)
        data["events"] = events
        data["updated_at"] = now_iso()
        self.events.write_dict(data)
        return event


# ---------------------------------------------------------------------------
# Async MCP-backed store
# ---------------------------------------------------------------------------


class MemoryStore:
    """Unified async store backed by the partenon-memory MCP server.

    When `client` is ``None`` the store falls back to synchronous JSON files so
    tests and local scripts can run without spawning an MCP subprocess.
    """

    def __init__(
        self,
        client: Optional[AsyncMemoryClient] = None,
        data_dir: Optional[Path] = None,
    ):
        self._client = client
        self._data_dir = data_dir or get_data_dir()
        self._fallback: Optional[_JsonBackend] = None if client else _JsonBackend(self._data_dir)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _mcp_list(self, kind: str, workspace_id: str, profile: Optional[str] = None) -> List[dict]:
        pages = await self._client.search("", limit=10000)
        items: List[dict] = []
        for page in pages:
            tags = page.get("tags", [])
            if kind not in tags or f"workspace:{workspace_id}" not in tags:
                continue
            try:
                item = json.loads(page.get("content", "{}"))
            except json.JSONDecodeError:
                continue
            if item.get("deleted"):
                continue
            items.append(item)
        if profile:
            items = [i for i in items if i.get("profile") == profile]
        return items

    async def _mcp_create(self, kind: str, workspace_id: str, item: dict) -> dict:
        item = dict(item)
        item.setdefault("workspace_id", workspace_id)
        item_id = item.get("id") or new_id(kind)
        item["id"] = item_id
        slug = _slug(kind, workspace_id, item_id)
        tags = _item_tags(kind, workspace_id, item)
        await self._client.put_page(slug, json.dumps(item, ensure_ascii=False), tags)
        return item

    async def _mcp_update(self, kind: str, workspace_id: str, item_id: str, patch: dict) -> Optional[dict]:
        slug = _slug(kind, workspace_id, item_id)
        page = await self._client.get_page(slug)
        if not page or not page.get("content"):
            return None
        try:
            item = json.loads(page["content"])
        except json.JSONDecodeError:
            return None
        if item.get("workspace_id", DEFAULT_WORKSPACE_ID) != workspace_id:
            return None
        item.update(patch)
        item["id"] = item_id
        item["updated_at"] = now_iso()
        tags = _item_tags(kind, workspace_id, item)
        await self._client.put_page(slug, json.dumps(item, ensure_ascii=False), tags)
        return item

    async def _mcp_delete(self, kind: str, workspace_id: str, item_id: str) -> bool:
        slug = _slug(kind, workspace_id, item_id)
        page = await self._client.get_page(slug)
        if not page or not page.get("content"):
            return False
        try:
            item = json.loads(page["content"])
        except json.JSONDecodeError:
            return False
        if item.get("workspace_id", DEFAULT_WORKSPACE_ID) != workspace_id:
            return False
        item["deleted"] = True
        tags = list({*page.get("tags", []), "deleted"})
        await self._client.put_page(slug, json.dumps(item, ensure_ascii=False), tags)
        return True

    # ------------------------------------------------------------------
    # Missions
    # ------------------------------------------------------------------

    async def list_missions(self, workspace_id: str, profile: Optional[str] = None) -> List[dict]:
        if self._fallback:
            return self._fallback.list_missions(workspace_id, profile)
        return await self._mcp_list("mission", workspace_id, profile)

    async def create_mission(self, workspace_id: str, mission: dict) -> dict:
        if self._fallback:
            return self._fallback.create_mission(workspace_id, mission)
        return await self._mcp_create("mission", workspace_id, mission)

    async def update_mission(self, workspace_id: str, mission_id: str, patch: dict) -> Optional[dict]:
        if self._fallback:
            return self._fallback.update_mission(workspace_id, mission_id, patch)
        return await self._mcp_update("mission", workspace_id, mission_id, patch)

    async def delete_mission(self, workspace_id: str, mission_id: str) -> bool:
        if self._fallback:
            return self._fallback.delete_mission(workspace_id, mission_id)
        return await self._mcp_delete("mission", workspace_id, mission_id)

    # ------------------------------------------------------------------
    # Cron
    # ------------------------------------------------------------------

    async def list_cron_jobs(self, workspace_id: str, profile: Optional[str] = None) -> List[dict]:
        if self._fallback:
            return self._fallback.list_cron_jobs(workspace_id, profile)
        return await self._mcp_list("cron", workspace_id, profile)

    async def create_cron_job(self, workspace_id: str, job: dict) -> dict:
        if self._fallback:
            return self._fallback.create_cron_job(workspace_id, job)
        return await self._mcp_create("cron", workspace_id, job)

    async def update_cron_job(self, workspace_id: str, job_id: str, patch: dict) -> Optional[dict]:
        if self._fallback:
            return self._fallback.update_cron_job(workspace_id, job_id, patch)
        return await self._mcp_update("cron", workspace_id, job_id, patch)

    async def delete_cron_job(self, workspace_id: str, job_id: str) -> bool:
        if self._fallback:
            return self._fallback.delete_cron_job(workspace_id, job_id)
        return await self._mcp_delete("cron", workspace_id, job_id)

    # ------------------------------------------------------------------
    # Nudges
    # ------------------------------------------------------------------

    async def list_nudges(self, workspace_id: str, target_profile: Optional[str] = None) -> List[dict]:
        if self._fallback:
            return self._fallback.list_nudges(workspace_id, target_profile)
        return await self._mcp_list("nudge", workspace_id, target_profile)

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------

    async def list_events(self, workspace_id: str) -> List[dict]:
        if self._fallback:
            return self._fallback.list_events(workspace_id)
        pages = await self._client.search("", limit=10000)
        events = []
        for page in pages:
            tags = page.get("tags", [])
            if "event" not in tags or f"workspace:{workspace_id}" not in tags:
                continue
            try:
                event = json.loads(page.get("content", "{}"))
            except json.JSONDecodeError:
                continue
            if event.get("deleted"):
                continue
            events.append(event)
        return events

    async def upsert_event(self, event: dict) -> dict:
        if self._fallback:
            return self._fallback.upsert_event(event)
        event = dict(event)
        workspace_id = event.get("workspace_id", DEFAULT_WORKSPACE_ID)
        event_id = event.get("id") or new_id("event")
        event["id"] = event_id
        slug = _slug("event", workspace_id, event_id)
        tags = _item_tags("event", workspace_id, event)
        await self._client.put_page(slug, json.dumps(event, ensure_ascii=False), tags)
        return event


# ---------------------------------------------------------------------------
# Factory functions
# ---------------------------------------------------------------------------


def get_store(
    client: Optional[AsyncMemoryClient] = None,
    data_dir: Optional[Path] = None,
) -> MemoryStore:
    return MemoryStore(client=client, data_dir=data_dir)


def get_mission_store(
    client: Optional[AsyncMemoryClient] = None,
    data_dir: Optional[Path] = None,
) -> MemoryStore:
    return get_store(client, data_dir)


def get_cron_store(
    client: Optional[AsyncMemoryClient] = None,
    data_dir: Optional[Path] = None,
) -> MemoryStore:
    return get_store(client, data_dir)


def get_event_store(
    client: Optional[AsyncMemoryClient] = None,
    data_dir: Optional[Path] = None,
) -> MemoryStore:
    return get_store(client, data_dir)


def get_nudge_store(
    client: Optional[AsyncMemoryClient] = None,
    data_dir: Optional[Path] = None,
) -> MemoryStore:
    return get_store(client, data_dir)


# ---------------------------------------------------------------------------
# One-time migration from JSON files to G-Brain pages
# ---------------------------------------------------------------------------


async def migrate_legacy_json_to_memory(
    client: AsyncMemoryClient,
    data_dir: Optional[Path] = None,
) -> None:
    """Move existing missions.json and cron.json into G-Brain pages once."""
    data_dir = data_dir or get_data_dir()
    for filename, kind in (
        ("missions.json", "mission"),
        ("cron.json", "cron"),
        ("nudges.json", "nudge"),
    ):
        path = data_dir / filename
        migrated = data_dir / f"{filename}.migrated"
        if not path.exists() or migrated.exists():
            continue
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            raw = []
        if isinstance(raw, dict):
            raw = raw.get("nudges" if kind == "nudge" else "items", [])
        if not isinstance(raw, list):
            raw = []
        for item in raw:
            item = dict(item)
            item_id = item.get("id") or new_id(kind)
            item["id"] = item_id
            workspace_id = item.get("workspace_id", DEFAULT_WORKSPACE_ID)
            slug = _slug(kind, workspace_id, item_id)
            tags = _item_tags(kind, workspace_id, item)
            await client.put_page(slug, json.dumps(item, ensure_ascii=False), tags)
        path.rename(migrated)
