# Workshop Landing — Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `web/workshop.html` as the third public page of the Partenon site and update navigation in the three existing pages.

**Architecture:** Single static HTML page using the existing Tailwind CDN + custom CSS pattern from `heroes.html`/`developers.html`. Sections are self-contained, copy-first, and reuse the same navbar/footer/animation utilities. No backend. Registration CTAs use `mailto:` placeholders.

**Tech Stack:** Static HTML, Tailwind CSS CDN, vanilla JS, Material Symbols Sharp.

## Global Constraints

- Palette: marble `#F7F5F0`, parchment `#EDE8DF`, midnight `#2A2A2E`, deep stone `#2A2A2E`, stripe indigo `#635BFF`, NVIDIA green `#76B900`, myth gold `#D4A853`, hero accent colors.
- Fonts: Cinzel (display), Inter (body), JetBrains Mono (code).
- No emojis. Use Material Symbols Sharp weight 300 for icons.
- No massive gradients or generic glows.
- Only animate `transform` and `opacity`.
- Mobile-first: asymmetric bento collapses to `w-full px-4` under 768px.
- One `<h1>` per page. One clear idea per section.
- Anti-AI-slop copy: no em-dashes, no "elevate"/"empower"/"revolutionize", no filler phrases. Direct, factual, verifiable.
- All capability claims map to `docs/CAPABILITIES.md` and code reality.

---

## File Structure

- **Create:** `web/workshop.html` — full landing page.
- **Modify:** `web/index.html` — add WORKSHOP link to navbar.
- **Modify:** `web/heroes.html` — add WORKSHOP link to navbar.
- **Modify:** `web/developers.html` — add WORKSHOP link to navbar.

---

### Task 1: Scaffold `web/workshop.html` shell

**Files:**
- Create: `web/workshop.html`

**Interfaces:**
- Consumes: existing design tokens and font imports from `heroes.html`.
- Produces: valid HTML shell with working navbar, empty `<main>`, and footer.

- [ ] **Step 1: Copy the `<head>` and CSS variable block from `web/heroes.html`**

Reuse the same Tailwind config, custom properties, font imports, and base styles. Change the `<title>` to `Workshop — The Partenon`.

- [ ] **Step 2: Add the floating island navbar**

Use the same navbar markup as `heroes.html`, with these links:
- THE MYTH → `index.html`
- THE HEROES → `heroes.html`
- WORKSHOP → `workshop.html` (active, `text-stripe-indigo`)
- FOR DEVELOPERS → `developers.html`
- CTA: INSTALL THE PARTENON → `developers.html#install`

Add the same mobile menu toggle.

- [ ] **Step 3: Add the footer**

Use the same footer as `heroes.html` but add a WORKSHOP link.

- [ ] **Step 4: Verify the empty page renders**

Open `http://localhost:8080/workshop.html` and confirm navbar/footer appear with no console errors.

- [ ] **Step 5: Commit**

```bash
git add web/workshop.html
git commit -m "feat(web): scaffold workshop.html shell with nav and footer"
```

---

### Task 2: Hero + storytelling impact strip

**Files:**
- Modify: `web/workshop.html`

**Interfaces:**
- Consumes: existing `.animate-on-scroll` utility and counter logic from `index.html`.
- Produces: hero section and 4-item impact strip.

- [ ] **Step 1: Build the hero section**

Content:
- Eyebrow: `INSTALLATION WORKSHOP`
- Headline: `Install The Partenon in 90 Minutes`
- Subhead: `A live, hands-on session every 15 days. You will leave with Partenon running on your machine and your first three heroes configured for your business.`
- Primary CTA: `REGISTER FOR NEXT SESSION` → `mailto:workshop@partenon.dev?subject=Register%20for%20Partenon%20Workshop`
- Secondary CTA: `SEE WHAT TO PREPARE` → `#prepare`

- [ ] **Step 2: Build the impact strip**

Four counters in an asymmetric grid (2+2 on desktop, stacked on mobile):
- `1M` installations goal
- `$1B+` revenue organized by Scribe profiles
- `10M+` Stripe payments processed by Collector profiles
- `1M+` security audits run by Guardian profiles

Use the same counter animation as `index.html` (data-target attributes + IntersectionObserver). Use `font-variant-numeric: tabular-nums`.

- [ ] **Step 3: Verify copy is anti-slop**

Read aloud. Remove any em-dashes, intensifiers, or claims that cannot be verified. Replace with direct statements.

- [ ] **Step 4: Commit**

```bash
git add web/workshop.html
git commit -m "feat(web): workshop hero and impact counters"
```

---

### Task 3: What you get — asymmetric bento

**Files:**
- Modify: `web/workshop.html`

**Interfaces:**
- Consumes: existing card styles and color tokens.
- Produces: three-value bento section.

- [ ] **Step 1: Create a 2+1 asymmetric grid**

Desktop: two wider cards on top, one full-width card below. Mobile: stacked.

Cards:
1. `A working local install` — Partenon runs from `./install.sh`. No live credentials needed.
2. `Three heroes configured for your business` — choose Scribe, Strategist, and one more based on your operation.
3. `A clear live / connect / roadmap map` — know what works today, what needs your API keys, and what is still being built.

- [ ] **Step 2: Verify no 3-equal-column layout**

The grid must not be three identical columns.

- [ ] **Step 3: Commit**

```bash
git add web/workshop.html
git commit -m "feat(web): workshop value bento"
```

---

### Task 4: Installation paths — Local and VPS tabs

**Files:**
- Modify: `web/workshop.html`

**Interfaces:**
- Consumes: existing `.install-tab` / `.install-panel` CSS pattern from `developers.html`.
- Produces: two-tab install section with copy-to-clipboard code blocks.

- [ ] **Step 1: Copy tab CSS/JS pattern from `developers.html`**

Use the same `.install-tab`, `.install-panel`, and copy-btn behavior.

- [ ] **Step 2: Write Local tab content**

Prereqs: Python 3.10+, Node.js 20+, npm, Git.
Commands:
```bash
git clone https://github.com/cuentadeservicio377-cell/partenon.git
cd partenon
./install.sh
```
Note: `install.sh` creates `.venv`, copies `.env.example`, runs `scripts/demo_scribe.py`. Hermes CLI is optional.

- [ ] **Step 3: Write VPS tab content**

Prereqs: Ubuntu 22.04+, Docker, Docker Compose, SSH access.
Commands:
```bash
git clone https://github.com/cuentadeservicio377-cell/partenon.git
cd partenon
docker compose up --build -d
```
Note: exposes dashboard on port 3000 and API on port 8000; configure firewall and reverse proxy for production.

- [ ] **Step 4: Test copy buttons and tab switching**

Click both tabs and each copy button. Verify panel visibility updates.

- [ ] **Step 5: Commit**

```bash
git add web/workshop.html
git commit -m "feat(web): workshop local and VPS install tabs"
```

---

### Task 5: Workshop agenda

**Files:**
- Modify: `web/workshop.html`

**Interfaces:**
- Consumes: existing timeline/step styles from `heroes.html` workflow.
- Produces: four numbered agenda blocks.

- [ ] **Step 1: Build four agenda blocks**

Use a vertical timeline with numbers and hero/section icons.

1. **Install and verify** (20 min) — clone, run `./install.sh`, confirm Scribe demo output.
2. **Configure your first three heroes** (35 min) — load documents into Scribe, Strategist, and one domain hero.
3. **Connect Hermes and build your first automation** (20 min) — set optional credentials and run a routing command.
4. **Brain setup: weekly reviews and CRONs** (15 min) — configure weekly review, objectives, and morning briefing.

- [ ] **Step 2: Verify times sum to 90 minutes**

20 + 35 + 20 + 15 = 90.

- [ ] **Step 3: Commit**

```bash
git add web/workshop.html
git commit -m "feat(web): workshop agenda section"
```

---

### Task 6: Prepare before the workshop — per-hero accordions

**Files:**
- Modify: `web/workshop.html`

**Interfaces:**
- Consumes: existing accordion behavior from `developers.html`.
- Produces: seven accordions, each with a checklist and an AI prompt.

- [ ] **Step 1: Build accordions for each hero**

Each accordion contains:
- What to bring (bullet list).
- Suggested prompt to extract the information with Kimi Code, ChatGPT, Claude, etc.

Hero checklists:
- **Scribe:** bank statements, expense receipts, income/expense spreadsheets, supplier list.
- **Herald:** brand description, logo files, social handles, existing posts or ads.
- **Collector:** Stripe account in test mode, product/service list, prices.
- **Guardian:** services/API keys used, who has access to what.
- **Strategist:** current project list, calendar tool, top 3 priorities.
- **Diplomat:** client/vendor list, recent emails/messages to follow up.
- **Brain:** previous decisions, notes, company objectives.

- [ ] **Step 2: Write AI prompts**

Each prompt should be copy-pasteable and ask the AI to interview the user and output a structured list. Example for Scribe:

```
Ask me questions one at a time until you understand my business finances. Then output a structured list with: income sources, fixed expenses, variable expenses, suppliers, and any financial documents I should gather.
```

- [ ] **Step 3: Verify all prompts are practical**

Each prompt must produce useful preparation material for the workshop.

- [ ] **Step 4: Commit**

```bash
git add web/workshop.html
git commit -m "feat(web): workshop per-hero preparation accordions"
```

---

### Task 7: Brain and automations

**Files:**
- Modify: `web/workshop.html`

**Interfaces:**
- Consumes: existing card and icon styles.
- Produces: Brain section with automation examples.

- [ ] **Step 1: Build the Brain section**

Content:
- What the Brain configures: weekly review CRON, objective tracking, morning briefing.
- Honest note: full autonomy grows as more integrations are connected after the workshop.

- [ ] **Step 2: Add automation examples**

Three small cards:
- Weekly review every Sunday at 20:00.
- Morning briefing with today's priorities.
- Objective nudges when deadlines approach.

- [ ] **Step 3: Commit**

```bash
git add web/workshop.html
git commit -m "feat(web): workshop brain and automations section"
```

---

### Task 8: Custom workshops and Workshop 2.0

**Files:**
- Modify: `web/workshop.html`

**Interfaces:**
- Consumes: existing card and CTA styles.
- Produces: two closing sections.

- [ ] **Step 1: Build custom workshops section**

Audience cards:
- Coworking spaces
- Universities
- Professional associations
- Networking organizations
- Enterprise teams

CTA: `REQUEST A CUSTOM WORKSHOP` → `mailto:workshop@partenon.dev?subject=Custom%20Workshop%20Request`

- [ ] **Step 2: Build Workshop 2.0 section**

Content: one month after the first session, attendees receive a link to a follow-up workshop to fix integrations, add heroes, and review progress.

CTA: `JOIN THE WAITLIST` → same mailto with subject `Workshop 2.0 Waitlist`.

- [ ] **Step 3: Commit**

```bash
git add web/workshop.html
git commit -m "feat(web): workshop custom and follow-up sections"
```

---

### Task 9: Update navigation in existing pages

**Files:**
- Modify: `web/index.html`
- Modify: `web/heroes.html`
- Modify: `web/developers.html`

**Interfaces:**
- Consumes: existing navbar markup.
- Produces: consistent four-link navigation everywhere.

- [ ] **Step 1: Add WORKSHOP link to desktop and mobile navs**

Insert between THE HEROES and FOR DEVELOPERS in all three pages.

Desktop link example from `heroes.html`:
```html
<a href="workshop.html" class="nav-link ...">WORKSHOP</a>
```

Mobile menu: same insertion order.

- [ ] **Step 2: Mark the correct link as active on each page**

On `workshop.html`, WORKSHOP gets the active color. On the others, keep their existing active states.

- [ ] **Step 3: Verify all four pages link to each other correctly**

Click every nav link on every page.

- [ ] **Step 4: Commit**

```bash
git add web/index.html web/heroes.html web/developers.html
git commit -m "feat(web): add workshop link to all navbars"
```

---

### Task 10: Verification and closure

**Files:**
- Modify: none (read-only verification)

- [ ] **Step 1: HTML parse check**

Run:
```bash
python3 -c "from html.parser import HTMLParser; [HTMLParser().feed(open(f).read()) for f in ['web/index.html','web/heroes.html','web/developers.html','web/workshop.html']]"
```
Expected: no errors.

- [ ] **Step 2: Full test/build verification**

```bash
pytest tests/ -q
bash -n install.sh
cd dashboard && npm run build
```
Expected: 184 passed, install.sh syntax ok, build success.

- [ ] **Step 3: Visual review in Chrome**

Open `http://localhost:8080/workshop.html` at 1440px and 390px. Scroll through all sections.

- [ ] **Step 4: Update TODOS.md**

Mark Task 2 as done. Add Phase 8 placeholders if needed.

- [ ] **Step 5: Final commit**

```bash
git add -A
git commit -m "feat(web): complete workshop landing phase 1"
```

---

## Spec Coverage Check

| Spec Section | Task |
|---|---|
| Navbar | Task 1, Task 9 |
| Hero + storytelling | Task 2 |
| What you get | Task 3 |
| Installation paths | Task 4 |
| Agenda | Task 5 |
| Prepare before workshop | Task 6 |
| Brain & automations | Task 7 |
| Custom workshops + follow-up | Task 8 |
| Verification | Task 10 |

No gaps. No placeholders.
