# AGENTS.md — Partenon

## Golden Rules
1. **Always commit** at session close: `git add -A && git commit -m "type: description"`
2. **Always update TODOS.md** before finishing
3. **Always verify visually** that HTML pages look right after important changes
4. **Focus on functional results**, not just code
5. **Do not break the build** — verify before commit
6. **Keep narrative consistency** between `index.html` (marketing) and `developers.html` (technical)

## Stack
- **Web pages**: Static HTML + Tailwind CSS CDN + vanilla JavaScript
- **Typography**: Space Grotesk (display), Geist (body), JetBrains Mono (mono/data and technical hero)
- **Aesthetic**: Nous Research / open-source technical manual with anti-slop. Background `#050505` / `#08080C`, cyan accent `#00D4FF` (saturation <80%), surgical amber `#FFB800`, double-bevel cards, floating fluid-island nav, 1px hairline borders, asymmetric/bento layouts. No massive gradients or generic glows.
- **Agents**: Hermes Agent (Nous Research) + Python skills
- **Future dashboard**: Next.js 15 + React 19 + TypeScript + Tailwind
- **Data / workspace**: Google Workspace (Sheets, Docs, Slides, Drive, Calendar, Gmail)
- **Payments**: Stripe API
- **Memory**: G-Brain by Garitán via MCP
- **Local deploy**: Docker / Docker Compose

## Conventions
- Use Tailwind classes extended via inline `tailwind.config` in each HTML file.
- Do not use banned fonts: Inter, Roboto, Arial, Open Sans, Helvetica.
- Do not use thick icons; prefer Material Symbols Sharp weight 300.
- Animations only with `transform` and `opacity`; never animate `width`, `height`, `top`, `left`.
- `backdrop-blur` only on fixed navbar or overlays, never on scrollable containers.
- Mobile-first: every asymmetric layout must collapse to `w-full` + `px-4` below 768px.
- Mermaid diagrams with `base` theme and flat Partenon colors (dark backgrounds, thin borders).
- Copy without em-dashes, intensifiers, filler phrases, or AI clichés.

## Do NOT touch without asking
- The structure of the 6 heroes (Treasurer, Messenger, Collector, Guardian, Strategist, Diplomat).
- The relationship "Hermes = company" (not CEO).
- The Nous-style aesthetic direction and the cyan `#00D4FF` / amber `#FFB800` palette.
- The 10 → 1M counter and its impact metrics.

## Closing Checklist
- [ ] Pages look good on desktop (1440px) and mobile (390px)
- [ ] No banned fonts or icons
- [ ] Mermaid renders without errors
- [ ] Commit done
- [ ] TODOS.md updated
- [ ] README.md updated if scope changed
