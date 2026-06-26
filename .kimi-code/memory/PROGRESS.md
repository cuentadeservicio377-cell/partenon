# Progreso

## Historial de Sesiones

### 2026-06-26 — Loop de mejora: integración NVIDIA/Stripe/Hermes
- Investigación con AgentSwarm sobre NVIDIA NemoClaw, OpenShell, Nemotron 3 Ultra, CUDA-X skills, Stripe Skills (`stripe-link-cli`, `mpp-agent`, `stripe-projects`) y funcionalidades core de Hermes Agent (skills, memory, cron, subagents, messaging gateway, MCP, self-improvement).
- Enriquecida `web/index.html`: hero con stack del hackathon, sección "Agentes que cobran, pagan y operan seguros", perfiles de héroes actualizados (Cobrador con Stripe Skills, Guardián con NemoClaw/OpenShell, Tesorero con cuDF/cuOpt, Estratega con cron/subagentes), sección "Hermes aprende de cada misión" con learning loop, cron y messaging gateway, contador de impacto corregido a "pymes", instalación con NemoClaw y Stripe Skills.
- Enriquecida `web/developers.html`: arquitectura Mermaid con NVIDIA NemoClaw/OpenShell/Nemotron y Stripe Skills, sección "NVIDIA y Stripe como infraestructura de agentes", perfiles técnicos actualizados, sección "Hermes es más que un modelo" con skills/memory/cron/subagents/gateway/MCP/self-improvement, ejemplos de Stripe Projects y cron, instalación y roadmap actualizados.
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
