# DESIGN — Partenon (Nous-style / anti-slop)

## Identity

Partenon is an agent operating system for SMBs. The interface should read like an open-source technical manual from Nous Research: dark, monospaced, live data, no ornaments. It is not mythology. It is a system of operational archetypes that runs inside Google Workspace.

## Palette

| Token | Value | Usage |
|-------|-------|-------|
| `bg` | `#050505` | OLED base background |
| `surface` | `#08080C` | Alternate section surfaces |
| `panel` | `#0E0E14` | Code and diagram backgrounds |
| `panel-raised` | `#111118` | Double-bevel cards (inner core) |
| `panel-strong` | `#16161F` | Hover/focus states |
| `text` | `#E8E8ED` | Primary text |
| `muted` | `#6B6B78` | Secondary text |
| `dim` | `#45454F` | Metadata, soft borders |
| `accent` | `#00D4FF` | Single accent (surgical cyan) |
| `accent-dim` | `rgba(0, 212, 255, 0.10)` | Accent backgrounds |
| `accent-glow` | `rgba(0, 212, 255, 0.20)` | Subtle accent shadow |
| `live` | `#FFB800` | Live states, pings (surgical use) |
| `line` | `rgba(255, 255, 255, 0.07)` | Borders and dividers |
| `line-strong` | `rgba(255, 255, 255, 0.14)` | Hover borders |

### Color rules
- One primary accent. Amber (`#FFB800`) appears on no more than 2 elements per page.
- Accent saturation below 80%.
- No pure `#000000`. The background is `#050505`.
- No massive gradients. Only subtle radial meshes at ~3% opacity.

## Typography

| Role | Font | Weights |
|------|------|---------|
| Display / data | JetBrains Mono | 400, 500 |
| Headlines | Space Grotesk | 500, 600, 700 |
| Body | Geist | 400, 500 |
| Icons | Material Symbols Sharp | 300 |

### Scale
- Hero monospaced: `clamp(3.5rem, 10vw, 8.5rem)` / leading `0.88` / tracking `-0.055em`
- H2: `clamp(2.5rem, 5vw, 4rem)` / leading `0.95` / tracking `-0.04em`
- H3: `1.75rem` / leading `1.1` / tracking `-0.02em`
- Body: `1rem` / leading `1.6`
- Small/label: `0.7rem` / uppercase / tracking `0.14em`
- Mono/data: `0.875rem` / leading `1.4`

### Typographic rules
- No Inter, Roboto, Arial, Open Sans, Helvetica.
- Numbers in `font-variant-numeric: tabular-nums`.
- Headlines with presence: large, tight tracking, tight line-height.
- Body limited to ~65 characters per line.
- Technical manual effect: use mono for large titles, seed numbers, and states.

## Layout

- Container: `max-w-[1400px] mx-auto px-4 md:px-6`.
- Asymmetric grid by default. Bento with variable `col-span` combinations.
- Spacing: sections `py-24 md:py-32`.
- Corners: outer double-bevel `18px`, inner `12px`. Buttons `rounded-full` or deliberate `0`.
- Borders: 1px `line`, transition to `line-strong` on hover.
- Mobile-first: every asymmetric layout collapses to `w-full` + `px-4` below 768px.

## Background

- Base `#050505`.
- Fixed mesh gradient: 2-3 large radial accent orbs at ~3% opacity.
- Fixed noise SVG at `opacity-3.5`.
- Optional scanlines on data sections: `repeating-linear-gradient` at 2% opacity.

## Components

### Floating nav (fluid island)
- Fixed at top, centered, `border-radius: 999px`.
- `backdrop-blur: 16px`, background `rgba(8,8,12,0.72)`.
- Links `border-radius: 999px`, muted color, subtle background on hover.
- Mobile menu: full-screen overlay with staggered reveal.

### Buttons
- Primary: `accent` background, `bg` text, weight 500, `rounded-full`, padding `0.875rem 1.5rem`.
  - Hover: `translateY(-2px)` + tinted accent `box-shadow`.
  - Active: `scale(0.98)`.
- Secondary: 1px `line` border, `rgba(255,255,255,0.02)` background, `text` color, `rounded-full`.
  - Hover: `line-strong` border, `accent` text, `rgba(255,255,255,0.04)` background.
- Internal button icon: `w-7 h-7` circle, moves on hover.

### Cards (double-bevel)
- Outer shell: `rgba(255,255,255,0.025)` background, 1px `line` border, `border-radius: 18px`, padding `6px`.
- Inner core: `panel-raised` background, 1px `rgba(255,255,255,0.05)` border, `border-radius: 12px`, `box-shadow: inset 0 1px 0 rgba(255,255,255,0.04)`.
- Hover: outer border moves to `line-strong`.

### Labels / Tags
- Mono uppercase, tracking `0.14em`, size `0.7rem`, `muted` color.
- Format: uppercase keywords preceded by an accent dot.

## Animations

- Transitions: `cubic-bezier(0.16, 1, 0.3, 1)` duration 350-900ms.
- Scroll reveal: `opacity` + `translateY(32px)`, custom easing.
- Counters: numeric animation with `requestAnimationFrame`.
- No `linear` or `ease-in-out` by default.
- Only `transform` and `opacity`. Never `width`, `height`, `top`, `left`.

## Iconography

- Material Symbols Sharp via Google Fonts, weight 300.
- Fallback with inline SVGs.
- Forbidden: thick Lucide, generic FontAwesome, emojis.

## Forbidden anti-patterns

- No Inter, Roboto, Arial, Open Sans, Helvetica.
- No emojis.
- No massive gradients on text or backgrounds.
- No neon glows everywhere.
- No uniformly rounded cards without double-bevel.
- No symmetrical 3-equal-card layouts.
- No copy with "elevate", "boost", "revolutionize", "seamless".
- No em-dashes. Use a period or colon.
- No hollow claims without concrete data.
- No dramatic transitions: "dive in", "here's the thing", "but here's the kicker".
- No `h-screen` for hero; use `min-h-[100dvh]`.
- No arbitrary `z-50` or `z-[9999]`.

## Voice

Direct, technical, no ornaments. Every sentence ends in a verifiable fact. The heroes are operational profiles, not gods. Hermes is the company. The Partenon is the shared workplace. Empty adjectives and intensifiers are forbidden.
