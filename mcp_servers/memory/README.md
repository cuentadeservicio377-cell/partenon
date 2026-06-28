# partenon-memory

Shared memory MCP server for Partenon (formerly `gbrain`).

## Exposed tools

- `gbrain_read_profile(profile, scope="default")`
- `gbrain_write_profile(profile, scope, content)`
- `gbrain_write_mission(mission_id, profile, title, status, input_data, output_data, learnings)`
- `gbrain_search_missions(profile=None, status=None)`
- `gbrain_search_entities(query, kind=None)`
- `gbrain_store_learning(profile, insight)`

## Usage

```bash
pip install -e .
python -m mcp_servers.memory.server
```

Configure in Hermes:

```yaml
mcp_servers:
  partenon-memory:
    command: python
    args: ["-m", "mcp_servers.memory.server"]
    env:
      GBRAIN_DATABASE_URL: "sqlite:///data/gbrain.db"
```
