# Partenon Workshop Package

This directory contains ready-to-run materials for onboarding real small businesses onto Partenon. It is designed for founders, operators, and facilitators who want to see how the seven heroes apply to concrete business types.

## What's inside

```text
workshop/
├── companies/          # Public company cards by business type
├── simulations/        # Step-by-step onboarding simulations
├── guides/             # Facilitator and hero-selection guides
└── checklists/         # Onboarding checklists by business type
```

## Company cards

Each card profiles a real small business, its public pain points, and why Partenon fits.

| Business type | Example card |
|---------------|--------------|
| Coffee shop | [`companies/coffee-shop--portland-coffee-roasters.md`](companies/coffee-shop--portland-coffee-roasters.md) |
| Marketing agency | [`companies/marketing-agency--searchbloom.md`](companies/marketing-agency--searchbloom.md) |
| Construction company | [`companies/construction-company--marsh-bell-construction.md`](companies/construction-company--marsh-bell-construction.md) |
| Retail store | [`companies/retail-store--brazos-bookstore.md`](companies/retail-store--brazos-bookstore.md) |
| SaaS / bootstrapped startup | [`companies/saas-startup--chatbase.md`](companies/saas-startup--chatbase.md) |

Additional reference cards are included for comparison:

- Coffee shop: [`coffee-shop--joe-coffee-company.md`](companies/coffee-shop--joe-coffee-company.md)
- Agency: [`marketing-agency--single-grain.md`](companies/marketing-agency--single-grain.md)
- Construction: [`construction-company--greenberg-construction.md`](companies/construction-company--greenberg-construction.md)
- Retail: [`retail-store--k-and-l-wine-merchants.md`](companies/retail-store--k-and-l-wine-merchants.md)
- SaaS: [`saas-startup--wp-umbrella.md`](companies/saas-startup--wp-umbrella.md)

## Simulations

Each simulation walks through a full Partenon onboarding using the real repository:

1. [`simulations/coffee-shop.md`](simulations/coffee-shop.md) — Joe Coffee Company
2. [`simulations/agency.md`](simulations/agency.md) — Single Grain
3. [`simulations/construction-company.md`](simulations/construction-company.md) — Marsh Bell Construction
4. [`simulations/retail-store.md`](simulations/retail-store.md) — Brazos Bookstore
5. [`simulations/saas-startup.md`](simulations/saas-startup.md) — Chatbase

Each simulation includes:

- Business context and Hermes interview questions
- Recommended hero activation order
- Example `client.yaml`, `.finance`, `.ops`, `.relations`, `.design`, `.payments`, and `.security` files
- Copy-paste commands with expected outputs
- First three missions per hero
- Gaps found during the simulation

## Guides

- [`guides/facilitator-guide.md`](guides/facilitator-guide.md) — how to run a 90-minute Partenon onboarding workshop
- [`guides/hero-selection-guide.md`](guides/hero-selection-guide.md) — quick reference for which heroes to activate first by business type

## Checklists

- [`checklists/onboarding-checklist.md`](checklists/onboarding-checklist.md) — generic day-1 to day-90 checklist
- [`checklists/business-type-checklists.md`](checklists/business-type-checklists.md) — tailored checklists for coffee shop, agency, construction, retail, and SaaS

## How to use this package

1. **Solo founder**: Pick your business-type card and simulation, copy the config files, run the commands, and complete the first three missions per hero.
2. **Facilitator**: Use the facilitator guide, run the group through the hero-selection exercise, then assign one simulation per breakout group.
3. **Contributor**: Add a new company card and simulation for a business type that is missing. Follow the existing format and cite public sources.

## Production readiness

Before running a live onboarding with a real company, review [`../PRODUCTION_READINESS.md`](../PRODUCTION_READINESS.md) and [`../MISSING_IMPLEMENTATION.md`](../MISSING_IMPLEMENTATION.md).
