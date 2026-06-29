# Release Process

Partenon follows [Semantic Versioning](https://semver.org/) and releases are
created from git tags. Images are published automatically to the GitHub
Container Registry (GHCR) by `.github/workflows/release.yml`.

## Before releasing

1. Make sure the `main` branch is green (CI passes).
2. Update `CHANGELOG.md` under `## [Unreleased]` with user-facing changes.
3. Decide the version bump:
   - `patch` for bug fixes and small improvements.
   - `minor` for new features that are backwards compatible.
   - `major` for breaking changes.

## Create a release

```bash
python3 scripts/bump_version.py patch --tag
```

This will:
- Bump the version in `pyproject.toml`.
- Add a dated section to `CHANGELOG.md`.
- Create a signed-ish lightweight annotated git tag `vX.Y.Z`.

Push the commit and tag:

```bash
git push origin main
git push origin vX.Y.Z
```

Or use the helper:

```bash
python3 scripts/bump_version.py patch --tag --push
```

## What happens next

The `Release` GitHub Actions workflow triggers on the tag and:
1. Builds and pushes `ghcr.io/<owner>/partenon/api:vX.Y.Z`.
2. Builds and pushes `ghcr.io/<owner>/partenon/dashboard:vX.Y.Z`.
3. Creates a GitHub Release with auto-generated notes.

## Docker image tags

| Tag | Example | Notes |
|-----|---------|-------|
| Semver | `v1.0.0` | Exact release |
| Minor | `v1.0` | Latest patch in the minor line |
| Short SHA | `sha-abc1234` | Per-commit builds (only on CI) |

## Production checklist

- [ ] `.env` is created from `.env.example` and secrets are real.
- [ ] `GBRAIN_DATABASE_URL` points to a managed Postgres with backups.
- [ ] `PARTENON_API_SECRET` and `DASHBOARD_AUTH_SECRET` are at least 32 chars.
- [ ] Dashboard is served over HTTPS.
- [ ] `DASHBOARD_ORIGIN` matches the public dashboard URL.
- [ ] A reverse proxy (nginx, Traefik, Caddy) terminates TLS in front of both services.
- [ ] Health endpoints (`/health`, `/health/ready`, `/metrics`) are monitored.
