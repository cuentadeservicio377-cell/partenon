# Partenon Workshop Agenda

Two formats: **90-minute** and **3-hour**.

---

## 90-Minute Agenda

**Audience:** Small-business owners, entrepreneurs, accelerator cohorts.
**Goal:** Install Partenon, understand the heroes, and walk through one complete simulation.

| Time | Segment | What happens |
|------|---------|--------------|
| 0:00-0:05 | Welcome and framing | Who is Hermes? What are the seven heroes? Why this matters for small business. |
| 0:05-0:15 | Live install | Clone repo, run `./install.sh`, verify `python3 scripts/demo_tesorero.py`. |
| 0:15-0:25 | Hero selection matrix | Use the industry table from `docs/ENTREPRENEUR_PLAYBOOK.md` to pick heroes for coffee shop, agency, construction, retail, SaaS. |
| 0:25-0:50 | Simulation walkthrough | Lead the coffee-shop simulation (`workshop/simulations/coffee-shop.md`): interview, config files, first 3 missions. |
| 0:50-0:75 | Hands-on onboarding | Participants create their own `config/company.yaml` and `.finance` or `.ops` file. |
| 0:75-0:85 | Smoke tests and dashboard | Run one hero smoke test and start the Next.js dashboard. |
| 0:85-0:90 | Next steps and Q&A | 30-day mission plan; review common gaps; share resources. |

---

## 3-Hour Agenda

**Audience:** University classes, deep-dive accelerator sessions, chambers of commerce.
**Goal:** Full onboarding experience with two simulations and a personal 30-day plan.

| Time | Segment | What happens |
|------|---------|--------------|
| 0:00-0:10 | Welcome and framing | Hermes = company; heroes = specialized agents; Google Workspace/Stripe as delivery surface. |
| 0:10-0:20 | Architecture overview | Four layers: interface, core, heroes, integrations. Show `web/developers.html` and `docs/architecture.md`. |
| 0:20-0:30 | Live install + demo | `./install.sh`, `python3 scripts/demo_tesorero.py`, `cd dashboard && npm run dev`. |
| 0:30-0:45 | Hero selection deep dive | Walk through the industry matrix and the five company cards in `workshop/companies/`. |
| 0:45-1:10 | Simulation 1: Coffee shop | Full walkthrough of `workshop/simulations/coffee-shop.md`. |
| 1:10-1:20 | Break | |
| 1:20-1:45 | Simulation 2: SaaS | Full walkthrough of `workshop/simulations/saas.md`; emphasize Guardian and Brain. |
| 1:45-2:20 | Hands-on onboarding | Participants run their own company interview, create all config files, and choose heroes. |
| 2:20-2:45 | Smoke tests and dashboard | Run smoke tests for 3 heroes; verify dashboard login and first project. |
| 2:45-2:55 | 30-day mission plan | Each participant writes 3 first missions for their business. |
| 2:55-3:00 | Closing and resources | Share repo, live site, docs, and workshop package files. |

---

## Facilitator Checklist

Before the workshop:
- [ ] Test `./install.sh` on the venue network.
- [ ] Have a fallback: pre-cloned USB drive or zip with `.venv` if network is slow.
- [ ] Prepare projector with `web/developers.html` and one simulation open.
- [ ] Print `workshop/HANDOUT.md` for each attendee.

During the workshop:
- [ ] Keep slides moving; most value is in live demos and hands-on time.
- [ ] Call out gaps honestly when a tool is local-only or requires credentials.
- [ ] Help participants choose one hero to activate first rather than all seven.

After the workshop:
- [ ] Collect questions and add them to the FAQ or `MISSING_IMPLEMENTATION.md`.
- [ ] Share the workshop package and repo link.
