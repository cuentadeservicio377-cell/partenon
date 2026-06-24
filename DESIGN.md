# Design System — Partenon

## Product Context

Partenon es un sistema de agentes IA para empresas, presentado como un panteón de héroes al servicio de Hermes. El proyecto se construye para un hackathon con jurado de Nous Research, Nvidia y Stripe. La primera entrega son dos páginas web:

1. **Página de marketing (`web/index.html`)** — manual de marca con storytelling, arquetipos, héroes, impacto y go-to-market.
2. **Página técnica (`web/developers.html`)** — espejo técnico con arquitectura, diagramas, fichas de agentes, integraciones y workshop.

## Aesthetic Direction

- **Direction:** Técnico-diagramático, inspirado en Nous Research / Hermes Agent.
- **Decoration level:** minimal.
- **Mood:** Oscuro, plano, preciso, de documentación viva. Sin cursilería, sin gradientes, sin glows, sin sombras difusas.
- **Reference:** https://hermes-agent.nousresearch.com

## Typography

- **Display/Hero:** Clash Display — grande, directo, peso 500-600.
- **Body:** Geist — legible, peso 400-500.
- **UI/Labels:** Geist — mismo que body, tamaños pequeños, tracking amplio en etiquetas.
- **Data/Tables:** JetBrains Mono — tabular-nums para contadores y métricas.
- **Code:** JetBrains Mono.
- **Loading:** Fontshare (Clash Display) + Bunny Fonts (Geist, JetBrains Mono) + Google Fonts (Instrument Serif para acentos serifos ocasionales).
- **Scale:**
  - Hero: 4rem - 8rem (responsive)
  - H2: 2.5rem - 4rem
  - H3: 1.5rem - 2rem
  - Body: 1rem - 1.125rem
  - Small/labels: 0.75rem - 0.875rem

## Color

- **Approach:** restrained / semantic por categoría.
- **Background:** `#050505`
- **Surface:** `#0a0a0a`
- **Surface 2:** `#111111`
- **Text:** `#f5f5f5`
- **Muted:** `#9a9a9a`
- **Acento primario (purple):** `#7F77DD` / `#534AB7`
- **Acento secundario (teal):** `#1D9E75`
- **Acento terciario (coral):** `#D85A30`
- **Bordes:** `rgba(255,255,255,0.08)` o colores de rampa atenuados.
- **Semantic:**
  - success: `#1D9E75`
  - warning: `#D85A30`
  - error: `#E24B4A`
  - info: `#378ADD`
- **Diagram colors (Nous style):**
  - UI / user: `c-gray` #888780
  - Core / router: `c-purple` #7F77DD
  - Profiles / skills: `c-teal` #1D9E75
  - Brain / memory: `c-coral` #D85A30
  - Data / payments: `c-blue` #378ADD

## Spacing

- **Base unit:** 4px
- **Density:** comfortable
- **Scale:** 2xs(2) xs(4) sm(8) md(16) lg(24) xl(32) 2xl(48) 3xl(64) 4xl(96)
- **Section padding:** py-24 to py-32 desktop, py-16 mobile.
- **Max content width:** 1280px (max-w-7xl) para contenido denso; 1024px (max-w-5xl) para lectura.

## Layout

- **Approach:** grid-disciplined con momentos editoriales.
- **Grid:** 12 columns en desktop, 1 en mobile.
- **Border radius:** sm 8px, md 12px, lg 16px, xl 24px.
- **Cards:** planas, borde fino (1px), fondo surface, sin sombra.

## Motion

- **Approach:** minimal-functional.
- **Easing:** `cubic-bezier(0.32, 0.72, 0, 1)` para entradas.
- **Duration:** micro 100ms, short 200ms, medium 400ms, long 700ms.
- **Scroll reveals:** fade-up sutil con IntersectionObserver.
- **No blur, no glow, no gradient animations.**

## Components

### Cards
- Fondo `#0a0a0a` o `#111111`.
- Borde 1px `rgba(255,255,255,0.08)`.
- Esquinas 12px-16px.
- Padding 24px-32px.
- Sin sombra, sin glow.

### Buttons
- Primary: fondo `c-purple` #7F77DD, texto blanco/negro, esquinas redondeadas.
- Secondary: borde fino, fondo transparente.
- Ghost: texto con underline animado.

### Diagrams
- Estilo Nous: nodos con bordes 0.5px-1px, esquinas 8px, colores por categoría.
- Mermaid theme `base` con colores personalizados.
- Conectores finos, flechas pequeñas.

### Labels / Tags
- Pill shape, borde fino, texto small uppercase tracking amplio.

## Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-06-23 | Initial design system created | Basado en transcrip y estética Nous Research / Hermes Agent. |
| 2026-06-23 | Paleta cambiada de dorado a púrpura/teal/coral | Para alinearse con la estética real de Nous Research. |
