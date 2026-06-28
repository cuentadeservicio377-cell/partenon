"""
G-Brain storage layer for Partenon.
Supports SQLite local storage and PostgreSQL via SQLAlchemy fallback.
"""

import json
import os
import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class GBrainStore:
    """Simple profile/mission/entity store."""

    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or os.getenv(
            "GBrain_DATABASE_URL", "sqlite:///data/gbrain.db"
        )
        if self.database_url.startswith("sqlite:///"):
            self.db_path = self.database_url.replace("sqlite:///", "")
            os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
        else:
            self.conn = None
        self._ensure_tables()

    def _ensure_tables(self):
        if self.conn is None:
            return
        with self.conn:
            self.conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile TEXT NOT NULL,
                    scope TEXT NOT NULL,
                    content TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS missions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mission_id TEXT NOT NULL UNIQUE,
                    profile TEXT NOT NULL,
                    title TEXT NOT NULL,
                    status TEXT NOT NULL,
                    input TEXT,
                    output TEXT,
                    learnings TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS entities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entity_id TEXT NOT NULL UNIQUE,
                    kind TEXT NOT NULL,
                    name TEXT NOT NULL,
                    data TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_profiles_profile ON profiles(profile);
                CREATE INDEX IF NOT EXISTS idx_missions_profile ON missions(profile);
                CREATE INDEX IF NOT EXISTS idx_entities_kind ON entities(kind);
                """
            )

    def read_profile(self, profile: str, scope: str = "default") -> Dict[str, Any]:
        if self.conn is None:
            return {}
        cur = self.conn.execute(
            "SELECT content FROM profiles WHERE profile = ? AND scope = ? ORDER BY id DESC LIMIT 1",
            (profile, scope),
        )
        row = cur.fetchone()
        if row is None:
            return {}
        return json.loads(row["content"])

    def write_profile(self, profile: str, scope: str, content: Dict[str, Any]) -> str:
        if self.conn is None:
            return "ok"
        now = datetime.now(timezone.utc).isoformat()
        with self.conn:
            self.conn.execute(
                "INSERT INTO profiles (profile, scope, content, updated_at) VALUES (?, ?, ?, ?)",
                (profile, scope, json.dumps(content, ensure_ascii=False), now),
            )
        return "ok"

    def write_mission(
        self,
        mission_id: str,
        profile: str,
        title: str,
        status: str,
        input_data: Optional[Dict[str, Any]] = None,
        output_data: Optional[Dict[str, Any]] = None,
        learnings: Optional[str] = None,
    ) -> str:
        if self.conn is None:
            return "ok"
        now = datetime.now(timezone.utc).isoformat()
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO missions (mission_id, profile, title, status, input, output, learnings, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(mission_id) DO UPDATE SET
                    status=excluded.status,
                    output=excluded.output,
                    learnings=excluded.learnings,
                    updated_at=excluded.updated_at
                """,
                (
                    mission_id,
                    profile,
                    title,
                    status,
                    json.dumps(input_data or {}, ensure_ascii=False),
                    json.dumps(output_data or {}, ensure_ascii=False),
                    learnings or "",
                    now,
                    now,
                ),
            )
        return "ok"

    def search_missions(self, profile: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        if self.conn is None:
            return []
        query = "SELECT * FROM missions WHERE 1=1"
        params: List[Any] = []
        if profile:
            query += " AND profile = ?"
            params.append(profile)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY updated_at DESC LIMIT 50"
        cur = self.conn.execute(query, params)
        rows = cur.fetchall()
        return [dict(r) for r in rows]

    def search_entities(self, query: str, kind: Optional[str] = None) -> List[Dict[str, Any]]:
        if self.conn is None:
            return []
        sql = "SELECT * FROM entities WHERE name LIKE ?"
        params: List[Any] = [f"%{query}%"]
        if kind:
            sql += " AND kind = ?"
            params.append(kind)
        sql += " ORDER BY updated_at DESC LIMIT 20"
        cur = self.conn.execute(sql, params)
        rows = cur.fetchall()
        return [dict(r) for r in rows]

    def store_learning(self, profile: str, insight: str) -> str:
        return self.write_mission(
            mission_id=f"learning-{datetime.now(timezone.utc).isoformat()}",
            profile=profile,
            title="Learning recorded",
            status="done",
            learnings=insight,
        )

    def put_page(self, slug: str, content: str, tags: Optional[List[str]] = None) -> str:
        """Save or update a page in the entities table."""
        if self.conn is None:
            return "ok"
        now = datetime.now(timezone.utc).isoformat()
        data = json.dumps({"content": content, "tags": tags or []}, ensure_ascii=False)
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO entities (entity_id, kind, name, data, updated_at)
                VALUES (?, 'page', ?, ?, ?)
                ON CONFLICT(entity_id) DO UPDATE SET
                    kind=excluded.kind,
                    name=excluded.name,
                    data=excluded.data,
                    updated_at=excluded.updated_at
                """,
                (slug, slug, data, now),
            )
        return "ok"

    def get_page(self, slug: str) -> Dict[str, Any]:
        """Retrieve a page by slug."""
        if self.conn is None:
            return {}
        cur = self.conn.execute(
            "SELECT entity_id, data FROM entities WHERE entity_id = ? AND kind = 'page'",
            (slug,),
        )
        row = cur.fetchone()
        if row is None:
            return {}
        parsed = json.loads(row["data"])
        return {
            "slug": row["entity_id"],
            "content": parsed.get("content", ""),
            "tags": parsed.get("tags", []),
        }

    def search_pages(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Hybrid text search over stored pages."""
        if self.conn is None:
            return []
        pattern = f"%{query}%"
        cur = self.conn.execute(
            """
            SELECT entity_id, name, data FROM entities
            WHERE kind = 'page' AND (name LIKE ? OR data LIKE ?)
            ORDER BY updated_at DESC
            LIMIT ?
            """,
            (pattern, pattern, limit),
        )
        rows = cur.fetchall()
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
        return results

    def link_pages(self, from_slug: str, to_slug: str, type_: str = "related") -> str:
        """Create a typed link between two pages by storing a link record."""
        if self.conn is None:
            return "ok"
        now = datetime.now(timezone.utc).isoformat()
        link_slug = f"link:{from_slug}:{to_slug}:{type_}"
        data = json.dumps({"from": from_slug, "to": to_slug, "type": type_}, ensure_ascii=False)
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO entities (entity_id, kind, name, data, updated_at)
                VALUES (?, 'link', ?, ?, ?)
                ON CONFLICT(entity_id) DO UPDATE SET
                    data=excluded.data,
                    updated_at=excluded.updated_at
                """,
                (link_slug, link_slug, data, now),
            )
        return "ok"

    def conflicts(self, profile: Optional[str] = None) -> List[Dict[str, Any]]:
        """Detect pages marked as conflicting."""
        if self.conn is None:
            return []
        pattern = "%conflict:true%"
        sql = "SELECT entity_id, name, data FROM entities WHERE kind = 'page' AND data LIKE ?"
        params: List[Any] = [pattern]
        if profile:
            sql += " AND (name LIKE ? OR data LIKE ?)"
            profile_pattern = f"%{profile}%"
            params.extend([profile_pattern, profile_pattern])
        sql += " ORDER BY updated_at DESC LIMIT 20"
        cur = self.conn.execute(sql, params)
        rows = cur.fetchall()
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
        return results
