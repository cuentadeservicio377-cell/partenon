# Partenon Hackathon Explainer — Plan

## Overview
- **Topic**: The Partenon — a working headquarters for Hermes profiles inside a small business.
- **Hook**: Most AI answers. Hermes acts. But an agent without a home wanders off.
- **Aha moment**: Seven specialized profiles share one brain and one memory, so handoffs are natural and nothing is lost.
- **Target audience**: Hackathon judges, open-source contributors, and small-business founders.
- **Length**: 2 minutes 20 seconds to 3 minutes (target ~2:45).
- **Resolution**: 1080p final; iterate at 480p.
- **Language**: English.
- **Voiceover word count**: ~420 words at ~150 wpm.

## Color Palette
| Role | Hex | Usage |
|------|-----|-------|
| Background | `#050505` | Full-scene base |
| Surface | `#08080C` | Secondary panels |
| Text | `#F7F5F0` | Primary copy (marble) |
| Muted | `#6B6B78` | Secondary / structural lines |
| Cyan accent | `#00D4FF` | Hermes, core, live wiring, CTAs |
| Amber | `#FFB800` | Live tags, key emphasis, counter |
| Parchment | `#EDE8DF` | Subtle surfaces, status labels |
| Hero colors | see Scene 3 | One per profile |

## Typography
- **Font**: `"Menlo"` for all text (monospace, Manim-safe).
- **Title size**: 48
- **Heading size**: 36
- **Body size**: 26–30
- **Label size**: 20–24
- **Caption size**: 18–20

## Arc: Problem → Solution → System → Honest Status → How to Use → Call to Action

---

## Scene 1: The Oracle Problem (~18s)
**Purpose**: Establish the gap between answering AI and acting AI.
**Layout**: LEFT_RIGHT split. Left: a static chat bubble. Right: a founder drowning in spreadsheets, invoices, and notifications.

### Visual elements
- Dark background `#050505`.
- Left panel: a rounded rectangle chat bubble with `"Q: What should I do?"` and `"A: You should organize your receipts."` in muted text.
- Right panel: a small founder figure surrounded by floating document rectangles labeled `RECEIPTS`, `INVOICES`, `FOLLOWUPS`, `CALENDAR`.
- A thin cyan arrow tries to leave the chat bubble but fades before reaching the work.

### Animation sequence
1. Fade in title `"Most AI tools are oracles."` at top. (1.5s)
2. Write the chat question and answer. (2.0s)
3. Draw the founder and the orbiting documents. (2.5s)
4. Show the cyan arrow leaving the bubble, then dim it. (2.0s)
5. Hold on the contrast: answer on the left, unresolved work on the right. (2.0s)
6. Fade out. (0.5s)

### Subtitle / voiceover
"Most AI tools today are oracles. You ask. They answer. Then you go back to your spreadsheet, your inbox, and do the work yourself."

---

## Scene 2: Hermes Needs a Home (~20s)
**Purpose**: Introduce Hermes as an agent and Partenon as its working headquarters.
**Layout**: FULL_CENTER. A single glowing core appears, then expands into a structure.

### Visual elements
- Center: a cyan ring labeled `"HERMES"`.
- It pulses. Text below: `"agent, not assistant"`.
- A faint Parthenon-style column outline rises behind the ring.
- Title card: `"THE PARTENON"`.

### Animation sequence
1. Draw the Hermes ring with a pulse. (1.5s)
2. Write `"agent, not assistant"`. (1.0s)
3. Fade in the column outline as a structural frame. (1.5s)
4. Transform the ring into the Partenon wordmark. (1.5s)
5. Add subtitle: `"a working headquarters for Hermes, inside a small business."` (1.5s)
6. Fade out. (0.5s)

### Subtitle / voiceover
"Hermes is different. Hermes is an agent: it can act. But an agent without structure is just a clever assistant that wanders off. So I built a home for it. I called it The Partenon."

---

## Scene 3: The Seven Heroes (~45s)
**Purpose**: Show the seven profiles around Hermes, each with a territory.
**Layout**: ANNOTATED_DIAGRAM. Hermes at center; heroes orbit in a ring.

### Visual elements
- Center circle: `"HERMES"` in cyan.
- Seven smaller circles arranged around it:
  - Scribe — `#4A90A4` — finance
  - Herald — `#9B59B6` — communications
  - Collector — `#635BFF` — payments
  - Guardian — `#76B900` — security
  - Strategist — `#FFB800` — operations
  - Diplomat — `#E74C3C` — relations
  - Brain — `#D4A853` — memory
- Thin lines connect Hermes to each hero.

### Animation sequence
1. Place Hermes at center. (1.0s)
2. Draw the ring path. (1.5s)
3. Animate each hero appearing one by one, clockwise, with its label. (0.8s each × 7 ≈ 5.6s)
4. Draw connecting lines back to Hermes. (2.0s)
5. Highlight the Brain and draw extra lines from Brain to every other hero. (2.5s)
6. Hold. (2.0s)
7. Fade out. (0.5s)

### Subtitle / voiceover
"The Partenon is a system of seven Hermes profiles that share one business context. The Scribe handles finance. The Herald handles communications. The Collector handles payments. The Guardian handles security. The Strategist handles operations. The Diplomat handles relationships. And the Brain holds the memory they all share."

---

## Scene 4: Honest Status Tags (~25s)
**Purpose**: Explain LIVE / CONNECT / ROADMAP without overselling.
**Layout**: PROGRESSIVE list. Three status cards appear vertically.

### Visual elements
- Three rounded rectangles stacked:
  - Top: amber tag `"LIVE"` + text `"runs the moment you install"`
  - Middle: cyan tag `"CONNECT"` + text `"works after you add credentials"`
  - Bottom: parchment tag `"ROADMAP"` + text `"not built yet; labeled clearly"`
- A small note at bottom: `"No credentials required to explore."`

### Animation sequence
1. Write the scene title `"Honest status tags"`. (1.0s)
2. Slide in the LIVE card. (1.5s)
3. Slide in the CONNECT card. (1.5s)
4. Slide in the ROADMAP card. (1.5s)
5. Fade in the bottom note. (1.0s)
6. Hold. (2.0s)
7. Fade out. (0.5s)

### Subtitle / voiceover
"Every capability is tagged. LIVE runs the moment you install. CONNECT works after you add your own Stripe or Google credentials. ROADMAP is not built yet, and we say so on every card. No credentials are required to explore."

---

## Scene 5: Architecture Flow (~22s)
**Purpose**: Show how a request moves from founder to tools through Hermes, core, and heroes.
**Layout**: LEFT_RIGHT horizontal flow diagram.

### Visual elements
- Nodes left to right:
  - `FOUNDER` (marble)
  - `HERMES` (cyan)
  - `CORE` (cyan)
  - `HEROES` (multi-color cluster)
  - `TOOLS` (muted)
- Arrows between nodes.
- Below: `Google Workspace`, `Stripe`, `G-Brain` as tool icons.

### Animation sequence
1. Draw the Founder node. (1.0s)
2. Draw arrow and Hermes node. (1.0s)
3. Draw arrow and Core node. (1.0s)
4. Draw arrow and Heroes cluster. (1.5s)
5. Draw arrow and Tools node, then reveal the three integrations. (2.0s)
6. A small packet dot animates along the full path. (2.0s)
7. Hold. (1.5s)
8. Fade out. (0.5s)

### Subtitle / voiceover
"A founder asks. Hermes routes the intent through partenon-core. The core dispatches the right hero. The hero calls the tool it needs: Google Workspace, Stripe, or G-Brain memory."

---

## Scene 6: Install and Run (~25s)
**Purpose**: Show how simple it is to get started and mention the workshop.
**Layout**: TOP_BOTTOM. Top: install commands. Bottom: workshop card.

### Visual elements
- Top: a code block with:
  ```
  git clone .../partenon.git
  cd partenon
  ./install.sh
  ```
- Bottom: a rounded card with `"90-MINUTE WORKSHOP"` and three bullets:
  - install locally or on a VPS
  - meet Scribe, Strategist, Guardian
  - leave with a live dashboard

### Animation sequence
1. Type the three install commands line by line. (3.0s)
2. Draw a checkmark and `"184 tests pass"`. (1.0s)
3. Slide up the workshop card. (1.5s)
4. Reveal the three bullets one by one. (2.0s)
5. Hold. (2.0s)
6. Fade out. (0.5s)

### Subtitle / voiceover
"You download the Partenon, configure the heroes you need, and run missions. The installer is idempotent. One hundred eighty-four tests pass. And if you want help, there is a free ninety-minute workshop where you leave with a live dashboard and a thirty-day plan."

---

## Scene 7: The Mission (~25s)
**Purpose**: Close with the open-source call to action and the one-million goal.
**Layout**: FULL_CENTER. Big counter, repo link, final tagline.

### Visual elements
- Center: large counter starting at `10` and ticking up toward `1,000,000`.
- Below counter: `"installations"`.
- Repo URL: `github.com/cuentadeservicio377-cell/partenon`.
- Final line: `"Hermes is the agent. The Partenon is the home."`
- Closing: `"Open Source Must Win."`

### Animation sequence
1. Write `"The mission"`. (1.0s)
2. Show the counter at 10, then animate it rising toward 1,000,000. (3.0s)
3. Write `"installations"` below. (1.0s)
4. Fade in the repo URL. (1.0s)
5. Write the final tagline. (1.5s)
6. Write `"Open Source Must Win."` (1.5s)
7. Hold. (2.0s)
8. Fade out. (0.5s)

### Subtitle / voiceover
"The goal is one million installations. Because every install means one more business spending less time on busywork and more time on product, customers, and growth. The repo is open. Hermes is the agent. The Partenon is the home. Open source must win."

---

## Voiceover Script (full, ~420 words)

"Most AI tools today are oracles. You ask. They answer. Then you go back to your spreadsheet, your inbox, and do the work yourself.

Hermes is different. Hermes is an agent: it can act. But an agent without structure is just a clever assistant that wanders off. So I built a home for it. I called it The Partenon.

The Partenon is a system of seven Hermes profiles that share one business context. The Scribe handles finance. The Herald handles communications. The Collector handles payments. The Guardian handles security. The Strategist handles operations. The Diplomat handles relationships. And the Brain holds the memory they all share.

Every capability is tagged. LIVE runs the moment you install. CONNECT works after you add your own Stripe or Google credentials. ROADMAP is not built yet, and we say so on every card. No credentials are required to explore.

A founder asks. Hermes routes the intent through partenon-core. The core dispatches the right hero. The hero calls the tool it needs: Google Workspace, Stripe, or G-Brain memory.

You download the Partenon, configure the heroes you need, and run missions. The installer is idempotent. One hundred eighty-four tests pass. And if you want help, there is a free ninety-minute workshop where you leave with a live dashboard and a thirty-day plan.

The goal is one million installations. Because every install means one more business spending less time on busywork and more time on product, customers, and growth. The repo is open. Hermes is the agent. The Partenon is the home. Open source must win."

---

## Scene Timing Summary
| Scene | Duration |
|-------|----------|
| 1. The Oracle Problem | ~18s |
| 2. Hermes Needs a Home | ~20s |
| 3. The Seven Heroes | ~45s |
| 4. Honest Status Tags | ~25s |
| 5. Architecture Flow | ~22s |
| 6. Install and Run | ~25s |
| 7. The Mission | ~25s |
| **Total** | **~180s = 3:00** |

If editing down to 2:20–2:40, trim waits in Scenes 1, 4, 5, and 6.

---

## Production Notes
- Render each scene independently with `manim -ql script.py SceneName` for drafts.
- Stitch with ffmpeg concat after final `-qh` renders.
- All text uses `Text`, no `MathTex`.
- Use monospace font `"Menlo"` throughout.
- Keep animations to `transform` and `opacity` only.
- Every scene ends with `FadeOut(Group(*self.mobjects))`.
