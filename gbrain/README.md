# partenon-gbrain

Shared memory MCP server for Partenon.

## Exposed tools

- `gbrain_read_profile(profile, scope="default")`
- `gbrain_write_profile(profile, scope, content)`
- `gbrain_write_mission(mission_id, profile, title, status, input_data, output_data, learnings)`
- `gbrain_search_missions(profile=None, status=None)`
- `gbrain_search_entities(query, kind=None)`
- `gbrain_store_learning(profile, insight)`

## Usage

```bash
pip install mcp
python -m gbrain.server
```

Configure in `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  gbrain:
    command: python
    args: ["-m", "gbrain.server"]
    env:
      GBrain_DATABASE_URL: "sqlite:///data/gbrain.db"
```
