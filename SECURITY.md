# Partenon Security Policy

## Credentials

- All secrets live in environment variables or a secrets manager. Start from `.env.example` and never commit `.env`.
- Rotate API keys (OpenRouter, Stripe, Google service accounts, NVIDIA) at least every 90 days or after personnel changes.
- The Guardian profile tracks key status and rotation deadlines.

## Reporting a vulnerability

If you discover a security issue, please email the maintainers:

```
To: security@example.com
Subject: [Partenon] Vulnerability report

- Summary:
- Affected files / components:
- Steps to reproduce:
- Possible impact:
- Suggested fix (optional):
```

Do not open a public issue for sensitive vulnerabilities.

## Guardian responsibilities

The Guardian hero is responsible for:

- Auditing profile access and tool permissions.
- Enforcing key rotation and logging rotation events.
- Reviewing `.env` and profile env files for leaked secrets.
- Running weekly security audits and pruning old audit logs.

See `docs/SECURITY.md` and `docs/HERO_GUIDE.md` for the full Guardian runbook.

## Useful references

- `.env.example` — required environment variables and placeholders.
- `docs/SECURITY.md` — detailed threat model and operational checklist.
- `hermes/profiles/partenon-guardian/skills/security/tools/` — Guardian tools.
