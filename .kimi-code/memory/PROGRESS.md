# Progreso

## Historial de Sesiones

### 2026-06-26 — Perfil `partenon-mensajero` creado
- Creado `hermes/profiles/partenon-mensajero/` como distribucion de Hermes Agent.
- Archivos: `SOUL.md`, `config.yaml`, `.env.example`, `templates/.design.example`, `cron/weekly-content.json`.
- Skill `comms` con `SKILL.md` y tres tools Python:
  - `brand_intake.py`: entrevista de marca y generacion de `.design`.
  - `content_calendar.py`: calendario de contenido semanal/mensual con contexto de marca.
  - `copy_generator.py`: copy para ads, emails, posts y landing con QA anti-slop.
- Tools verificados con `python3 -m py_compile` y ejecucion de prueba.
- Actualizado `TODOS.md`.
- Commit `c0bcf85`.

### 2026-06-24 — Rediseño Nous-style de las páginas web
- Plan aprobado para reestructurar `web/index.html` y `web/developers.html` con estética Nous Research / manual técnico open source y reglas anti-AI-slop.
- Actualizado `DESIGN.md` con tokens visuales y reglas de copy anti-slop.
- Reescrito `web/index.html`:
  - Hero con título monospaced.
  - Sección "Manual de dos caras" como entrada.
  - Fichas de los 6 perfiles con archivo, herramientas y conexiones.
  - Contador 10 → 1M con métricas de proyección.
  - Go-to-market, instalación y Google Workspace.
- Reescrito `web/developers.html`:
  - Más diagramas Mermaid: arquitectura general, secuencia de misión, 4 conexiones por perfil, MCP/G-Brain, workshop.
  - Fichas técnicas con framework, skills, tools, MCP, inputs/outputs.
  - Estructura de repositorio con archivos `.finance`, `.design`, `.payments`, `.security`, `.ops`, `.relations`.
  - Workshop técnico de 90 min con diagrama de secuencia.
- Actualizados `README.md`, `SPEC.md`, `AGENTS.md`, `TODOS.md`.
- Capturas desktop/mobile regeneradas con Playwright.
- Commit `e786b18`.

## Features Completadas
- Perfil `partenon-mensajero` creado con skill comms, tools Python y cron semanal.
- Páginas web de marketing y técnica rediseñadas y commiteadas.
- Sistema visual Nous-style aplicado.
- Documentación del proyecto sincronizada.

## Bloqueadores Resueltos
- Ninguno.
