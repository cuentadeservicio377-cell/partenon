"""MCP client for G-Brain used by the Partenon Brain.

This implementation uses the local GBrainStore from `gbrain.tools` instead of
shelling out to an external `gbrain` binary.
"""

import json
import os
from pathlib import Path
from typing import Any, Optional

try:
    from mcp_servers.memory.tools import GBrainStore
except ImportError:  # pragma: no cover - fallback when repo root is not on sys.path
    import importlib.util

    _REPO_ROOT = Path(__file__).resolve().parents[6]
    _TOOLS_PATH = _REPO_ROOT / "mcp_servers" / "memory" / "tools.py"
    _spec = importlib.util.spec_from_file_location("mcp_servers.memory.tools", _TOOLS_PATH)
    _module = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_module)
    GBrainStore = _module.GBrainStore  # type: ignore[misc]


class GBrainClient:
    """G-Brain client backed by the local GBrainStore."""

    def __init__(self, database_url: Optional[str] = None):
        self.store = GBrainStore(
            database_url
            or os.getenv("GBRAIN_DATABASE_URL")
            or os.getenv("GBrain_DATABASE_URL")
        )

    def _conn(self):
        """Return the SQLite connection if available."""
        return self.store.conn

    def _ensure_page_table(self):
        """Ensure the entities table exists for page storage."""
        conn = self._conn()
        if conn is None:
            return
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_id TEXT NOT NULL UNIQUE,
                kind TEXT NOT NULL,
                name TEXT NOT NULL,
                data TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    @staticmethod
    def _now() -> str:
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()

    def put_page(
        self, slug: str, content: str, tags: Optional[list[str]] = None
    ) -> dict[str, Any]:
        """Save or update a page in G-Brain."""
        conn = self._conn()
        if conn is None:
            return {
                "ok": False,
                "error": "put_page requires a SQLite-backed GBrainStore",
            }
        self._ensure_page_table()
        data = json.dumps(
            {"content": content, "tags": tags or []},
            ensure_ascii=False,
        )
        conn.execute(
            """
            INSERT INTO entities (entity_id, kind, name, data, updated_at)
            VALUES (?, 'page', ?, ?, ?)
            ON CONFLICT(entity_id) DO UPDATE SET
                kind=excluded.kind,
                name=excluded.name,
                data=excluded.data,
                updated_at=excluded.updated_at
            """,
            (slug, slug, data, self._now()),
        )
        conn.commit()
        return {"ok": True, "slug": slug}

    def get_page(self, slug: str) -> dict[str, Any]:
        """Retrieve a page by slug."""
        conn = self._conn()
        if conn is None:
            return {"ok": False, "error": "get_page requires a SQLite-backed GBrainStore"}
        self._ensure_page_table()
        row = conn.execute(
            "SELECT entity_id, data FROM entities WHERE entity_id = ? AND kind = 'page'",
            (slug,),
        ).fetchone()
        if row is None:
            return {"ok": False, "error": f"page not found: {slug}"}
        parsed = json.loads(row["data"])
        return {
            "ok": True,
            "slug": row["entity_id"],
            "content": parsed.get("content", ""),
            "tags": parsed.get("tags", []),
        }

    def search(self, query: str, limit: int = 5) -> dict[str, Any]:
        """Hybrid text search over stored pages."""
        conn = self._conn()
        if conn is None:
            return {"ok": True, "results": [], "total": 0}
        self._ensure_page_table()
        pattern = f"%{query}%"
        rows = conn.execute(
            """
            SELECT entity_id, name, data FROM entities
            WHERE kind = 'page' AND (name LIKE ? OR data LIKE ?)
            ORDER BY updated_at DESC
            LIMIT ?
            """,
            (pattern, pattern, limit),
        ).fetchall()
        results = []
        for row in rows:
            parsed = json.loads(row["data"])
            results.append(
                {
                    "slug": row["entity_id"],
                    "name": row["name"],
                    "content": parsed.get("content", "")[:500],
                    "tags": parsed.get("tags", []),
                }
            )
        return {"ok": True, "results": results, "total": len(results)}

    def link(
        self, from_slug: str, to_slug: str, type_: str = "related"
    ) -> dict[str, Any]:
        """Create a typed link between two pages.

        The local GBrainStore does not support links, so this returns a no-op
        response with a warning.
        """
        return {
            "ok": True,
            "warning": "link is not supported by the local SQLite GBrainStore",
            "from": from_slug,
            "to": to_slug,
            "type": type_,
        }

    def conflicts(self, profile: Optional[str] = None) -> dict[str, Any]:
        """Detect decisions marked as conflicting."""
        conn = self._conn()
        if conn is None:
            return {"ok": True, "results": [], "total": 0}
        self._ensure_page_table()
        pattern = "%conflict:true%"
        sql = "SELECT entity_id, name, data FROM entities WHERE kind = 'page' AND data LIKE ?"
        params: list[Any] = [pattern]
        if profile:
            sql += " AND (name LIKE ? OR data LIKE ?)"
            profile_pattern = f"%{profile}%"
            params.extend([profile_pattern, profile_pattern])
        sql += " ORDER BY updated_at DESC LIMIT 20"
        rows = conn.execute(sql, params).fetchall()
        results = []
        for row in rows:
            parsed = json.loads(row["data"])
            results.append(
                {
                    "slug": row["entity_id"],
                    "name": row["name"],
                    "content": parsed.get("content", ""),
                    "tags": parsed.get("tags", []),
                }
            )
        return {"ok": True, "results": results, "total": len(results)}
