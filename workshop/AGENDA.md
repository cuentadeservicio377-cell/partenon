# Partenon Hermes Onboarding Workshop — Agenda

**Duration:** 90 minutes  
**Audience:** Founders, operators, or technical implementers who want to onboard a small business onto Partenon.

---

## 0. Setup (before the session)

- [ ] Clone the Partenon repo.
- [ ] Run `./install.sh` and `python3 scripts/demo_tesorero.py`.
- [ ] Confirm `python3 workshop/simulations/sim_runner.py route "organize my numbers"` returns `partenon-tesorero`.

---

## 1. Introduction (10 min)

- What Partenon is: seven heroes, one shared context, no single tool does everything.
- The Hermes relationship: Hermes is the company, not the CEO.
- Workshop goal: onboard one real business in 90 minutes and know what is production-ready vs. what still needs wiring.

---

## 2. The five case studies (15 min)

Present the company cards and ask the room to pick one:

1. Joe Coffee Company — New York coffee shop / roaster
2. Single Grain — digital marketing agency
3. SpawGlass — Texas commercial construction contractor
4. Tracksmith — athletic apparel retail / e-commerce
5. Buffer — bootstrapped social-media SaaS

For each, discuss:

- What is the most urgent problem in the next 30 days?
- Which hero should be activated first?
- Which integrations are real today and which are stubs?

---

## 3. Router and hero selection (10 min)

Live demo:

```bash
python3 workshop/simulations/sim_runner.py route "organize my numbers"
python3 workshop/simulations/sim_runner.py route "create a campaign"
python3 workshop/simulations/sim_runner.py route "invoice a client"
```

Discuss how Partenon maps natural language to a hero and where the router is still rule-based.

---

## 4. Guided simulation (35 min)

Walk through the selected simulation file (`coffee-shop.md`, `agency.md`, `construction.md`, `retail.md`, or `saas.md`):

1. Brand interview with the Herald (`.design`).
2. First project and tasks with the Strategist.
3. Client/vendor milestone with the Diplomat.
4. Payment link or invoice with the Collector.
5. Content calendar with the Herald.
6. Morning briefing with the Strategist.
7. Key audit with the Guardian.

Pause after each hero to explain what is real and what is a documented gap.

---

## 5. Production-readiness review (15 min)

Open `workshop/checklists/PRODUCTION_READINESS.md` and classify each item:

- **Green:** works out of the box today.
- **Yellow:** works locally, needs credentials for live use.
- **Red:** not implemented; requires engineering or a third-party integration.

Update `MISSING_IMPLEMENTATION.md` with any new gaps discovered during the session.

---

## 6. Next steps and closing (5 min)

- Assign owner and deadline for the first three yellow/red items.
- Point participants to:
  - `docs/ENTREPRENEUR_PLAYBOOK.md`
  - `docs/HERO_GUIDE.md`
  - `workshop/guides/HERMES_ONBOARDING.md`
- Run `python3 scripts/demo_tesorero.py` and `cd dashboard && npm run build` to verify the base system.

---

## Materials

- Slides: `workshop/SLIDES.md`
- Participant handout: `workshop/HANDOUT.md`
- Case studies: `workshop/companies/`
- Simulations: `workshop/simulations/`
