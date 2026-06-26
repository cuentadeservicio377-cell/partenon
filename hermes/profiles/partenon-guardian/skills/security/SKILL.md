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

## Tools

- `skills/security/tools/key_manager.py`: key listing, rotation, access audit, and model recommendation helpers.
