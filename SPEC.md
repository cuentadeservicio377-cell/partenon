# SPEC — Partenon Website Rebuild

## Transcript Checklist

### Marketing page (`web/index.html`)

- [x] Talk about / brand introduction at the top.
- [x] Explain that there are two pages and that they serve as a marketing manual.
- [x] Philosophical narrative: Partenon = where the heroes are; heroes run errands for the gods; Hermes = god; Partenon = union of god + heroes.
- [x] Explained as marketing archetypes, without Greek kitsch.
- [x] Hermes = the company (not the CEO). It needs help. It has a powerful canvas.
- [x] Hermes publishes tasks; heroes pick them up from the Partenon.
- [x] Hero tools = Pegasus: open source + skills.
- [x] **Treasurer**:
  - [x] Google Sheets expert, dashboards, organizing information.
  - [x] Construction company example: materials, profit, cost, variable/fixed costs.
  - [x] Coffee shop example: marketing spend, taxes, rent, supplies, employees.
  - [x] Splits Hermes into subtasks/missions.
  - [x] Joint mission with entrepreneur and Hermes.
  - [x] `.finance` file.
- [x] **Messenger**:
  - [x] Sales + communication.
  - [x] Social media, memory, and brand.
  - [x] `.design` file.
  - [x] Open Design.
  - [x] Research questions: what company?, what do you sell?, who do you help?, why?, how do you solve it?, how does your project help?
  - [x] Secondary missions with the entrepreneur.
  - [x] Campaigns, organic calendar, SEO, GEO.
  - [x] WordPress / SSH / WordPress skills.
  - [x] Presentations, letters, emails.
  - [x] Connects to the Treasurer's Google Sheets.
- [x] **Collector**:
  - [x] Stripe, payment links, subscriptions.
  - [x] Online store, services, physical products.
- [x] **Guardian**:
  - [x] Security + Nvidia.
  - [x] Manages models, API keys, accounts (Twitter/X, OpenAI, Kimi Coding, etc.).
  - [x] `.security` file.
- [x] **Strategist**:
  - [x] Administration / operations manager / project management.
  - [x] Google Calendar, Gmail, reminders, client/operations details.
- [x] **Diplomat**:
  - [x] Relationships with clients and vendors.
  - [x] Gemini knight analogy (two sides, middle ground).
  - [x] Milestones, reminders, coordination with Strategist.
- [x] **G-Brain by Garitán**:
  - [x] Brain connected via MCP.
  - [x] All agents connected to Hermes.
- [x] **10 → 1M counter**:
  - [x] Progressive and coherent numbers.
  - [x] Multiple metrics per scale (income, quality, numbers in order, hours saved, jobs created).
- [x] **Reference paper/article** — placeholder: Hermes Business OS.
- [x] **Go-to-market**:
  - [x] Biweekly webinars with pre-registrations.
  - [x] Universities: accelerators, innovation departments, business/any-major students, extracurricular auditorium activities (with capacity data).
  - [x] Business organizations: BNI, Way/Pio, chambers of commerce, Rotary.
  - [x] Coworkings: specific workshops and partnerships.
  - [x] Accelerators: Hermes as a customized agent backed by Stripe, Nvidia, Nous Research.
- [x] **Repository / installation**:
  - [x] "Install Hermes" command (`curl -fsSL ... | bash`).
  - [x] Free Google Workspace as shared surface.
  - [x] Repository structure.
- [x] **Hero cards**:
  - [x] What it does, how it does it, connections, MSP, tools, skills, Drive.

### Technical page (`web/developers.html`)

- [x] Exact mirror of marketing but technical.
- [x] Complete architecture with flow diagrams (Mermaid).
- [x] Technical specifications per hero:
  - [x] Framework, skills, tools, MCP, personality, profile.
  - [x] How it connects, according to documentation, interconnections.
- [x] Point-to-point diagrams per hero (Treasurer/Sheets, Collector/Stripe, Guardian/models, Messenger/channels).
- [x] G-Brain/MCP technical with profile read/write diagram.
- [x] Stack and repository structure with `.finance`, `.design`, `.payments`, `.security`, `.ops`, `.relations` files.
- [x] Packaged 90-minute technical workshop:
  - [x] Pre-installation command.
  - [x] Initial review.
  - [x] Technical onboarding.
  - [x] Graphical process explanation with sequence diagram.

### Design

- [x] Approved redesign: Nous Research / open-source technical manual style with anti-slop.
- [x] OLED background `#050505` / `#08080C`, with subtle radial mesh, noise SVG, and optional scanlines.
- [x] Single cyan accent `#00D4FF` (saturation <80%); amber `#FFB800` on no more than 2 elements per page.
- [x] Display typography: Space Grotesk; body: Geist; mono/data: JetBrains Mono (also used in hero for technical effect); icons: Material Symbols Sharp.
- [x] Double-bevel cards (outer shell 18px + inner core 12px); `rounded-full` buttons.
- [x] Floating "fluid island" nav with backdrop blur and staggered mobile menu.
- [x] Asymmetric and bento layouts; aggressive collapse to one column below 768px.
- [x] Anti-AI-slop copy: no em-dashes, intensifiers, filler phrases, dramatic transitions, or AI clichés.
- [x] No emojis, no Inter/Roboto/Arial/Open Sans/Helvetica, no thick Lucide.

## Validation Notes

- Reviewed in Chrome/Chromium via Playwright at 1440px and 390px.
- Mermaid renders with `base` theme and custom `themeVariables` (backgrounds `#111118`, borders `#00D4FF`, text `#E8E8ED`).
- Milestone counters animate on viewport entry.
- Reveals use `IntersectionObserver` + CSS `transform`/`opacity`; no layout animations.
- Pre-flight anti-slop: no em-dashes, intensifiers, or dramatic headings.
