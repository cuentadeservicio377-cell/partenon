# Partenon Guardian — Security Skill Pack

> Security, access, and model recommendation agent for small businesses.
> Audits keys, validates permissions, recommends models, and logs events.

## Included skills

### `security`
- List and rotate API keys.
- Audit profile permissions and access requests.
- Manage secrets references.
- Recommend GPU/model allocations.
- Set and review security policies.
- Audit key strength and detect providers.
- Recommend AI models by provider, budget, and latency.

## Quick start

1. Copy `.env.example` to `.env` and fill in provider keys.
2. Copy `templates/.security.example` to your workspace as `.security`.
3. Use `skills/security/tools/audit.py` to audit profile permissions.
4. Use `skills/security/tools/key_manager.py` to check key strength.
5. Use `skills/security/tools/model_recommender.py` to choose a model.

## Safety rules

- The Guardian never exposes full secrets in logs.
- Key rotation always requires explicit owner approval.
- Access changes follow least privilege.
- Every security event is logged in G-Brain.

## MCP Tools

The Guardian exposes the `partenon-security` MCP server. Available tools:

- `security_list_keys`
- `security_rotate_key`
- `security_audit_access`
- `security_validate_access`
- `security_manage_secrets`
- `security_allocate_gpu`
- `security_set_policy`
- `security_audit_log`
- `security_audit_key_strength`
- `security_detect_key_provider`
- `security_recommend_model`
- `security_rotate_key_live`

## Dry-run vs live

| Tool | Dry-run behavior | Live requirement |
|---|---|---|
| `security_audit_key_strength` | Local analysis of length, entropy, and weak substrings. | None. |
| `security_detect_key_provider` | Detects provider from key prefix. | None. |
| `security_recommend_model` | Returns a recommendation table. | None. |
| `security_rotate_key` | Simulates rotation. | Provider API access + explicit approval. |
| `security_rotate_key_live` | Returns a controlled placeholder. | Provider API access + explicit approval. |
| `security_audit_access` | Simulates permission audit. | Policy store access. |
| `security_manage_secrets` | Simulates secret management. | Approved secrets manager. |

Live mode is opt-in. Key-strength and model-recommendation tools run safely without credentials.
