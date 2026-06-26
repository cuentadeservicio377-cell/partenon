# Partenon Web Promise Examples

This directory contains placeholder implementations that demonstrate the interfaces described on the public website (`web/index.html`, `web/heroes.html`, `web/developers.html`). They are intended to close the gap between marketing copy and repository reality until production implementations are ready.

## Files

- `hermes-cli-stub.py` — Stub for the `hermes` command-line interface.
- `api-server-stub.py` — Stub REST API server matching the documented endpoints.
- `mcp-client-example.py` — Example client for the G-Brain MCP server.

## Running the stubs

### Hermes CLI stub

```bash
python3 -m venv .venv
source .venv/bin/activate
python examples/hermes-cli-stub.py init --name "Cafe Central"
python examples/hermes-cli-stub.py activate scribe
python examples/hermes-cli-stub.py mission scribe --type financial-model
python examples/hermes-cli-stub.py status --verbose
```

### API server stub

```bash
pip install fastapi uvicorn
uvicorn examples.api-server-stub:app --reload --port 8000
```

Then test with curl:

```bash
curl http://localhost:8000/api/v1/heroes
curl http://localhost:8000/api/v1/mcp/tools
curl -X POST http://localhost:8000/api/v1/missions \
  -H "Content-Type: application/json" \
  -d '{"hero": "scribe", "type": "financial-model"}'
```

### MCP client example

```bash
pip install mcp
python examples/mcp-client-example.py
```

## Important note

These files are **stubs**. They do not perform real Stripe charges, send real emails, or modify real Google Workspace documents. They exist to:

1. Show the intended command and API shapes.
2. Help front-end and integration development proceed in parallel.
3. Serve as acceptance criteria for the production implementations.

See `MISSING_IMPLEMENTATION.md` for the full audit and recommended production fixes.
