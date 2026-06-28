# Partenon Onboarding Checklist

Use this checklist for any business onboarding onto Partenon. Mark each item as you complete it.

## Days 1–7: Foundation

- [ ] Clone the repo and run `./install.sh`.
- [ ] Copy `.env.example` to `.env` and set real or test credentials.
- [ ] Run `python3 scripts/demo_scribe.py` and verify the report.
- [ ] Create `config/company.yaml` with company name, industry, currency, timezone, and active profiles.
- [ ] Choose the hero activation order for your business type (see [`../guides/hero-selection-guide.md`](../guides/hero-selection-guide.md)).
- [ ] Copy the profile templates you need:
  - `.finance` from `hermes/profiles/partenon-scribe/templates/.finance.example`
  - `.design` from `hermes/profiles/partenon-herald/templates/.design.example`
  - `.payments` from `hermes/profiles/partenon-collector/templates/.payments.example`
  - `.security` from `hermes/profiles/partenon-guardian/templates/.security.example`
  - `.ops` from `hermes/profiles/partenon-strategist/templates/.ops.example`
  - `.relations` from `hermes/profiles/partenon-diplomat/templates/.relations.example`
  - `.brain` from `hermes/profiles/partenon-brain/templates/.brain.example`
- [ ] Fill `.finance` with fixed costs, variable budgets, and vendors.
- [ ] Start the dashboard (`cd dashboard && npm install && npm run dev`) and confirm it loads.

## Days 8–30: First missions

- [ ] Run the first mission for your top-priority hero and verify the output.
- [ ] Create your first project in the Strategist and assign at least one task with owner and due date.
- [ ] Register your top 5 clients/vendors in `.relations`.
- [ ] Create your first payment link or subscription in `.payments` (local mode first).
- [ ] Schedule the Strategist's morning briefing and the Diplomat's daily follow-ups.
- [ ] Guardian: list keys, audit all active profiles, and write the first `.security` policy.
- [ ] Brain: index at least one validated decision.

## Days 31–60: Operations

- [ ] Connect live Google Workspace credentials and verify Drive/Sheet creation.
- [ ] Connect Stripe test credentials and verify a test payment link.
- [ ] Automate weekly reports from the Scribe and Collector.
- [ ] Build reusable checklists for your industry.
- [ ] Review the Guardian's weekly audit and rotate any key older than 90 days.

## Days 61–90: Scale

- [ ] Connect live Stripe and G-Brain production credentials.
- [ ] Document your company's standard operating procedures in `docs/WELCOME.md`.
- [ ] Train any additional users on the dashboard and Hermes prompts.
- [ ] Review `PRODUCTION_READINESS.md` and `MISSING_IMPLEMENTATION.md` for blockers.
