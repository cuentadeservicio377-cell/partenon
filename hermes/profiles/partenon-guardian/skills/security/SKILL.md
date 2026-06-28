# Skill: security

Security functions for Partenon Guardian profiles.

## Functions

### list_keys()

Return a table of all configured API keys.

Output fields:

- `provider`: external provider name.
- `key_id`: short identifier or environment variable name.
- `fingerprint`: first and last four characters of the key, masked in between.
- `status`: `active`, `expired`, `revoked`, or `pending_rotation`.
- `last_rotated`: ISO 8601 timestamp or `never`.

Rules:

- Never print the full key.
- Mark keys older than 90 days as `pending_rotation`.

### rotate_key(provider)

Rotate the API key for a provider.

Steps:

1. Validate that the provider is known and configured.
2. Generate or request a new key from the provider console or CLI.
3. Update the environment variable or secrets manager reference.
4. Revoke the previous key once the new one is confirmed working.
5. Record the event in the brain under `security/events/rotations`.

### audit_access(profile)

Audit the permissions assigned to a Partenon profile.

Output fields:

- `profile`: profile name.
- `tools`: list of enabled toolsets.
- `mcp_servers`: list of connected MCP servers.
- `skills`: list of auto-loaded skills.
- `files`: list of file scopes or patterns the profile can access.
- `violations`: list of permissions that exceed the profile's documented role.

Rules:

- Compare against the canonical role definition in `.security` templates.
- Flag any tool, MCP server, or file scope not justified by the role.

### validate_access(profile, resource, action)

Check whether a profile is allowed to perform an action on a resource.

Returns:

- `allowed`: boolean.
- `reason`: short explanation.
- `required_role`: role that would grant access if denied.

Rules:

- Deny by default.
- Require explicit permission in the profile's policy.
- Log every denial under `security/events/access_denied`.

### manage_secrets(action, key_id, value=None, metadata=None)

Vault-style management of API key references.

Actions:

- `list`: return all configured secret references with fingerprints.
- `store`: save a new secret reference.
- `rotate`: replace an existing secret reference.
- `delete`: remove a secret reference.

Rules:

- Never return the full secret value.
- Validate the value against the provider's expected pattern.
- Include a rotation policy in the returned metadata.

### allocate_gpu(profile, model_name, requested_gpus=1, region="us-central")

Allocate NVIDIA GPU resources for a Partenon profile and model.

Output fields:

- `profile`: requesting profile.
- `model`: NVIDIA model identifier.
- `allocated_gpus`: number of GPUs allocated.
- `region`: compute region.
- `status`: `allocated` or `denied`.
- `rate_limits`: requests per minute and tokens per day.
- `estimated_cost_per_hour`: approximate hourly cost.
- `quota_remaining`: GPUs still available under the profile's quota.

Rules:

- Deny the allocation if `NVIDIA_API_KEY` is missing.
- Cap requested GPUs to a safe maximum.
- Return a deterministic configuration object for development and testing.

### set_policies(profile, permissions=None)

Write the active RBAC policy for a profile.

Output fields:

- `profile`: profile name.
- `permissions`: granted tools, MCP servers, skills, files, and actions.
- `violations`: permissions that exceed the canonical role.
- `policy_path`: path to the persisted policy file.

Rules:

- Validate against the canonical role definition.
- Record the policy as JSON for operator review.
- Do not silently drop requested permissions; flag violations instead.

### audit_log(event_type, profile, resource, action, status, message=None, metadata=None)

Append a tamper-evident security event to the audit log.

Output fields:

- `id`: unique event identifier.
- `timestamp`: ISO 8601 timestamp in UTC.
- `event_type`, `profile`, `resource`, `action`, `status`.
- `message`: optional human-readable note.
- `metadata`: optional structured context.

Rules:

- Never include raw secret values in the log entry.
- Write events as JSON Lines under `data/audit/security.log`.
- Support filtering by event type and profile.

## Tools

- `skills/security/tools/key_manager.py`: key listing, rotation, access audit, and model recommendation helpers.
- `skills/security/tools/secrets_manager.py`: vault-style secret storage, rotation, and deletion.
- `skills/security/tools/gpu_allocator.py`: NVIDIA GPU allocation and quota helpers.
- `skills/security/tools/policy_manager.py`: role-based access policy management.
- `skills/security/tools/audit_logger.py`: tamper-evident security event logging.

## MCP Tools

This skill exposes the `partenon-security` MCP server with the following tools:

- `security_list_keys`
- `security_rotate_key`
- `security_audit_access`
- `security_validate_access`
- `security_manage_secrets`
- `security_allocate_gpu`
- `security_set_policy`
- `security_audit_log`

## Dry-run vs live

| Tool | Dry-run behavior | Live requirement |
|---|---|---|
| `security_list_keys` | Reads keys from local environment or config and returns masked fingerprints; no provider APIs are called. | None for read-only inspection. |
| `security_rotate_key` | Simulates provider rotation, returns a synthetic new fingerprint, leaves real keys untouched, and writes a simulated event to the local audit log. | Provider API credentials (e.g., `NVIDIA_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or Twitter/X tokens) and explicit operator approval. |
| `security_audit_access` | Scans profile definitions and local policy files, comparing them against canonical role templates in the repo. | None by default. Optional G-Brain sync requires `GBRAIN_DATABASE_URL`. |
| `security_validate_access` | Evaluates the request against local RBAC policy and returns `allowed` or `denied`. | None by default. |
| `security_manage_secrets` | Operates on a local stub vault; stores, rotates, or deletes references in memory or a local file without touching a real secrets backend. | An integrated secrets manager (e.g., HashiCorp Vault, AWS Secrets Manager, 1Password) configured via its own environment variables. |
| `security_allocate_gpu` | Returns a deterministic allocation object with placeholder quotas and zero cost; no GPU is provisioned. | Valid `NVIDIA_API_KEY` and an NVIDIA cloud account with available quota. |
| `security_set_policy` | Writes the policy to a local JSON file and flags violations without applying it to the orchestrator. | Orchestrator policy API endpoint configured; otherwise remains local. |
| `security_audit_log` | Appends the event to `data/audit/security.log`. | None by default. Optional G-Brain mirroring requires `GBRAIN_DATABASE_URL`. |

No tool in this skill performs payments, dispatches, or other external side effects in dry-run mode. Live mutations require explicit approval.
