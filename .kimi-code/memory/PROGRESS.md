# Progreso

## Historial de Sesiones

### 2026-06-26 — Migración de `Heroes.tsx` a `web/heroes.html`
- Creada la página `web/heroes.html` como versión estática basada EXACTAMENTE en `Kimi_Agent_10 Storytelling Web Sites/app/src/pages/Heroes.tsx`.
- Stack: HTML5 estático + Tailwind CSS CDN + CSS personalizado; fuentes Cinzel, Inter, JetBrains Mono; iconos Material Symbols Sharp y SVG inline.
- Secciones migradas: Hero "Meet Your Heroes" con navegación rápida de 7 iconos, 7 perfiles detallados de héroes (Scribe, Herald, Collector, Guardian, Strategist, Diplomat, Brain), Comparison Matrix, Workflow Timeline de product launch de 7 pasos, CTA con copy-to-clipboard.
- Interactividad preservada: reveal on scroll con IntersectionObserver, hover cards/badges, copy-to-clipboard con toast, smooth scroll, mobile nav hamburguesa, navbar flotante que cambia entre tema claro/oscuro según sección.
- Correcciones aplicadas en TODO el contenido:
  - "Nose Research" → "Nous Research".
  - "Envidia" → "NVIDIA".
  - MCP connections presentados como integraciones/descripciones genéricas (Google Workspace, Stripe, NVIDIA, CRM, Email, Calendar, Social media APIs) en lugar de nombres de tools inventados.
  - Footer con créditos correctos: Nous Research, NVIDIA, Stripe.
- Validación HTML básica: OK.
- Actualizados `TODOS.md` y `PROGRESS.md`.

### 2026-06-26 — Migración de `Home.tsx` a `web/index.html`
- Reemplazada la página `web/index.html` anterior por una versión estática basada EXACTAMENTE en `Kimi_Agent_10 Storytelling Web Sites/app/src/pages/Home.tsx`.
- Stack: HTML5 estático + Tailwind CSS CDN + CSS personalizado; fuentes Cinzel, Inter, JetBrains Mono; iconos Material Symbols Sharp y SVG inline.
- Secciones migradas: Hero Gateway (dos paneles), The Myth, The Heroes (7 tarjetas: Scribe, Herald, Collector, Guardian, Strategist, Diplomat, Brain), How It Works (4 pasos), Impact Counter con milestone bar, Growth Plan (4 canales), Partners, CTA con typing effect.
- Interactividad preservada: reveal on scroll, hover de paneles/tarjetas, contadores animados con IntersectionObserver, efecto typewriter, copy-to-clipboard con toast, smooth scroll, mobile nav.
- Correcciones aplicadas en TODO el contenido:
  - "Nose Research" → "Nous Research".
  - "Envidia" → "NVIDIA".
  - Métricas inventadas etiquetadas como objetivos de diseño, hipótesis o proyecciones de adopción.
  - No se presentan MCP tools inventados; se usan descripciones genéricas o herramientas reales de Stripe / Google Workspace.
  - Matiz de alpha / early preview para NemoClaw / OpenShell.
  - "Kimi Coding" → "Kimi / Moonshot" en contenido heredado.
  - NVIDIA agent skills descritos correctamente.
  - Stripe Skills presentados como skills opcionales de Hermes, no productos Stripe.
  - Footer con créditos correctos y disclaimer de no afiliación oficial.
- Validación HTML básica: OK.
- Actualizados `TODOS.md` y `PROGRESS.md`.

### 2026-06-26 — Recuperación de storytelling desde `Kimi_Agent_10 Storytelling Web Sites/`
- Auditoría completa de `Kimi_Agent_10 Storytelling Web Sites/` con AgentSwarm. Se recuperaron patrones narrativos y de información técnica; se descartaron estética clásica (Cinzel, mármol, iconos figurativos), errores de marca ("Nose Research" → Nous Research) y el séptimo héroe "The Brain".
- Enriquecida `web/index.html`: sección de proceso de 4 pasos (intención → héroes → misiones → entrega), contadores animados con milestone bar 10 → 1M, métricas de impacto secundarias, growth plan de 4 canales (workshops, empresas piloto, partners técnicos, marketplace de perfiles), CTA tipeado con efecto de escritura y toast de copiado.
- Enriquecida `web/developers.html`: badges técnicos y tablas de especificación por héroe (rol, I/O, permisos, conexiones, Pegaso/toolkit, eval, MCP), API reference de G-Brain con tabla de métodos y ejemplos de código, workshop timeline visual de 4 fases, install tabs (Local / NemoClaw / Stripe / Variables) con feedback de copiado, badge "Hermes harness" en NVIDIA NemoClaw.
- Actualizado `scripts/capture.py` para forzar contadores `.stat-value` y regenerar screenshots.
- Actualizados `README.md` y `TODOS.md`.
- Regenerados screenshots desktop/mobile en `screenshots/`.
- Validados HTML de ambas páginas.
- Commit realizado.

### 2026-06-26 — Loop de reparación completo (3 fases)
- Reescrita `web/index.html` como especificación maestra de marketing con narrativa de arquetipos, Hermes=empresa, 6 héroes con Pegasos, ejemplos de construcción/cafetería, contador 10→1M, carta de intención de Pablo (PlayStation/LATAM/wsc.lat) y go-to-market detallado.
- Reescrita `web/developers.html` como espejo técnico con arquitectura Mermaid, secuencia de misión, fichas técnicas por héroe, diagramas de conexión por perfil, workshop de 90 min, estructura de repo y roadmap.
- Actualizados screenshots desktop/mobile en `screenshots/`.
- Actualizado `README.md` con narrativa nueva, Pegasos, flujo y estado.
- Actualizado `TODOS.md`.
- Actualizados 6 SOUL.md de perfiles con sección "Pegaso".
- Verificado `python scripts/demo_tesorero.py` PASS.
- Verificado `cd dashboard && npm run build` PASS.
- Commit final del loop realizado.

### 2026-06-26 — Perfil `partenon-estratega` completado
- Creado `hermes/profiles/partenon-estratega/` como distribucion de Hermes Agent.
- Archivos: `SOUL.md`, `config.yaml`, `.env.example`, `.ops`, `templates/.ops.example`, `cron/morning-briefing.json`, `cron/midday-pulse.json`, `cron/weekly-planning.json`, `cron/weekly-retro.json`.
- Skill `ops` con `SKILL.md` y cinco tools Python.
- Tools verificados con `python3 -m py_compile` y ejecucion de prueba.
- Actualizados `TODOS.md`, `CHANGELOG.md` y `README.md`.

### 2026-06-26 — Perfil `partenon-diplomatico` completado
- Completado `hermes/profiles/partenon-diplomatico/` como distribucion de Hermes Agent.
- Archivos nuevos: `skills/relations/tools/crm.py`, `skills/relations/tools/followups.py`.
- Tools verificados.
- Actualizados `TODOS.md` y `CHANGELOG.md`.

### 2026-06-26 — Perfiles `partenon-tesorero`, `partenon-mensajero`, `partenon-cobrador`, `partenon-guardian` creados
- Cada uno con SOUL.md, config.yaml, .env.example, templates y cron.
- Skills finance, comms, payments, security con tools Python.
- Tools verificados con `python3 -m py_compile`.

### 2026-06-24 — Rediseño Nous-style de las páginas web
- Plan aprobado para reestructurar `web/index.html` y `web/developers.html`.
- Actualizado `DESIGN.md` con tokens visuales y reglas de copy anti-slop.
- Commit `e786b18`.

## Features Completadas
- Páginas web maestras reconstruidas y commiteadas.
- Seis perfiles de Hermes con SOUL.md actualizados (incluyendo Pegaso).
- Demo Tesorero funcional.
- Dashboard Next.js con kanban y cron.
- Sistema visual Nous-style aplicado.
- Documentación del proyecto sincronizada.

## Bloqueadores Resueltos
- Ninguno.
