# Partenon Workshop Slides

> Speaker notes and slide content. Designed for a 90-minute or 3-hour workshop.

---

## Slide 1: Title

**Partenon: An AI Agent Operating System for Small Business**

*Install it. Choose your heroes. Run your first missions.*

Speaker notes:
- Welcome participants. Set the tone: practical, hands-on, no hype.
- Mention the live site and GitHub repo.

---

## Slide 2: The Problem

**Small businesses drown in operational chaos.**

- Finance: spreadsheets that never reconcile
- Operations: tasks slip through cracks
- Marketing: inconsistent posting
- Payments: late invoices, lost revenue
- Security: credentials scattered across tools
- Relationships: no central client/vendor history

Speaker notes:
- Ask: "Which of these hurts most in your business?" Get a show of hands.

---

## Slide 3: The Idea

**Hermes = your company. The heroes = specialized agents.**

| Hero | Role | Config file |
|------|------|-------------|
| Scribe | Finance | `.finance` |
| Herald | Communications | `.design` |
| Collector | Payments | `.payments` |
| Guardian | Security | `.security` |
| Strategist | Operations | `.ops` |
| Diplomat | Relations | `.relations` |
| Brain | Memory | `.brain` |

Speaker notes:
- Emphasize: Hermes is not a chatbot. It is the company profile that routes missions.
- Each hero has real Python tools, config files, and cron jobs in `hermes/profiles/`.

---

## Slide 4: Architecture

**Four layers**

1. Interface — static site, Next.js dashboard, Hermes CLI
2. Core — router, onboarding engine, workflow engine, eval loop
3. Heroes — seven Hermes Agent distributions
4. Integrations — Google Workspace, Stripe, G-Brain

Speaker notes:
- Show `docs/assets/architecture-diagram.mmd` or the SVG on `web/developers.html`.
- Point to `partenon-core/tools/router.py` as the intent classifier.

---

## Slide 5: What You Will Build Today

By the end of this workshop:

1. Partenon installed locally
2. `config/company.yaml` for your business
3. Config files for 3+ heroes
4. First missions assigned
5. Dashboard running at `http://localhost:3000`

Speaker notes:
- Set expectations: not everything will be live; some integrations need real credentials.

---

## Slide 6: Live Install

```bash
git clone https://github.com/cuentadeservicio377-cell/partenon.git
cd partenon
./install.sh
python3 scripts/demo_tesorero.py
```

Speaker notes:
- Run this live. Narrate each step.
- If install is slow, switch to a pre-prepared machine.

---

## Slide 7: Hero Selection Matrix

| Business type | Activate first |
|---------------|----------------|
| Coffee shop | Scribe → Strategist → Herald → Collector |
| Marketing agency | Strategist → Diplomat → Scribe → Herald → Collector |
| Construction | Strategist → Diplomat → Scribe → Guardian |
| Retail | Scribe → Collector → Herald → Strategist |
| SaaS | Guardian → Scribe → Collector → Strategist → Brain |

Speaker notes:
- Reference `docs/ENTREPRENEUR_PLAYBOOK.md`.
- Explain why the order matters: start with the hero that removes the most friction.

---

## Slide 8: Company Card Example — Philz Coffee

**Real business, real pain points**

- Long wait times, inconsistent speed
- Labor cost unclear by shift
- Pricing pressure (non-dairy upcharges)

Why Partenon:
- Scribe parses POS exports
- Strategist schedules staff
- Herald promotes mobile ordering
- Collector handles catering links

Speaker notes:
- Open `workshop/companies/coffee-shop--philz-coffee.md`.
- Mention sources are public URLs.

---

## Slide 9: Simulation Walkthrough

**Coffee shop onboarding**

1. Hermes interview → `config/company.yaml`
2. Copy templates → `.finance`, `.design`, `.ops`, `.payments`
3. First missions for Scribe, Strategist, Herald, Collector
4. Expected outputs + documented gaps

Speaker notes:
- Walk through `workshop/simulations/coffee-shop.md`.
- Highlight actual CLI commands and Python tool calls.

---

## Slide 10: Hands-On — Your Company Interview

**Questions Hermes asks:**

1. Company name and industry
2. Currency and timezone
3. Employees and locations
4. Top 3 operational pains
5. Tools already in use
6. Final approver for brand, finance, operations

Speaker notes:
- Give participants 5 minutes to answer these for their own business.
- Then help them write `config/company.yaml`.

---

## Slide 11: Config Files

```bash
cp hermes/profiles/partenon-tesorero/templates/.finance.example .finance
cp hermes/profiles/partenon-mensajero/templates/.design.example .design
cp hermes/profiles/partenon-estratega/templates/.ops.example .ops
```

Speaker notes:
- Explain that these are real config files the heroes read.
- Walk through one example, e.g., `.finance` fixed/variable costs.

---

## Slide 12: Smoke Tests

```bash
hermes profile use partenon-tesorero
python3 hermes/profiles/partenon-tesorero/skills/finance/tools/audit.py --weekly

hermes profile use partenon-estratega
python3 hermes/profiles/partenon-estratega/skills/ops/tools/projects.py create "My first project"
```

Speaker notes:
- Run smoke tests live. Celebrate PASS outputs.
- Explain PARTIAL: some heroes need credentials or external integrations.

---

## Slide 13: Dashboard

```bash
cd dashboard
npm install
npm run dev
```

Open `http://localhost:3000`
Login: `admin` / `partenon`

Speaker notes:
- Show the kanban and cron views.
- Mention the dashboard reads local JSON files today.

---

## Slide 14: Gaps and Honest Limits

- Live Google Workspace / Stripe / G-Brain need real credentials.
- Herald drafts content but does not auto-publish to social platforms yet.
- Collector creates local payment records; real links need Stripe keys.
- Brain requires the G-Brain binary/MCP for persistent memory.

Speaker notes:
- Honesty builds trust. Document gaps; do not oversell.
- Point to `MISSING_IMPLEMENTATION.md`.

---

## Slide 15: Your 30-Day Mission Plan

Template:

| Week | Mission | Hero | Success metric |
|------|---------|------|----------------|
| 1 | Upload and classify expenses | Scribe | Margin visible |
| 2 | Create first project + checklist | Strategist | 3 tasks completed |
| 3 | Register top clients/vendors | Diplomat | 5 relationships logged |
| 4 | Set up one payment link | Collector | 1 invoice paid |

Speaker notes:
- Have participants fill this in for their business.
- Encourage starting with one hero, not all seven.

---

## Slide 16: Resources

- Repo: https://github.com/cuentadeservicio377-cell/partenon
- Live site: https://hermespartenon.online/
- Docs: `docs/ENTREPRENEUR_PLAYBOOK.md`, `docs/HERO_GUIDE.md`, `docs/QUICKSTART.md`
- Workshop package: `workshop/`
- Gaps: `MISSING_IMPLEMENTATION.md`

Speaker notes:
- Share these in chat or on a handout.
- Thank participants and open for Q&A.
