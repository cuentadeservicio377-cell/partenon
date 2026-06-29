# Release Readiness Audit — Git and Version Hygiene

**Scope:** git status, version metadata, changelog, roadmap/progress consistency
**Auditor:** release-readiness auditor (read-only)
**Date:** 2026-06-29
**Repository:** `/Users/pablomeneses/Documents/Kimi Code/Partenon`
**Branch:** `main`

---

## 1. Git Status

| Check | Result | Evidence |
|---|---|---|
| Working tree clean | **FAIL** | `git status --porcelain` returned two modifications and one untracked directory:<br>` M data/sample_expenses.xlsx`<br>` M data/sample_expenses_report.json`<br>`?? audits/` |
| Branch state | **WARNING** | `git status --branch --porcelain`: `## main...origin/main [ahead 25]`. There are 25 local commits not yet pushed to `origin/main`. |
| Current branch | PASS | `main` (confirmed via `git branch --show-current`). |
| Untracked files | **WARNING** | `audits/` is untracked. Expected, because this audit report is being created in it, but the directory itself should be committed if audit reports are meant to persist. |

**Required action before push:**
- Decide what to do with the two modified `data/` files.
  - `data/sample_expenses_report.json` shows a content change (`1 insertion, 1 deletion`).
  - `data/sample_expenses.xlsx` is a binary file whose size changed (`8280 -> 8280` bytes, still modified).
  - These look like regenerated demo artifacts. Either commit them intentionally if they represent intended sample output, or revert them and add the pattern to `.gitignore` if they are generated.

---

## 2. Recent Commit History

| Check | Result | Evidence |
|---|---|---|
| Recent commits present | PASS | `git log --oneline -10` shows a clear linear history with conventional commits:<br>`9bdb8ea feat(deploy): close Phase 6 with production Docker stack, CI/CD, metrics and release process`<br>`9dd714e feat(gateway): close Phase 5 with Hermes-native gateway skill and API dry-run endpoint`<br>`5519ebf docs(readme): update status, roadmap, and known gaps after MCP unification sprint`<br>`653f471 fix(runtime): migrate API store, workflow engine, and integrations to partenon-memory MCP`<br>`fabd2b1 fix(packaging): Hermes distribution repair — core skill path, Brain profile, manifests, console scripts, wheel/sdist`<br>`f166da2 feat(api): Phase 4 real-time dashboard + FastAPI backend, JWT, SSE, workspace isolation`<br>`70de957 feat(phase-3): real integrations - Google Workspace, Stripe, Slack, Guardian`<br>`9dce278 feat(phase-2): complete hero final design + MCP wrappers`<br>`8189d61 docs(hermes): add operating modes, MCP tools, and dry-run/live tables to all hero profiles`<br>`90a1afc feat(phase-2): extend MCP servers with full tool lists and align profile permissions` |

---

## 3. Version Metadata (`pyproject.toml`)

| Check | Result | Evidence |
|---|---|---|
| Version declared | PASS | `pyproject.toml` line 7: `version = "1.0.0"`. |
| Version matches latest changelog release | **FAIL** | `CHANGELOG.md` has no `## [1.0.0]` section; the latest dated heading is `## 2026-06-25`, and everything since is under `[Unreleased]`. The package version is pinned to `1.0.0` but no release notes exist for that version. |
| Build backend configured | PASS | `build-system` uses `hatchling`. |
| Console scripts defined | PASS | `partenon-router`, `partenon-onboard`, `partenon-workflow`, `partenon-eval` declared at lines 68–72. |
| Classifiers | WARNING | Classifier `Development Status :: 3 - Alpha` is correct for the current state, but note the project is claiming production Docker/CI/CD while still labeled Alpha. Not a blocker, just a narrative inconsistency. |

**Required action before push:**
- Either move the `[Unreleased]` content into a `## [1.0.0] - 2026-06-29` section (if this is the 1.0.0 release), or keep `[Unreleased]` and bump `pyproject.toml` to a pre-release version such as `1.0.0-dev` or `0.9.0`.

---

## 4. Changelog (`CHANGELOG.md`)

| Check | Result | Evidence |
|---|---|---|
| File exists and is readable | PASS | `CHANGELOG.md` present. |
| `[Unreleased]` not empty | **WARNING** | `[Unreleased]` contains the entire Phase 6 deployment work (lines 5–23): Dockerfile, docker-compose, CI/CD, metrics, release process, 26 new tests. If the repo is meant to be released now, these entries should be moved under a versioned heading. |
| Release instructions present | PASS | `docs/RELEASE.md` exists and `scripts/bump_version.py` is referenced in the changelog line 14. |
| Date-based fallback section | PASS | `## 2026-06-25` section exists for pre-1.0.0 work. |

**Required action before push:**
- Close out `[Unreleased]` into a `1.0.0` section before tagging/pushing as a release.

---

## 5. Roadmap / Progress Consistency

| Check | Result | Evidence |
|---|---|---|
| `TODOS.md` current phase | **FAIL / INCONSISTENT** | `TODOS.md` line 9 declares **"Phase 0 — Contaminants Cleanup"** as the current phase. That phase is marked complete (all checkboxes `[x]` lines 12–22). |
| `PROGRESS.md` current phase | PASS | `PROGRESS.md` line 5 states "Phase 6 Deployment World: production Docker stack, CI/CD, metrics, and release process" and line 26 says "Phase 6 closed; repository is ready for Phase 7 — Website Reality." |
| `TODOS.md` pending phase | PASS | `TODOS.md` line 106 lists **"Phase 7 — Website Reality"** as the pending phase. |
| Cross-document agreement | **FAIL** | `TODOS.md` says current phase is Phase 0, while `PROGRESS.md` and `CHANGELOG.md`/git history confirm Phase 6 is closed and Phase 7 is next. This is stale metadata. |

**Required action before push:**
- Update `TODOS.md` "Current Phase" to **"Phase 7 — Website Reality"** (or mark Phase 6 as closed and Phase 7 as current).

---

## 6. Version Tags

| Check | Result | Evidence |
|---|---|---|
| Git tag for `1.0.0` | **WARNING** | `git describe --tags --always` returned commit hash `9bdb8ea`, meaning no tags exist on the current branch. A release push would normally be accompanied by a `v1.0.0` tag. |

**Required action before push:**
- If this is a release, create and push a `v1.0.0` tag after the changelog is closed out.
- If this is not a release, consider whether the branch should be pushed without a tag.

---

## 7. Executive Summary

### Verdict: **NOT READY** to push as a release.

The repository is functionally complete through Phase 6 (per `PROGRESS.md` and recent commits), but it has git/version hygiene blockers that should be resolved before commit and push.

### Blockers (priority order)

1. **Uncommitted working-tree changes** — `data/sample_expenses.xlsx` and `data/sample_expenses_report.json` are modified. These must be committed intentionally (if they are intended sample artifacts) or reverted (if they are generated by demos/tests).
2. **Version/changelog mismatch** — `pyproject.toml` declares `1.0.0`, but `CHANGELOG.md` still places all recent work under `[Unreleased]` with no `## [1.0.0]` section.
3. **Stale phase metadata in `TODOS.md`** — `TODOS.md` claims the current phase is "Phase 0", while `PROGRESS.md` and git history confirm Phase 6 is closed and Phase 7 is next.
4. **Unpushed commits** — The local `main` branch is 25 commits ahead of `origin/main`. This is not a blocker per se, but the above items should be cleaned up before those 25 commits are pushed.

### Non-blocker warnings

- `audits/` directory is untracked (expected for this report).
- No `v1.0.0` git tag exists yet.
- `Development Status :: 3 - Alpha` classifier contrasts with the production-ready Docker/CI claims.

---

**Recommendation:** Clean the working tree, update `CHANGELOG.md` and `TODOS.md` to reflect Phase 6 closure / Phase 7 start, reconcile `pyproject.toml` version with the changelog, and only then push.
