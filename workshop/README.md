# Partenon Workshop Package

A reusable workshop kit for teaching entrepreneurs, developers, and ecosystem partners how to install, configure, and run Partenon for real small businesses.

---

## What is included

| File | Purpose |
|------|---------|
| [`README.md`](README.md) | This overview |
| [`AGENDA.md`](AGENDA.md) | 90-minute and 3-hour versions |
| [`SLIDES.md`](SLIDES.md) | Speaker notes and slide content |
| [`HANDOUT.md`](HANDOUT.md) | One-page attendee handout |
| [`../docs/HERMES_ONBOARDING.md`](../docs/HERMES_ONBOARDING.md) | Detailed guide for how Hermes should guide a new company through setup |
| [`guides/facilitator-guide.md`](guides/facilitator-guide.md) | Facilitator notes for running the workshop |
| [`guides/hero-selection-guide.md`](guides/hero-selection-guide.md) | Deeper guidance on choosing first heroes |
| [`companies/`](companies/) | Five real-world company cards |
| [`simulations/`](simulations/) | Simulated onboardings for each company |
| [`checklists/production-readiness.md`](checklists/production-readiness.md) | PASS/FAIL/PARTIAL production-readiness checklist |
| [`checklists/business-type-checklists.md`](checklists/business-type-checklists.md) | Per-business-type 30-day onboarding checklists |
| [`checklists/onboarding-checklist.md`](checklists/onboarding-checklist.md) | Generic onboarding checklist |

---

## Target audience

- **Entrepreneurs and small-business owners** who want to organize operations, finance, sales, communication, collections, security, and administration.
- **Developers and operators** who want to install Partenon, extend hero profiles, and run onboarding for clients.
- **Universities, accelerators, chambers of commerce, coworking spaces, and business organizations** that run hands-on workshops and events.

---

## Learning objectives

By the end of the workshop, attendees can:

1. Explain what Partenon is, who Hermes is, and what the seven heroes do.
2. Install Partenon locally and run the Scribe demo.
3. Choose the right heroes for a given business type.
4. Customize `.finance`, `.ops`, `.design`, `.payments`, `.relations`, `.security`, and `.brain` files.
5. Run hero tools directly and interpret their outputs.
6. Identify which integrations require real credentials and which work in local mode.
7. Document gaps honestly and decide whether to build, buy, or wait.

---

## How to use this package

1. **Before the event:**
   - Read [`../docs/HERMES_ONBOARDING.md`](../docs/HERMES_ONBOARDING.md).
   - Pick one or two company cards from [`companies/`](companies/) that match your audience.
   - Run `./install.sh` and `python3 scripts/demo_scribe.py` on the demo machine.

2. **During the event:**
   - Follow [`AGENDA.md`](AGENDA.md).
   - Present from [`SLIDES.md`](SLIDES.md).
   - Distribute [`HANDOUT.md`](HANDOUT.md).
   - Walk through the matching simulation in [`simulations/`](simulations/).

3. **After the event:**
   - Share the repo link: https://github.com/cuentadeservicio377-cell/partenon
   - Share the live site: https://hermespartenon.online/
   - Ask attendees to complete the first mission in their own dashboard.

---

## Company cards and matching simulations

| Business type | Company card | Simulation |
|---------------|--------------|------------|
| Coffee shop | [`coffee-shop--flora-coffee.md`](companies/coffee-shop--flora-coffee.md) | [`flora-coffee-onboarding.md`](simulations/flora-coffee-onboarding.md) |
| Marketing agency | [`marketing-agency--mack-media-group.md`](companies/marketing-agency--mack-media-group.md) | [`mack-media-group-onboarding.md`](simulations/mack-media-group-onboarding.md) |
| Construction company | [`construction-company--boreal-contractors.md`](companies/construction-company--boreal-contractors.md) | [`boreal-contractors-onboarding.md`](simulations/boreal-contractors-onboarding.md) |
| Retail store | [`retail-store--kick-pleat.md`](companies/retail-store--kick-pleat.md) | [`kick-pleat-onboarding.md`](simulations/kick-pleat-onboarding.md) |
| SaaS/bootstrapped startup | [`saas-startup--outseta.md`](companies/saas-startup--outseta.md) | [`outseta-onboarding.md`](simulations/outseta-onboarding.md) |

---

## Related documentation

- [`docs/QUICKSTART.md`](../docs/QUICKSTART.md) — 15-minute local demo
- [`docs/ENTREPRENEUR_PLAYBOOK.md`](../docs/ENTREPRENEUR_PLAYBOOK.md) — hero selection by business type
- [`docs/HERO_GUIDE.md`](../docs/HERO_GUIDE.md) — every tool, env var, and cron job per hero
- [`docs/API.md`](../docs/API.md) — commands and return values
- [`docs/FAQ.md`](../docs/FAQ.md) — honest answers to common questions
- [`MISSING_IMPLEMENTATION.md`](../MISSING_IMPLEMENTATION.md) — current gaps and suggested priorities

---

## License and attribution

Partenon is an open-source project. The company cards use only public information. See individual cards for sources.
