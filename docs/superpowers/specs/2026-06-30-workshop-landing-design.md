# Design — Workshop Landing (`web/workshop.html`)

> Scope: Fase 1 of the Workshop hub. A single static landing page that registers attendees for the biweekly installation workshop and prepares them before the session.

---

## Goal

Create `web/workshop.html` as the third main page of the site, alongside `index.html` and `heroes.html`, with `developers.html` remaining the technical brief.

The page must:
1. Tell the 1-million-installations story with concrete impact metrics.
2. Explain what the workshop is and who it is for.
3. Give two installation paths: Local machine and VPS.
4. Show the day-of agenda in four blocks.
5. Give per-hero preparation checklists + AI prompts for attendees who do not have the documents ready.
6. Close with Workshop 2.0 follow-up and custom-workshop offering for organizations.
7. Update navigation in `web/index.html`, `web/heroes.html`, and `web/developers.html`.

---

## Design system

Reuse the existing site design system:
- Palette: marble `#F7F5F0`, parchment `#EDE8DF`, midnight `#2A2A2E`, deep stone `#2A2A2E`, stripe indigo `#635BFF`, NVIDIA green `#76B900`, myth gold `#D4A853`, hero accent colors.
- Fonts: Cinzel (display), Inter (body), JetBrains Mono (code).
- No emojis. Material Symbols Sharp weight 300 for icons.
- No massive gradients. Only animate `transform` and `opacity`.
- Mobile-first; asymmetric bento collapses to `w-full px-4` under 768px.
- One `<h1>` per page. Every section gets one clear idea.

---

## Page sections

### 1. Navbar
Same floating island nav used in `heroes.html`/`developers.html`. Links:
- THE MYTH → `index.html`
- THE HEROES → `heroes.html`
- WORKSHOP → `workshop.html` (active state)
- FOR DEVELOPERS → `developers.html`
- CTA: INSTALL THE PARTENON → `developers.html#install`

Update the same nav in the other three pages.

### 2. Hero
- Eyebrow: `INSTALLATION WORKSHOP`
- Headline: `Install The Partenon in 90 Minutes`
- Subhead: live, hands-on session every 15 days. Leave with Partenon running and your first three heroes configured.
- CTA primary: `REGISTER FOR NEXT SESSION` (mailto or Calendly placeholder).
- CTA secondary: `SEE WHAT TO PREPARE` → scrolls to `#prepare`.
- Storytelling strip below hero: 1M installations goal + impact counters (jobs created, revenue organized, Stripe payments processed, security audits run). Use the same counter animation pattern as `index.html`.

### 3. What You Get
Asymmetric bento grid on desktop (2+1 layout), stacked on mobile:
- A working local install.
- Three heroes configured for your business.
- A clear map of what is live, what needs credentials, and what is roadmap.

Copy is direct and factual. No em-dashes, no filler verbs like "elevate" or "empower".

### 4. Installation Paths (`#install`)
Two tabs:
- **Local** — prereqs (Python 3.10+, Node 20+, Git), commands `git clone` + `./install.sh`, expected output.
- **VPS** — prereqs (Ubuntu 22.04+, Docker, Docker Compose), commands `docker compose up --build -d`, notes on SSH and firewall.

Both show honest status: no credentials required for the base install; optional Hermes CLI distributed separately.

### 5. Workshop Agenda (`#agenda`)
Four numbered blocks with times:
1. Install & verify (20 min)
2. Configure your first three heroes (35 min)
3. Connect Hermes and build your first automation (20 min)
4. Brain setup: weekly reviews, objectives, and CRONs (15 min)

### 6. Prepare Before the Workshop (`#prepare`)
Accordions, one per hero, plus a general "AI helper" intro:
- Scribe: bank statements, expense receipts, Excel/Sheets of income and costs, supplier list.
- Herald: brand description, logo files, social handles, existing posts or ads.
- Collector: Stripe account (test mode is enough), product/service list, prices.
- Guardian: list of services/API keys used, who has access to what.
- Strategist: current project list, calendar tool, top 3 priorities.
- Diplomat: client/vendor list, recent emails or messages to follow up.
- Brain: previous decisions, notes, company objectives.

Each accordion includes a prompt block attendees can paste into Kimi Code / ChatGPT / Claude to extract the information if they do not have it documented.

### 7. Brain & Automations (`#brain`)
Explain what the Brain configures during the workshop:
- Weekly review CRON.
- Objective tracking.
- Morning briefing.
- Honest note: full autonomy requires connected integrations over time.

### 8. Custom Workshops (`#custom`)
Cards for:
- Coworking spaces
- Universities
- Professional associations
- Networking organizations
- Enterprise teams

CTA: `REQUEST A CUSTOM WORKSHOP` (mailto).

### 9. Workshop 2.0 Follow-Up (`#followup`)
Short section: one month after the first session, attendees receive a link to a follow-up workshop to review what is not working, fix integrations, and add more heroes.

### 10. Footer
Same footer pattern as the other pages, with links to the four main pages.

---

## Technical notes

- Static HTML + Tailwind CSS CDN + vanilla JS.
- No backend required; registration CTAs use `mailto:` or external link placeholders.
- Reuse existing CSS variables and components from `heroes.html`/`developers.html`.
- Reuse existing `copyInstall()` / copy-to-clipboard JS if code blocks are present.
- Reuse accordion pattern from `developers.html` (or simple `<details>` if JS-free is preferred).

---

## Out of scope for Fase 1

- `web/workshop-guides.html` detailed API-key guides (Fase 2).
- `web/workshop-followup.html` full follow-up landing (Fase 3).
- Real registration form backend.

---

## Files to create/modify

Create:
- `web/workshop.html`

Modify:
- `web/index.html` — add WORKSHOP link to nav.
- `web/heroes.html` — add WORKSHOP link to nav.
- `web/developers.html` — add WORKSHOP link to nav.
