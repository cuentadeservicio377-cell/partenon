"""MCP client for G-Brain used by the Partenon Brain."""

import json
import os
import subprocess
from typing import Any


class GBrainClient:
    """G-Brain client via the `gbrain` command."""

    def __init__(self, database_url: str | None = None):
        self.database_url = database_url or os.getenv(
            "GBRAIN_DATABASE_URL", "postgresql://localhost:5432/gbrain"
        )

    def _call(
        self, command: str, *args: str, stdin: str | None = None
    ) -> dict[str, Any]:
        """Run a gbrain command and return parsed JSON."""
        full_args = ["gbrain", command, *args]
        result = subprocess.run(
            full_args,
            input=stdin.encode() if stdin is not None else None,
            capture_output=True,
            text=True,
            check=False,
            env={**os.environ, "GBRAIN_DATABASE_URL": self.database_url},
        )
        if result.returncode != 0:
            return {"ok": False, "error": result.stderr.strip()}
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"ok": True, "raw": result.stdout.strip()}

    def put_page(
        self, slug: str, content: str, tags: list[str] | None = None
    ) -> dict[str, Any]:
        """Save or update a page in G-Brain."""
        tags = tags or []
        full_content = f"---\ntags: {json.dumps(tags)}\n---\n\n{content}"
        return self._call("put", slug, stdin=full_content)

    def get_page(self, slug: str) -> dict[str, Any]:
        """Retrieve a page by slug."""
        return self._call("get", slug)

    def search(self, query: str, limit: int = 5) -> dict[str, Any]:
        """Hybrid text search."""
        return self._call("query", query, "--no-expand")

    def link(
        self, from_slug: str, to_slug: str, type_: str = "related"
    ) -> dict[str, Any]:
        """Create a typed link between two pages."""
        return self._call("link", from_slug, to_slug, "--type", type_)

    def conflicts(self, profile: str | None = None) -> dict[str, Any]:
        """Detect decisions marked as conflicting."""
        query = f"conflict:true {profile or ''}".strip()
        return self.search(query, limit=20)
