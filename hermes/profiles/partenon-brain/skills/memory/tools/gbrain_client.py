"""Cliente MCP para G-Brain usado por el Brain de Partenon."""

import json
import os
import subprocess
from typing import Any


class GBrainClient:
    """Cliente de G-Brain via comando `gbrain`."""

    def __init__(self, database_url: str | None = None):
        self.database_url = database_url or os.getenv(
            "GBRAIN_DATABASE_URL", "postgresql://localhost:5432/gbrain"
        )

    def _call(self, command: str, *args: str) -> dict[str, Any]:
        """Ejecuta un comando de gbrain y devuelve el JSON parseado."""
        full_args = ["gbrain", command, *args]
        result = subprocess.run(
            full_args,
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

    def put_page(self, slug: str, content: str, tags: list[str] | None = None) -> dict[str, Any]:
        """Guarda o actualiza una pagina en G-Brain."""
        import tempfile

        tags = tags or []
        full_content = f"---\ntags: {json.dumps(tags)}\n---\n\n{content}"
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(full_content)
            path = f.name
        try:
            return self._call("put", slug, f"<{path}")
        finally:
            os.unlink(path)

    def get_page(self, slug: str) -> dict[str, Any]:
        """Recupera una pagina por slug."""
        return self._call("get", slug)

    def search(self, query: str, limit: int = 5) -> dict[str, Any]:
        """Busqueda hibrida por texto."""
        return self._call("query", query, "--no-expand")

    def link(self, from_slug: str, to_slug: str, type_: str = "related") -> dict[str, Any]:
        """Crea un enlace tipado entre dos paginas."""
        return self._call("link", from_slug, to_slug, "--type", type_)

    def conflicts(self, profile: str | None = None) -> dict[str, Any]:
        """Detecta decisiones marcadas como conflictivas."""
        query = f"conflict:true {profile or ''}".strip()
        return self.search(query, limit=20)
