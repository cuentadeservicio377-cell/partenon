# Partenon Hermes Onboarding Workshop — Slide Deck

A facilitator slide deck in Markdown. Each top-level heading is a slide.

---

## Partenon Hermes Onboarding Workshop

**Goal:** Onboard a real small business in 90 minutes and leave with a production-readiness scorecard.

---

## What Partenon is

- Seven hero profiles around one shared business context.
- Hermes is the company, not the CEO.
- Each hero owns a domain: money, message, money-in, security, operations, relationships, memory.

---

## The seven heroes

| Hero | Spanish name | Domain |
|---|---|---|
| Scribe | Tesorero | Finance |
| Herald | Mensajero | Communications |
| Collector | Cobrador | Payments |
| Guardian | Guardian | Security |
| Strategist | Estratega | Operations |
| Diplomat | Diplomatico | Relationships |
| Brain | Cerebro | Memory / G-Brain |

---

## Why onboarding matters

- A hero without context generates generic output.
- Onboarding creates `.finance`, `.design`, `.payments`, `.security`, `.ops`, `.relations`, and `.brain`.
- These files are the contract between the founder and the agents.

---

## The five case studies

1. **Joe Coffee Company** — New York coffee shop / roaster
2. **Single Grain** — digital marketing agency
3. **SpawGlass** — Texas commercial construction contractor
4. **Tracksmith** — athletic apparel retail / e-commerce
5. **Buffer** — bootstrapped social-media SaaS

Each card includes real revenue, headcount, pain points, and sources.

---

## Pick a business: what changes?

| Type | First hero | Urgent question |
|---|---|---|
| Coffee shop | Scribe | Do we know our margin? |
| Agency | Strategist | Which client is at risk? |
| Construction | Strategist | Is the permit on track? |
| Retail | Scribe | Which category is profitable? |
| SaaS | Guardian | Are our keys and access clean? |

---

## Router demo

```bash
python3 workshop/simulations/sim_runner.py route "organize my numbers"
python3 workshop/simulations/sim_runner.py route "create a campaign"
python3 workshop/simulations/sim_runner.py route "invoice a client"
```

The router is rule-based today. It scores keywords and regex patterns. It will improve when it loads profile metadata dynamically.

---

## Simulation flow

For the chosen business:

1. Herald — brand interview (`.design`)
2. Strategist — first project + tasks + checklist
3. Diplomat — client/vendor + milestone
4. Collector — payment link or invoice
5. Herald — content calendar
6. Strategist — morning briefing
7. Guardian — key audit

---

## What works today vs. what needs wiring

**Green:** local project, task, checklist, client, vendor, milestone, calendar, briefing, key audit.

**Yellow:** payment links and invoices work locally but need `STRIPE_SECRET_KEY` for live Stripe.

**Red:** Gmail/Contacts dispatch, social publishing, G-Brain memory, real Google Sheets, and some industry-specific templates are not implemented.

---

## Production-readiness scorecard

Use `workshop/checklists/PRODUCTION_READINESS.md` to score:

- Core platform (router, workflow, eval loop, onboarding)
- Hero profiles
- Integrations (Google, Stripe, G-Brain, Gmail)
- Testing and quality

Classify each item: green / yellow / red.

---

## What to do next

1. Create `config/company.yaml` for your company.
2. Complete the brand interview.
3. Activate the first 2–4 heroes.
4. Connect live credentials for yellow items.
5. Schedule engineering for red items.

---

## Resources

- `docs/ENTREPRENEUR_PLAYBOOK.md` — copy-paste prompts
- `docs/HERO_GUIDE.md` — tool and env reference
- `workshop/guides/HERMES_ONBOARDING.md` — full onboarding guide
- `workshop/simulations/` — five runnable simulations
- `workshop/checklists/PRODUCTION_READINESS.md` — go-live checklist

---

## Workshop closing

- Verify `python3 scripts/demo_tesorero.py` passes.
- Verify `cd dashboard && npm run build` passes.
- Update `MISSING_IMPLEMENTATION.md` and `TODOS.md`.
- Commit the workshop package.
