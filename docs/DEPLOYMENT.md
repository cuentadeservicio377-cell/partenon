# Deployment Guide

This document explains how to run Partenon in production using Docker Compose.

## Quick start (local)

1. Copy the environment template and add real credentials:

   ```bash
   cp .env.example .env
   # Edit .env and set secrets and integration credentials.
   ```

2. Start the stack:

   ```bash
   docker compose up --build -d
   ```

3. Verify services:

   ```bash
   curl http://localhost:8000/health/ready
   curl -I http://localhost:3000/login
   ```

4. Stop the stack:

   ```bash
   docker compose down
   ```

## Services

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| `gbrain` | `postgres:16-alpine` | `5432` | Persistent memory store for the `partenon-memory` MCP server. |
| `api` | `Dockerfile` | `8000` | FastAPI backend and MCP runtime. |
| `dashboard` | `dashboard/Dockerfile` | `3000` | Next.js Mission Control dashboard. |

## Development override

For live reload while working on the API:

```bash
docker compose -f docker-compose.yml -f docker-compose.override.yml up --build
```

## Required environment variables

| Variable | Purpose |
|----------|---------|
| `PARTENON_API_SECRET` | JWT signing secret (≥ 32 chars). |
| `DASHBOARD_AUTH_SECRET` | Dashboard session secret (≥ 32 chars). |
| `DASHBOARD_APP_USERNAME` | Dashboard login username. |
| `DASHBOARD_APP_PASSWORD` | Dashboard login password. |
| `GBRAIN_DATABASE_URL` | Postgres URL for the memory MCP server. |
| `OPENROUTER_API_KEY` | LLM provider key. |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Path or JSON for Google Workspace. |
| `STRIPE_SECRET_KEY` | Stripe secret key. |
| `SLACK_BOT_TOKEN` | Slack bot token for Strategist notifications. |

The Docker Compose file overrides `GBRAIN_DATABASE_URL` to point at the
`gbrain` Postgres service.

## Health endpoints

| Endpoint | Service | Use |
|----------|---------|-----|
| `GET /health` | API | Liveness probe. |
| `GET /health/live` | API | Kubernetes-style liveness. |
| `GET /health/ready` | API | Readiness probe; checks memory store. |
| `GET /metrics` | API | Prometheus metrics. |
| `GET /login` | Dashboard | Basic availability. |

## Production checklist

- [ ] Replace all placeholder secrets with strong, unique values.
- [ ] Use a managed Postgres instance with automated backups.
- [ ] Serve the dashboard and API over HTTPS.
- [ ] Set `DASHBOARD_ORIGIN` to the public dashboard URL.
- [ ] Place a reverse proxy (nginx, Traefik, Caddy) in front of both services.
- [ ] Monitor `/health/ready` and `/metrics`.
- [ ] Pin image tags instead of using `:latest`.
- [ ] Run `docker compose pull` before updates and keep backups of `./data`.

## Releasing

See [docs/RELEASE.md](RELEASE.md).
