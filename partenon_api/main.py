"""FastAPI application for Partenon Mission Control."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from partenon_api.config import get_dashboard_origin, get_data_dir, get_gbrain_database_url
from partenon_api.mcp_client import AsyncMemoryClient
from partenon_api.routers import auth, cron, events, gateway, heroes, integrations, missions, stream
from partenon_api.store import JsonStore, migrate_legacy_json_to_memory


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: seed default workspace and connect memory store."""
    data_dir = get_data_dir()
    workspace_store = JsonStore(data_dir / "workspaces.json")
    workspaces = workspace_store.read_list()
    if not any(w.get("id") == "default" for w in workspaces):
        workspaces.append({
            "id": "default",
            "name": "Default workspace",
            "created_at": __import__("datetime").datetime.now().isoformat(),
        })
        workspace_store.write_list(workspaces)

    # Connect to the partenon-memory MCP server unless tests request the
    # synchronous JSON fallback.
    store_mode = os.environ.get("PARTENON_STORE_MODE", "mcp")
    memory_client: AsyncMemoryClient | None = None
    if store_mode != "json":
        memory_client = AsyncMemoryClient(database_url=get_gbrain_database_url())
        await memory_client.__aenter__()
        try:
            await migrate_legacy_json_to_memory(memory_client, data_dir)
        except Exception:
            # Do not block startup if migration fails; log and continue.
            pass

    app.state.memory_client = memory_client
    yield
    if memory_client is not None:
        await memory_client.__aexit__(None, None, None)


app = FastAPI(
    title="Partenon API",
    description="Real-time operations backend for Hermes Partenon profiles.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[get_dashboard_origin()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(missions.router, prefix="/api/v1")
app.include_router(cron.router, prefix="/api/v1")
app.include_router(heroes.router, prefix="/api/v1")
app.include_router(events.router, prefix="/api/v1")
app.include_router(integrations.router, prefix="/api/v1")
app.include_router(stream.router, prefix="/api/v1")
app.include_router(gateway.router, prefix="/api/v1")


@app.get("/health", tags=["system"])
async def health() -> dict:
    return {"status": "ok", "service": "partenon-api"}


if __name__ == "__main__":
    import uvicorn

    from partenon_api.config import get_api_host, get_api_port

    uvicorn.run("partenon_api.main:app", host=get_api_host(), port=get_api_port(), reload=True)
