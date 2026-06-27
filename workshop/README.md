# Partenon Hermes Onboarding Workshop

A hands-on workshop package for onboarding real small businesses onto Partenon. It includes five researched case studies, five runnable simulations, a facilitator guide, slides, a handout, and a production-readiness checklist.

---

## What is in this package

```
workshop/
├── README.md                          # This file
├── AGENDA.md                          # 90-minute workshop agenda
├── SLIDES.md                          # Facilitator slide deck
├── HANDOUT.md                         # One-page participant handout
├── companies/                         # Real small business case studies
│   ├── coffee-shop--oblique-coffee-roasters.md
│   ├── agency--envision-creative.md
│   ├── construction-company--flintrock-operating.md
│   ├── retail--greenlight-bookstore.md
│   └── saas--plausible-analytics.md
├── simulations/                       # Step-by-step onboarding runs
│   ├── 01-coffee-shop-onboarding.md
│   ├── 02-agency-onboarding.md
│   ├── 03-construction-company-onboarding.md
│   ├── 04-retail-onboarding.md
│   ├── 05-saas-onboarding.md
│   ├── sim_runner.py                  # Standalone runner for all simulations
│   └── run_all_sims.sh                # Reproduce every simulation
├── guides/
│   └── HERMES_ONBOARDING.md           # Complete onboarding guide
└── checklists/
    └── PRODUCTION_READINESS.md        # Go-live verification checklist
```

---

## Quick start

1. Install and verify Partenon:
   ```bash
   ./install.sh
   python3 scripts/demo_tesorero.py
   ```

2. Run all five simulations:
   ```bash
   bash workshop/simulations/run_all_sims.sh
   ```

3. Open the matching simulation markdown and walk through the commands.

4. Check production readiness:
   ```bash
   cat workshop/checklists/PRODUCTION_READINESS.md
   ```

---

## The five businesses

| # | Business | Type | Why it was chosen |
|---|---|---|---|
| 1 | Oblique Coffee Roasters | Coffee shop / roaster | Owner-operated, historic building risk, tight margins |
| 2 | Envision Creative | Marketing agency | Project/retainer cash flow, scope creep, reporting |
| 3 | Flintrock Operating L.L.C | Construction contractor | Small commercial GC, job costing, retainage |
| 4 | Greenlight Bookstore | Independent retail | Unionized staff, thin margins, event-driven sales |
| 5 | Plausible Analytics | Bootstrapped SaaS | Privacy/security, subscriptions, remote team |

---

## How the simulations work

The simulations use `sim_runner.py`, a standalone wrapper around the real Partenon hero tools. Each scenario writes its data to `workshop/simulations/workspaces/<business>/` so the main `partenon-core/data/` directory is not affected.

The runner supports these actions:

```
route, design, project, task, checklist, client, vendor, milestone,
followups, payment-link, invoice, keys, briefing, calendar, summary
```

Example:

```bash
python3 workshop/simulations/sim_runner.py route "organize my numbers"
python3 workshop/simulations/sim_runner.py project oblique "Buyout campaign" "John Chandler" 2026-07-31 120000 food
```

---

## Scope and known limitations

This workshop demonstrates the local, credential-free layer of Partenon. Anything that requires an external integration is documented as a production gap:

- Stripe payments need `STRIPE_SECRET_KEY`.
- Google Sheets/Drive need `GOOGLE_SERVICE_ACCOUNT_JSON`.
- Gmail/Contacts dispatch is not wired.
- Social publishing is not wired.
- G-Brain memory requires a separate `gbrain` service.

See `workshop/checklists/PRODUCTION_READINESS.md` and `MISSING_IMPLEMENTATION.md` for the full list.

---

## License and reuse

The company cards cite public sources. Simulations and guides are part of the Partenon repository and follow the same license as the project.
