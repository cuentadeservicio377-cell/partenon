# Progreso

## Historial de Sesiones

### 2026-06-26 — Perfil `partenon-diplomatico` completado
- Completado `hermes/profiles/partenon-diplomatico/` como distribucion de Hermes Agent.
- Archivos ya existentes: `SOUL.md`, `config.yaml`, `.env.example`, `templates/.relations.example`, `cron/daily-followups.json`, `skills/relations/SKILL.md`.
- Archivos nuevos:
  - `skills/relations/tools/crm.py`: CRM adaptado de `hermes-ventas` para clientes, proveedores, hitos, contratos, comunicaciones y calificaciones.
  - `skills/relations/tools/followups.py`: seguimientos diarios, recordatorios y generación de mensajes formales.
- Tools verificados con `python3 -m py_compile` y ejecucion de prueba.
- Actualizados `TODOS.md` y `CHANGELOG.md`.

### 2026-06-26 — Perfil `partenon-tesorero` creado
- Creado `hermes/profiles/partenon-tesorero/` como distribucion de Hermes Agent.
- Archivos: `SOUL.md`, `config.yaml`, `.env.example`, `templates/.finance.example`, `cron/daily-report.json`.
- Skill `finance` con `SKILL.md` y cuatro tools Python:
  - `google_sheets.py`: lectura, escritura y creacion de dashboards en Google Sheets.
  - `parsers.py`: parseo de gastos desde Excel/CSV con inferencia de categoria y tipo fijo/variable.
  - `templates.py`: plantillas Excel de presupuesto, proveedores y flujo de caja.
  - `__init__.py`: exports del paquete finance.
- Tools verificados con `python3 -m py_compile`.
- Actualizado `TODOS.md`.
- Commit `606e8a4`.

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
- Perfil `partenon-diplomatico` completado con skill relations, CRM, follow-ups y cron diario.
- Perfil `partenon-tesorero` creado con skill finance, tools Python y cron diario.
- Perfil `partenon-mensajero` creado con skill comms, tools Python y cron semanal.
- Páginas web de marketing y técnica rediseñadas y commiteadas.
- Sistema visual Nous-style aplicado.
- Documentación del proyecto sincronizada.

## Bloqueadores Resueltos
- Ninguno.
