# Partenon Security Model

This document explains how Partenon handles credentials, permissions, audit logging, and key rotation. It is based on the actual code in `hermes/profiles/partenon-guardian/skills/security/`, `.env.example`, and the profile templates.

For setup instructions, read [`QUICKSTART.md`](QUICKSTART.md). For business guidance, read [`ENTREPRENEUR_PLAYBOOK.md`](ENTREPRENEUR_PLAYBOOK.md).

---

## Core principle

**Secrets live only in `.env`. Profile config files contain references, never values.**

No hero, script, or tool in this repository should ever write a raw API key, password, or token into `.finance`, `.design`, `.payments`, `.security`, `.ops`, `.relations`, or `.brain`. If you find a file that does, treat it as a bug.

---

## Credential storage

### `.env` (required)

Copy `.env.example` to `.env` and fill in your credentials. The installer does this automatically.

```bash
cp .env.example .env
```

Key variables:

| Variable | Used by | Notes |
|----------|---------|-------|
| `OPENROUTER_API_KEY` | All heroes | Default LLM router. |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Scribe, Herald, Strategist, Diplomat | Path to a Google Cloud service account JSON file. |
| `STRIPE_SECRET_KEY` | Collector | Live or test Stripe key. Keep in test mode until you are ready. |
| `STRIPE_PUBLISHABLE_KEY` | Collector | Public key for client-side links. |
| `NVIDIA_API_KEY` | Guardian, optional | For NVIDIA NIM model access. |
| `OPENAI_API_KEY` | Guardian, optional | For OpenAI model access. |
| `KIMI_API_KEY` | Guardian, optional | For Kimi model access. |
| `GBRAIN_DATABASE_URL` | Brain | Used by `.env.example`. |
| `GBrain_DATABASE_URL` | Brain | Used by `gbrain/server.py` and `partenon-core/config/mcp/servers.yaml`. |

> **Note on G-Brain naming:** `GBRAIN_DATABASE_URL` in `.env.example` does not match the `GBrain_DATABASE_URL` default used by `gbrain/server.py` and `partenon-core/config/mcp/servers.yaml`. Set the exact variable name required by the component you run. This inconsistency is tracked in `MISSING_IMPLEMENTATION.md`.

### `.security` (Guardian profile file)

`.security` is a configuration file, not a vault. It stores:

- The environment variable name that holds each provider key.
- A regex pattern the Guardian uses to validate key format.
- Rotation policy (`rotation_days: 90`).
- Least-privilege permissions for each profile.

Example entry from `hermes/profiles/partenon-guardian/templates/.security.example`:

```yaml
providers:
  stripe:
    env_var: STRIPE_SECRET_KEY
    pattern: "^sk_(test|live)_[A-Za-z0-9]+$"
    required: true
    key_reference: "env://STRIPE_SECRET_KEY"
    rotation_days: 90
```

The actual key value is never stored here. The `key_reference` field tells the Guardian where to look in the environment.

### Service account JSON files

Google Workspace integrations use a service account JSON file. Store it outside the repository or in a `.gitignore`d directory such as `config/`:

```bash
mkdir -p config
cp /path/to/downloaded-key.json config/google-service-account.json
# Set the variable in .env
GOOGLE_SERVICE_ACCOUNT_JSON=config/google-service-account.json
```

Add `config/` to `.gitignore` if it is not already there.

---

## Guardian responsibilities

The Guardian (`partenon-guardian`) is the security layer. Its real tools are in `hermes/profiles/partenon-guardian/skills/security/tools/`.

### Key management (`key_manager.py`)

- `list_keys()` — reads environment variables, returns masked fingerprints only. Full values are never returned.
- `rotate_key(provider)` — sets a placeholder rotation value in the environment and records metadata. The operator must replace the placeholder with the real key from the provider console.
- `rotate_keys(providers)` — rotates multiple keys in one call.
- `audit_access(profile)` — returns the canonical tools, MCP servers, skills, files, and actions for a profile.
- `validate_access(profile, resource, action)` — returns an allow/deny decision against least-privilege policy.
- `get_model_recommendation(task)` — recommends a provider/model based on task sensitivity.

### Audit logging (`audit_logger.py`)

- `audit_log()` — appends a JSON Lines event to `hermes/profiles/partenon-guardian/data/audit/security.log`.
- `get_audit_logs()` — reads the log with optional filters by event type or profile.
- `prune_audit_logs(retention_days=365)` — removes entries older than the retention period.

### Policy management (`policy_manager.py`)

- `set_policies(profile, permissions)` — writes an active RBAC policy for a profile and flags any permissions that exceed the canonical role.
- `get_policy(profile)` — returns the active policy or the canonical default.

### Secrets manager (`secrets_manager.py`)

- `manage_secrets("list", key_id)` — lists configured secret references with masked fingerprints.
- `manage_secrets("store", key_id, value)` — validates the value against the provider pattern and stores it in the environment.
- `manage_secrets("rotate", key_id, value)` — replaces an existing secret reference.
- `manage_secrets("delete", key_id)` — removes a secret reference from the environment.

### GPU allocator (`gpu_allocator.py`)

- `allocate_gpu(profile, model_name, requested_gpus)` — validates `NVIDIA_API_KEY` presence and returns a deterministic allocation config. It does not call the NVIDIA API in this version.

---

## Key rotation workflow

Partenon recommends rotating production keys every 90 days. The current workflow is semi-automated:

1. The Guardian flags a key as `pending_rotation` based on `rotation_days` or the `_LAST_ROTATED` companion variable.
2. The operator generates a new key in the provider console.
3. The operator updates `.env` with the new key.
4. The operator runs `source .env` or restarts the service so the new value is loaded.
5. The Guardian logs the rotation event with masked fingerprints.

Example:

```bash
# 1. Check status
python - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-guardian/skills/security/tools")
from key_manager import list_keys
for k in list_keys():
    print(k)
PY

# 2. Rotate placeholder (operator must still replace .env)
python - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-guardian/skills/security/tools")
from key_manager import rotate_key
print(rotate_key("stripe"))
PY

# 3. Log the event
python - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-guardian/skills/security/tools")
from audit_logger import audit_log
print(audit_log(
    event_type="rotation",
    profile="partenon-guardian",
    resource="STRIPE_SECRET_KEY",
    action="rotate",
    status="success",
    message="Stripe key rotated by operator."
))
PY
```

---

## Permission model

Each hero profile declares the tools, MCP servers, skills, files, and actions it needs in `.security` and `policy_manager.py`. The Guardian compares the active policy against a canonical role and reports violations.

Canonical roles are defined in `policy_manager.py` (`_CANONICAL_ROLES`). Examples:

| Profile | Tools | MCP servers | Skills | Files |
|---------|-------|-------------|--------|-------|
| `partenon-guardian` | terminal, file, gbrain | gbrain | security | `partenon-guardian/**` |
| `partenon-tesorero` | terminal, file | none | finance | `partenon-tesorero/**` |
| `partenon-cobrador` | terminal, file | none | payments | `partenon-cobrador/**` |
| `partenon-brain` | terminal, file, gbrain | gbrain | memory | `partenon-brain/**` |

In a production deployment, these roles should be enforced by the orchestrator, container runtime, or secrets manager, not only by Python code.

---

## Audit log format

Each security event is a JSON Lines record:

```json
{
  "id": "uuid",
  "timestamp": "2026-06-26T21:00:00+00:00",
  "event_type": "access|rotation|policy|system",
  "profile": "partenon-cobrador",
  "resource": "STRIPE_SECRET_KEY",
  "action": "read",
  "status": "allowed|denied|success|failed",
  "message": "...",
  "metadata": {}
}
```

The log path is `hermes/profiles/partenon-guardian/data/audit/security.log`.

---

## Network and data boundaries

- **Local files:** Hero tools read and write files in the project directory and `data/`. No data leaves the machine unless an external MCP or API is configured.
- **Google Workspace:** Access is scoped to the service account you provide. Use a dedicated service account with minimum required scopes.
- **Stripe:** Use test keys (`sk_test_*`) until you are ready for production. The Collector falls back to local-mode records when no Stripe key is available.
- **G-Brain:** The local MCP server can run against PGLite or Postgres. The database URL is read from the environment; no hard-coded credentials are shipped.
- **Hermes Agent CLI:** Partenon profiles are designed for the Hermes Agent CLI, but the CLI is not bundled. It must be installed separately from Nous Research.

---

## Security checklist before going live

- [ ] `.env` is created from `.env.example` and contains real credentials.
- [ ] `.env` is listed in `.gitignore` and has never been committed.
- [ ] Service account JSON files are stored in a `.gitignore`d directory.
- [ ] Stripe keys are in test mode until you intentionally switch to live.
- [ ] The Guardian has audited every active profile with `key_manager.audit_access()`.
- [ ] API keys are rotated at least every 90 days.
- [ ] The audit log directory has restricted file permissions.
- [ ] The dashboard password in `.env` is not the default `partenon`.
- [ ] You have reviewed `MISSING_IMPLEMENTATION.md` for known security gaps.

---

## What is NOT protected yet

The following gaps are known and tracked in `MISSING_IMPLEMENTATION.md`:

- The Guardian does not integrate with a real secrets manager (HashiCorp Vault, AWS Secrets Manager, etc.). It operates on environment variables only.
- The Guardian does not yet call provider APIs to rotate keys automatically.
- The workflow engine does not enforce permissions at runtime.
- There is no CI pipeline to scan for leaked secrets.

---

## Reporting issues

If you find a security issue in the code, do not open a public issue first. Contact the maintainers privately and provide:

1. The file and function involved.
2. Steps to reproduce.
3. The maximum impact you can demonstrate.
4. Suggested mitigation, if any.
