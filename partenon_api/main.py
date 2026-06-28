"""FastAPI application for Partenon Mission Control."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from partenon_api.config import get_dashboard_origin
from partenon_api.routers import auth, cron, events, heroes, integrations, missions, stream


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: seed default workspace on startup."""
    from partenon_api.config import DEFAULT_WORKSPACE_ID, get_data_dir
    from partenon_api.store import JsonStore

    data_dir = get_data_dir()
    workspace_store = JsonStore(data_dir / "workspaces.json")
    workspaces = workspace_store.read_list()
    if not any(w.get("id") == DEFAULT_WORKSPACE_ID for w in workspaces):
        workspaces.append({
            "id": DEFAULT_WORKSPACE_ID,
            "name": "Default workspace",
            "created_at": __import__("datetime").datetime.now().isoformat(),
        })
        workspace_store.write_list(workspaces)
    yield


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


@app.get("/health", tags=["system"])
async def health() -> dict:
    return {"status": "ok", "service": "partenon-api"}


if __name__ == "__main__":
    import uvicorn

    from partenon_api.config import get_api_host, get_api_port

    uvicorn.run("partenon_api.main:app", host=get_api_host(), port=get_api_port(), reload=True)
