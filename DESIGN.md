# Design System: Partenon

## 1. Visual Theme & Atmosphere

A restrained, dark-interface system for a hackathon landing + technical documentation. The atmosphere is technical but warm — like a Nous Research sub-product: flat, confident, and readable. Marketing page uses asymmetric editorial layouts; technical page uses dense, diagram-driven architecture.

- **Density:** Daily App Mode (4–7) for marketing; Cockpit Dense (7–9) for technical specs.
- **Variance:** Offset Asymmetric (6–8) on desktop, collapsing to strict single-column on mobile.
- **Motion:** Fluid CSS (4–7). Soft scroll reveals, spring-like hover physics, animated counters. No continuous scroll listeners.

## 2. Color Palette & Roles

| Token | Hex | Role |
|-------|-----|------|
| **Void Black** | `#050505` | Primary background (near-OLED, not pure black) |
| **Deep Surface** | `#0a0a0a` | Cards, elevated surfaces |
| **Panel Surface** | `#111111` | Inner card surfaces, code blocks |
| **Primary Text** | `#f5f5f5` | Headings and body |
| **Muted Text** | `#9a9a9a` | Descriptions, labels, metadata |
| **Hairline** | `rgba(255,255,255,0.08)` | Borders, dividers, card outlines |
| **Nous Purple** | `#7F77DD` | Primary accent: hero highlights, Hermes, CTAs |
| **Tool Teal** | `#1D9E75` | Secondary accent: Mensajero, Estratega, success |
| **Stripe Coral** | `#D85A30` | Tertiary accent: Cobrador, Guardián, Diplomático |
| **Nous Cream** | `#C9A227` | Quaternary accent: Stripe/Nous touch, milestones |

**Rules:**
- Max 3 visible accents at once; never glow/gradient.
- No pure `#000000`.
- No warm/cool gray mixing: all neutrals are neutral-leaning-warm `#050505` → `#f5f5f5`.

## 3. Typography

- **Display:** `Clash Display` — tight tracking (`tracking-tight`), weight-driven hierarchy.
- **Body:** `Geist` — relaxed leading (`leading-relaxed`), max 65ch paragraphs.
- **Mono:** `JetBrains Mono` — code, file names, numbers, metrics.
- **Banned:** Inter, Roboto, Arial, Open Sans, Helvetica, generic serif fonts.

## 4. Component Stylings

- **Buttons:**
  - Primary: filled Nous Purple `#7F77DD`, near-black text, `rounded-full`, `px-6 py-3`.
  - Secondary: transparent with Hairline border, white text, `rounded-full`.
  - Active: `scale-[0.98]` / `-translate-y-[1px]` tactile feedback.
  - Hover: border or background shift; no outer glow.
- **Cards:**
  - Background `#0a0a0a`, border `1px solid rgba(255,255,255,0.08)`, radius `12px`–`16px`.
  - Used only when grouping complex information; otherwise use negative space and dividers.
- **Tags / Pills:** `rounded-full`, `text-[10px] uppercase tracking-[0.2em]`, Hairline border, Muted Text.
- **Code:** JetBrains Mono, Nous Purple color.
- **Diagrams (Mermaid):** flat dark theme, hairline borders, no shadows/glows.

## 5. Layout Principles

- Contain page layouts with `max-w-6xl` / `max-w-7xl` centered.
- Desktop: asymmetric grids, left-aligned headlines, split screens.
- Mobile (< 768px): aggressive single-column collapse, `w-full`, `px-4`/`px-6`, no horizontal overflow.
- Full-height sections use `min-h-[100dvh]`, never `h-screen`.
- Use CSS Grid for multi-column structures; avoid flexbox percentage math.

## 6. Motion & Interaction

- Scroll reveals via `IntersectionObserver`: `translate-y-[20px] opacity-0` → `translate-y-0 opacity-1`, duration ~700ms, easing `cubic-bezier(0.32, 0.72, 0, 1)`.
- Counters animate with `requestAnimationFrame`, ease-out-cubic, tabular nums.
- Hover transitions: `transition-all duration-300 cubic-bezier(0.16, 1, 0.3, 1)`.
- No layout-property animations (`width`, `height`, `top`, `left`).
- `backdrop-blur` only on fixed navbar.

## 7. Anti-Patterns (Banned)

- No emojis.
- No Inter / generic fonts.
- No pure black `#000000`.
- No neon/outer glow shadows.
- No gradients (background or text).
- No 3-column equal-card feature rows.
- No AI copywriting clichés: “Elevate”, “Seamless”, “Unleash”, “Next-Gen”.
- No fake round numbers (`99.99%`, `50%`).
- No centered hero sections when variance > 4.
- No `h-screen`.
