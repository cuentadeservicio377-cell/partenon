# Partenon Audit Index

This directory contains read-only audits produced by the Kimi Code CLI agent swarm.
Use this index to consult findings before editing the website or pushing a release.

## Website Claims Audits (Phase 7 preparation)

| Report | Scope | Key risk areas |
|--------|-------|----------------|
| [`audit_web_index.md`](audit_web_index.md) | `web/index.html` marketing copy | NVIDIA as core tech, social media/CRM promises, automatic payments, trust badges |
| [`audit_web_heroes.md`](audit_web_heroes.md) | `web/heroes.html` per-hero capabilities | Social network badges, NVIDIA GPU allocation, real-time dashboards, Notion/Tasks badges |
| [`audit_web_developers.md`](audit_web_developers.md) | `web/developers.html` technical claims | Fictional `hermes` CLI, `npx create-hermes`, wrong API endpoints, outdated Docker tab |
| [`audit_cross_cutting.md`](audit_cross_cutting.md) | NVIDIA, Stripe, Hermes, live status across all pages | NVIDIA integration status, Hermes CLI bundling, credential requirements, health/status mocks |

## Release Readiness Audits (pre-push)

| Report | Scope | Verdict |
|--------|-------|---------|
| [`release_readiness_git_and_version_hygiene.md`](release_readiness_git_and_version_hygiene.md) | Git status, version, changelog, tags | TODOS phase stale; data artifacts reverted |
| [`release_readiness_tests_and_lint_verification.md`](release_readiness_tests_and_lint_verification.md) | Tests, lint, compile checks | PASS — 184/184 tests, ruff clean, dashboard build OK |
| [`release_readiness_docker_and_ci_verification.md`](release_readiness_docker_and_ci_verification.md) | Docker, compose, GitHub Actions | PASS — YAML valid, CI covers build/integration |
| [`release_readiness_security_and_secrets_audit.md`](release_readiness_security_and_secrets_audit.md) | Secrets, env files, dockerignore | PASS — no hardcoded secrets found |
| [`release_readiness_documentation_and_consistency.md`](release_readiness_documentation_and_consistency.md) | README, docs, links, consistency | Broken links fixed in this commit |

## How to use these audits

1. Before changing a page, open the matching website report and look for claims marked `incorrect` / `high severity`.
2. When preparing a release, run through the release-readiness reports and resolve any `FAIL` items.
3. After fixes, update this index only if new reports are added.
