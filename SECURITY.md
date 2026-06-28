# Security Policy

This document describes how credentials are handled in Partenon and how to report security issues.

## Credential storage

- All secrets live in environment variables or a dedicated secrets manager.
- `.env` is never committed to version control. See `.env.example` for the required variables.
- Profile templates (`.finance`, `.design`, `.security`, etc.) must not contain real keys or passwords.
- API keys and tokens are rotated on suspicion of exposure and logged via the Guardian.

## Reporting vulnerabilities

If you discover a security issue, please email the maintainers privately. Do not open a public issue until the problem is acknowledged and a fix is available.

**Email template:**

```
To: security@partenon.example.com
Subject: [Security] Short description of the issue

Description:
- What is the issue?
- Which component or file is affected?
- Steps to reproduce (if applicable).
- Potential impact.
- Suggested fix (optional).
```

## Guardian responsibilities

The `partenon-guardian` profile owns security hygiene:

- Audit active API keys and flag keys older than 90 days.
- Validate profile permissions against `.security` templates.
- Log rotation and access events to `data/audit/security.log`.
- Alert when a profile requests access outside its least-privilege scope.

For operational runbooks, see `workshop/guides/` and `docs/API.md`.
