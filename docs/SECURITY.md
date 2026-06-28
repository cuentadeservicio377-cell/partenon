# Partenon Security Guide

This document describes the security model that is actually implemented in the repository. It is written for operators and developers who need to store credentials, rotate keys, and audit access.

For the full list of Guardian tools, see [`docs/HERO_GUIDE.md`](HERO_GUIDE.md). For the entrepreneur rollout checklist, see [`docs/ENTREPRENEUR_PLAYBOOK.md`](ENTREPRENEUR_PLAYBOOK.md).

---

## 1. Threat model

Partenon is designed for small businesses that already use Google Workspace, Stripe, and one or more AI providers. The main risks we address are:

1. **Credential leakage** — API keys, service accounts, and tokens must not be committed or logged.
2. **Over-permissioned heroes** — each profile should only access the tools and files it needs.
3. **Stale keys** — production keys should be rotated periodically and after personnel changes.
4. **No audit trail** — security events must be recorded with timestamps and actors.

---

## 2. `.env` handling

The global environment file is created from [`.env.example`](../.env.example) by `install.sh` or `scripts/setup_hermes.py`.

### Rules

- `.env` is listed in `.gitignore` and must **never** be committed.
- Only placeholder keys are stored in `.env.example`. Real secrets are filled in locally.
- Tools read secrets from environment variables, never from chat logs or profile files.

### Required secrets

| Variable | Used by | File that reads it |
|----------|---------|-------------------|
| `OPENROUTER_API_KEY` | All heroes that use LLMs | Every profile `config.yaml` |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Google Workspace integrations | `partenon_core/config/mcp/servers.yaml`, Scribe, Strategist, Diplomat, Herald |
| `STRIPE_SECRET_KEY` | Collector payments | `hermes/profiles/partenon-collector/.env.example`, `stripe_tools.py` |
| `GBRAIN_DATABASE_URL` / `GBrain_DATABASE_URL` | Brain / G-Brain | `gbrain/server.py` reads `GBrain_DATABASE_URL`; `.env.example` uses `GBRAIN_DATABASE_URL` |

> **Known issue**: the repository has a naming inconsistency. `gbrain/server.py` and `partenon_core/config/mcp/servers.yaml` default to `GBrain_DATABASE_URL`, while `.env.example` documents `GBRAIN_DATABASE_URL`. Set the exact variable name required by the component you run. This is tracked in [`MISSING_IMPLEMENTATION.md`](../MISSING_IMPLEMENTATION.md).

### Local profile env files

Each hero has its own `hermes/profiles/<profile>/.env.example`. In production, consolidate these into the root `.env` rather than maintaining separate files.

---

## 3. Google service accounts

Partenon uses a Google Cloud service account JSON to access Sheets, Docs, Slides, Drive, Calendar, and Gmail.

### How to create one

1. Go to [Google Cloud Console](https://console.cloud.google.com/) → IAM & Admin → Service Accounts.
2. Create a service account for `Partenon`.
3. Generate a JSON key and download it.
4. Store the JSON file outside the repo (e.g., `~/.secrets/partenon-google.json`).
5. Set `GOOGLE_SERVICE_ACCOUNT_JSON=/absolute/path/to/key.json` in `.env`.

### Recommended scopes

The Scribe's [`google_sheets.py`](../hermes/profiles/partenon-scribe/skills/finance/tools/google_sheets.py) requests:

```python
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
```

For Calendar and Gmail access, enable the corresponding APIs in Google Cloud and add the minimum scopes your use case requires. Do not use a domain-wide delegation unless necessary.

### Storage rule

The service account JSON is a credential. Treat it like a private key: keep it out of Git, out of screenshots, and out of chat logs.

---

## 4. Stripe key rotation

The Collector handles Stripe via [`stripe_tools.py`](../hermes/profiles/partenon-collector/skills/payments/tools/stripe_tools.py). The Guardian is responsible for rotating the key.

### What the Guardian does

The Guardian's [`key_manager.py`](../hermes/profiles/partenon-guardian/skills/security/tools/key_manager.py) tracks providers including Stripe:

```python
_PROVIDER_CONFIG = {
    "stripe": {
        "env_var": "STRIPE_SECRET_KEY",
        "pattern": r"^sk_(test|live)_[A-Za-z0-9]+$",
    },
}
```

Functions:

- `list_keys()` — shows provider, env var, masked fingerprint, status (`active` / `pending_rotation` / `missing`), and last rotation date.
- `rotate_key(provider)` — updates the environment variable reference and timestamp. It does **not** call Stripe APIs; you replace the real key through your provider console or secrets manager.
- `rotate_keys(providers)` — rotates multiple providers in one call.

### Safe rotation sequence

1. Generate a new restricted Stripe key in the Stripe Dashboard.
2. Update your `.env` or secrets manager with the new key.
3. Run the Guardian: `Guardian, rotate the Stripe secret key and log the event.`
4. Verify the Collector still works (e.g., create a test payment link).
5. Revoke the old key in Stripe.

### Key status logic

A key is marked `pending_rotation` if:

- it has never been rotated, or
- its last rotation timestamp is older than 90 days (`_ROTATION_INTERVAL_DAYS = 90`).

You can override this by setting a companion env var such as `STRIPE_SECRET_KEY_LAST_ROTATED=2026-06-26T00:00:00Z`.

---

## 5. Guardian responsibilities

The Guardian is the security profile. Its tool set lives in [`hermes/profiles/partenon-guardian/skills/security/tools/`](../hermes/profiles/partenon-guardian/skills/security/tools/).

### Access auditing

`audit_access(profile)` returns the canonical tools, MCP servers, skills, files, and actions for a profile. It compares the requested profile against a hard-coded canonical map in `key_manager.py`. In production, you would load this from `.security` instead.

Example:

```python
from hermes.profiles.partenon-guardian.skills.security.tools.key_manager import audit_access
print(audit_access("partenon-collector"))
```

### Policy management

`policy_manager.py` writes RBAC policies as JSON files under the profile's `data/policies/` directory:

```python
from hermes.profiles.partenon-guardian.skills.security.tools.policy_manager import set_policies
set_policies("partenon-scribe", permissions={
    "tools": ["terminal", "file"],
    "mcp_servers": ["google_workspace", "gbrain"],
    "skills": ["finance"],
    "files": ["hermes/profiles/partenon-scribe/**"],
    "actions": ["read_financial_data"],
})
```

### Audit logging

`audit_logger.py` appends JSON Lines events to:

```text
hermes/profiles/partenon-guardian/data/audit/security.log
```

Each event contains:

- `id` — UUID
- `timestamp` — ISO 8601 UTC
- `event_type` — e.g., `access`, `rotation`, `policy`
- `profile` — which profile triggered the event
- `resource` — what was accessed or modified
- `action` — what was attempted
- `status` — `allowed`, `denied`, `success`, `failed`
- `message` and `metadata`

Example:

```python
from hermes.profiles.partenon-guardian.skills.security.tools.audit_logger import audit_log
audit_log(
    event_type="rotation",
    profile="partenon-guardian",
    resource="STRIPE_SECRET_KEY",
    action="rotate_key",
    status="success",
    message="Stripe key rotated manually",
)
```

Read logs with:

```python
from hermes.profiles.partenon-guardian.skills.security.tools.audit_logger import get_audit_logs
print(get_audit_logs(profile="partenon-collector", limit=10))
```

### GPU allocation

`gpu_allocator.py` returns a deterministic allocation object for NVIDIA GPU use. It denies allocation if `NVIDIA_API_KEY` is missing.

---

## 6. Secret masking

The Guardian never prints full secrets. `key_manager._fingerprint(value)` returns a masked string:

```python
_fingerprint("sk_test_1234567890abcdef")  # "sk_t...cdef"
```

The eval loop in [`partenon_core/tools/eval_loop.py`](../partenon_core/tools/eval_loop.py) also scans outputs for unsafe patterns and subtracts points if it finds:

```python
unsafe_patterns = ["sk-", "pk-", "nvapi-", "-----BEGIN", "PRIVATE KEY", "password", "secret", "token"]
```

---

## 7. Security checklist

- [ ] `.env` is in `.gitignore` and not committed.
- [ ] Service account JSON is stored outside the repo.
- [ ] Stripe keys use restricted, company-owned keys rather than personal test keys.
- [ ] The Guardian weekly audit cron job is enabled (`hermes/profiles/partenon-guardian/cron/weekly-audit.json`).
- [ ] Every rotation event is written to `security.log`.
- [ ] Each hero profile's permissions are documented in `.security`.
- [ ] No profile file contains raw secret values.
- [ ] Dashboard credentials are changed from the default `admin` / `partenon` (`DASHBOARD_APP_USERNAME`, `DASHBOARD_APP_PASSWORD`).

---

## 8. What is not implemented yet

See [`MISSING_IMPLEMENTATION.md`](../MISSING_IMPLEMENTATION.md) for the complete gap list. Security-specific gaps include:

- No real secrets-manager integration (HashiCorp Vault, AWS Secrets Manager, etc.). Keys are read from env vars only.
- No automated audit log retention enforcement outside `prune_audit_logs()`.
- No real NVIDIA NeMoClaw / OpenShell integration.
- The Guardian's canonical roles are hard-coded in `key_manager.py`; they should be loaded from `.security` templates at runtime.
