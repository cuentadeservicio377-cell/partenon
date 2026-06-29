# Release Readiness Audit — Docker and CI Verification

**Project:** Partenon  
**Auditor:** Kimi Code CLI (subagent)  
**Date:** 2026-06-29  
**Scope:** `Dockerfile`, `.dockerignore`, `docker-compose.yml`, `docker-compose.override.yml`, `dashboard/Dockerfile`, `.github/workflows/ci.yml`, `.github/workflows/release.yml`, plus referenced build/runtime artifacts.

---

## Audit Checks

| # | Check | Result | Evidence | Required Action Before Push |
|---|-------|--------|----------|----------------------------|
| 1 | API `Dockerfile` exists and is readable | PASS | `Dockerfile` (54 lines) present and parsed. Multi-stage build with `builder` and `runner` stages. | None |
| 2 | Dashboard `Dockerfile` exists and is readable | PASS | `dashboard/Dockerfile` (30 lines) present and parsed. Multi-stage Node.js build using `output: 'standalone'`. | None |
| 3 | `.dockerignore` exists and is readable | PASS | `.dockerignore` (50 lines) present. Excludes `.env`, `.env.*` (keeps `.env.example`), `.git/`, `node_modules/`, build artifacts, secrets. | None |
| 4 | `docker-compose.yml` YAML syntax | PASS | `python3 -c "yaml.safe_load(...)"` → `YAML OK` | None |
| 5 | `docker-compose.override.yml` YAML syntax | PASS | `python3 -c "yaml.safe_load(...)"` → `YAML OK` | None |
| 6 | `.github/workflows/ci.yml` YAML syntax | PASS | `python3 -c "yaml.safe_load(...)"` → `YAML OK` | None |
| 7 | `.github/workflows/release.yml` YAML syntax | PASS | `python3 -c "yaml.safe_load(...)"` → `YAML OK` | None |
| 8 | Files referenced by Docker/CI exist | PASS | Verified presence of `pyproject.toml`, `requirements.txt`, `distribution.yaml`, `install.sh`, `dashboard/package.json`, `dashboard/package-lock.json`, `.env.example`. | None |
| 9 | Dashboard standalone output configured | PASS | `dashboard/next.config.ts` sets `output: 'standalone'`, matching `dashboard/Dockerfile` copy of `.next/standalone`. | None |
| 10 | API health endpoints exist | PASS | `partenon_api/main.py:81` `/health`, `:87` `/health/live`, `:93` `/health/ready`. Dockerfile `HEALTHCHECK` targets `/health`. | None |
| 11 | Dashboard login route exists | PASS | `dashboard/src/app/login/page.tsx` exists; Dockerfile `HEALTHCHECK` targets `/login`. | None |
| 12 | `install.sh` syntax (run in CI) | PASS | `bash -n install.sh` → exit code `0`. | None |
| 13 | GitHub Actions action versions current | PASS | Uses `actions/checkout@v4`, `actions/setup-python@v5`, `actions/setup-node@v4`, `docker/setup-buildx-action@v3`, `docker/build-push-action@v5`, `docker/login-action@v3`, `docker/metadata-action@v5`, `softprops/action-gh-release@v2`. None are deprecated. | None |
| 14 | CI integration job `.env` setup | PASS | `.github/workflows/ci.yml:100-106` copies `.env.example` to `.env` and appends required CI secrets (`DASHBOARD_AUTH_SECRET`, `PARTENON_API_SECRET`, `DASHBOARD_APP_USERNAME`, `DASHBOARD_APP_PASSWORD`). | None |
| 15 | Docker daemon available for local build verification | FAIL / ENV | `docker --version` works, but `docker build --check` fails: `failed to connect to the docker API ... check if the path is correct and if the daemon is running`. Local image builds could not be executed. | Start Docker daemon and re-run `docker build` locally, or rely on the CI `docker` job for build verification before push. |
| 16 | Release workflow metadata usage consistency | WARNING | `.github/workflows/release.yml:28-38` generates metadata tags, but `build-push-action` steps use manually constructed tags (`ghcr.io/${{ github.repository }}/api:${{ github.ref_name }}`) instead of `${{ steps.meta.outputs.tags }}`. Labels are consumed. Functional, but the `tags` block in `metadata-action` is effectively unused. | Consider using `${{ steps.meta.outputs.tags }}` for semver/sha tags, or remove unused metadata `tags` config. |
| 17 | Dockerfile source consistency | WARNING | `Dockerfile` copies `partenon_core/`, `mcp_servers/`, `partenon_api/`, `hermes/`, `skills/`, `scripts/`, `data/`, `config/`, `distribution.yaml`. It does **not** copy `web/` or `tests/`, whereas `pyproject.toml` force-includes `web/` and `tests/` in the wheel. Since the API does not serve `web/` static files (verified by grep), this is not a runtime blocker, but it creates a content discrepancy between the wheel and the Docker image. | Document intent or copy `web/` into the image if future releases need it served from the container. |
| 18 | `docker compose` command compatibility | PASS | CI uses `docker compose` (v2 plugin syntax). Modern GitHub Actions runners and local Docker 29.x support this. | None |
| 19 | Container runtime healthchecks | PASS | Both Dockerfiles define `HEALTHCHECK` with reasonable intervals/timeouts/retries. Compose `depends_on` uses `condition: service_healthy`, supported by Compose v2.20+. | None |
| 20 | Release image tags and permissions | PASS | Release workflow sets `permissions: contents: write, packages: write`, logs into `ghcr.io`, and pushes `api` and `dashboard` images tagged with `${{ github.ref_name }}`. | None |

---

## Detailed Findings

### 1. Dockerfiles (API and Dashboard)
- **API**: `python:3.12-slim-bookworm` builder installs build tools and editable package with extras `[workspace,payments,slack,db]`. Runner stage installs `curl` and `libpq5` (required by `psycopg2-binary`), creates non-root `partenon` user, exposes `8000`, defines healthcheck, and runs `uvicorn`.
- **Dashboard**: `node:20-alpine` with `npm ci`, `npm run build`, standalone output, non-root `nextjs` user, exposes `3000`, healthchecks `/login`, and runs `node server.js`.
- No Dockerfile syntax errors detected by static inspection.

### 2. Docker Compose
- `docker-compose.yml` defines `gbrain` (Postgres 16), `api`, and `dashboard` services on a private `partenon` bridge network.
- Service dependencies use `condition: service_healthy`, matching the `HEALTHCHECK` instructions.
- Environment variables and `.env` file wiring are consistent with `.env.example`.
- Override file bind-mounts source for local dev reload without breaking production compose.

### 3. CI Workflow
- Four jobs: `python`, `dashboard`, `docker`, `integration`.
- `python` installs editable package with `[all]` extras, runs pytest, ruff, install-script syntax check, and secret scan.
- `dashboard` installs Node deps, lints, and builds with CI-only auth secrets.
- `docker` builds both images with Buildx and GHA cache.
- `integration` starts the full stack, verifies `/health/ready` and `/login`, and tears down with `if: always()`.

### 4. Release Workflow
- Triggered on `v*.*.*` tags.
- Pushes both `api` and `dashboard` images to GHCR.
- Creates a GitHub release and attaches `CHANGELOG.md`.
- Warning: metadata-action `tags` block is not wired into build-push-action.

---

## Executive Summary

**Verdict:** The repository is **ready to commit and push from a Docker/CI static-analysis perspective**, with **no hard blockers** in the Dockerfiles, Compose files, or workflow definitions.

**Blockers (none).**

**Recommended pre-push actions (priority order):**

1. **Verify image builds actually pass.** The local Docker daemon was not running, so real image builds could not be confirmed. Either start the daemon locally and run `docker build -f Dockerfile .` and `cd dashboard && docker build -f Dockerfile .`, or merge and watch the CI `docker` job on the first push.
2. **(Optional) Clean up release metadata wiring.** In `.github/workflows/release.yml`, use `${{ steps.meta.outputs.tags }}` in the `build-push-action` `tags` input, or remove the unused `tags` block from `docker/metadata-action` to avoid confusion.
3. **(Optional) Reconcile `web/` inclusion.** Decide whether `web/` should be copied into the API image; if it is only packaged for the wheel/sdist and not served by the container, document that intent.

**Files audited:**
- `Dockerfile`
- `.dockerignore`
- `docker-compose.yml`
- `docker-compose.override.yml`
- `dashboard/Dockerfile`
- `.github/workflows/ci.yml`
- `.github/workflows/release.yml`
- Cross-referenced: `pyproject.toml`, `requirements.txt`, `distribution.yaml`, `dashboard/next.config.ts`, `dashboard/package.json`, `dashboard/package-lock.json`, `install.sh`, `.env.example`, `partenon_api/main.py`, `dashboard/src/app/login/page.tsx`.
