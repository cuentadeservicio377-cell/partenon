# Partenon FAQ

Honest answers to questions entrepreneurs and developers actually ask. If something here is not clear, check [`docs/HERO_GUIDE.md`](HERO_GUIDE.md) for technical details and [`docs/ENTREPRENEUR_PLAYBOOK.md`](ENTREPRENEUR_PLAYBOOK.md) for rollout guidance.

---

## 1. Does Partenon replace my accountant?

No. The Scribe organizes expenses, builds dashboards, and flags anomalies, but it does not file taxes, interpret tax law, or sign financial statements. Use it to prepare clean data for your accountant, not to eliminate them.

## 2. Do I need a Hermes Agent subscription?

Not for the local demo. The Python tools in `hermes/profiles/` run without the Hermes CLI. To use the natural-language agent experience described on the website, you need the Hermes Agent CLI from Nous Research, which is distributed separately. `install.sh` and `scripts/setup_hermes.py` detect whether it is installed and give you instructions if it is missing.

## 3. What if I do not use Google Workspace?

Many tools fall back to local files when Google Workspace is not configured:

- Scribe: uses local Excel workbooks via `openpyxl`.
- Strategist: stores projects/tasks in `data/projects.json` and `data/tasks.json`.
- Collector: stores payments in local `.payments`.
- Brain: can use a local SQLite database via `GBrain_DATABASE_URL=sqlite:///data/gbrain.db`.

However, several features are designed around Google Workspace: live Sheets dashboards, Calendar invites, and Gmail reminders. Without it, you get a local-first system.

## 4. What if I do not use Stripe?

The Collector can run in local mode without Stripe credentials. It will create placeholder payment links and record local payments. For real money movement, you need a Stripe account and `STRIPE_SECRET_KEY` in `.env`. Other payment processors are not implemented yet.

## 5. Is my data private?

Local data lives in your repository: `data/`, `output/`, `.finance`, `.design`, `.payments`, etc. Cloud data goes only to the providers you configure (Google, Stripe, OpenRouter). Nothing is sent to a Partenon-owned backend because there is no Partenon-owned backend.

## 6. Where do API keys go?

In `.env` at the project root. Never commit `.env`. Each profile has its own `.env.example`, but in production you should consolidate secrets in the root `.env`. See [`docs/SECURITY.md`](SECURITY.md).

## 7. Why is there a `GBRAIN_DATABASE_URL` vs `GBrain_DATABASE_URL` mismatch?

A naming inconsistency in the repository. `.env.example` uses `GBRAIN_DATABASE_URL`, while `gbrain/server.py` and `partenon-core/config/mcp/servers.yaml` read `GBrain_DATABASE_URL`. Set whichever variable the component you are running expects. This is tracked in [`MISSING_IMPLEMENTATION.md`](../MISSING_IMPLEMENTATION.md).

## 8. Can I run this in production today?

Cautiously. The core tools work, the dashboard builds, and the demo runs. Live integrations require real credentials and are only partially wired. See [`MISSING_IMPLEMENTATION.md`](../MISSING_IMPLEMENTATION.md) for the complete gap list. We recommend running it as a local operations companion first.

## 9. What does the dashboard actually do?

The Next.js dashboard in `dashboard/` reads and writes local JSON files (`data/tasks.json`, `data/cron.json`). It shows a mission kanban, KPI cards, and a cron manager. It is not yet connected to Hermes, G-Brain, or live integrations. See `dashboard/package.json` and `dashboard/src/app/page.tsx`.

## 10. How do I add a new hero?

A hero is a directory under `hermes/profiles/` containing:

- `SOUL.md` — identity and rules
- `config.yaml` — model, tools, MCP servers
- `skills/<skill>/SKILL.md` and `tools/*.py`
- `templates/.<hero>.example`
- optional `cron/*.json`

Then add the profile to `partenon-core/tools/router.py` and `data/cron.json` if you want it routed and scheduled.

## 11. Do I need an NVIDIA account?

Only if you want to use NVIDIA models or the NemoClaw/OpenShell sandbox. The repository defaults to OpenRouter, so an `OPENROUTER_API_KEY` is enough for most heroes. The Guardian supports `NVIDIA_API_KEY` for GPU allocation tracking.

## 12. Can the agents make decisions without me?

Only within narrow, configured boundaries:

- Herald can draft copy and calendars, but social publishing requires `operations.autonomy.publish_social: true`.
- Strategist can create tasks but asks for owners and due dates.
- Diplomat drafts proposals and reminders but does not sign contracts.
- Collector records payments only after Stripe confirms them.

The default posture is "draft and ask for approval."

## 13. What happens when a cron job fails?

Cron jobs are JSON configurations under `hermes/profiles/<profile>/cron/` and `data/cron.json`. They describe what tool to run and when, but there is no production scheduler bundled in the repo. You can run them manually, wire them to your own cron daemon, or use the dashboard cron manager as a starting point.

## 14. Can I use my own LLM instead of OpenRouter?

Yes. Each profile `config.yaml` has a `model.default` field. You can change it to any model string supported by Hermes Agent. The code also supports OpenAI, NVIDIA, and Kimi via environment variables, although the current defaults point to OpenRouter.

## 15. Is the `10 → 1M` counter real?

No. The counter on `web/index.html` is a design projection of adoption milestones, not live tracking. There is no analytics backend updating it.

## 16. How do I report a bug or contribute?

The repository is at `https://github.com/cuentadeservicio377-cell/partenon`. For now, open an issue with a reproducible command, expected output, and actual output. There is no CI yet, so include the result of `python3 scripts/demo_tesorero.py` and `cd dashboard && npm run build`.

## 17. What is the difference between Hermes and the heroes?

Hermes represents the company. It is not a chatbot or a CEO persona. The heroes are specialized agents that take missions from Hermes. This distinction matters because it keeps the system grounded in business operations rather than anthropomorphizing a single assistant.

## 18. Can I run Partenon inside Docker?

Yes. `docker-compose.yml` defines a Postgres service for G-Brain and a dashboard service. It does not include the Hermes Agent or the static web pages. Run:

```bash
docker-compose up --build
```

Then access the dashboard at http://localhost:3000.

---

Still have questions? Read the code, then read [`docs/HERO_GUIDE.md`](HERO_GUIDE.md) and [`docs/API.md`](API.md).
