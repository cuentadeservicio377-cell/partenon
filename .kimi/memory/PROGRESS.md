# Progreso

## Historial de Sesiones

### 2026-06-26 — Fase 3: Real Integrations completada
- Creado adaptador `mcp_servers/google_workspace/` con cliente y servidor FastMCP para Sheets, Docs, Slides, Calendar y Gmail.
- Cableados Scribe, Herald, Strategist y Diplomat a `partenon-google-workspace`; actualizados `config.yaml`, `SOUL.md` y `SKILL.md`.
- Implementado Stripe live mode en `mcp_servers/payments/server.py`: payment links, invoices, subscriptions, charges, income report, pending/overdue, fraud monitoring.
- Creado `mcp_servers/payments/webhook.py` con endpoint `/webhooks/stripe` que valida firma y emite `payment_confirmed` al workflow engine.
- Creado adaptador Slack en `mcp_servers/notifications/slack.py` y MCP server `partenon-slack`; añadida acción `notify_slack` al workflow de tareas vencidas.
- Implementado Guardian key audit y model recommendation en `mcp_servers/security/key_manager.py`.
- Añadidos tests: `test_google_workspace_adapter.py`, `test_stripe_live.py`, `test_stripe_webhook.py`, `test_slack_adapter.py`, `test_guardian_key_manager.py`; extendido `test_handoffs.py`.
- Checks PASS: `python -m pytest tests/` (59 tests), `npm run lint`, `npm run build`, secret scan, `bash -n install.sh`.
- Actualizados `.env.example`, `pyproject.toml`, `requirements.txt`, `README.md`, `CHANGELOG.md`, `TODOS.md`, `MEMORY.md`, brain central y gbrain.

### 2026-06-26 — Fase 2: Hero Final Design + MCP Wrappers completada
- Finalizadas listas de herramientas dry-run/live para los 7 héroes.
- Reescritos `SOUL.md` y `SKILL.md` de cada héroe con modos de operación, catálogo de herramientas MCP y tablas dry-run/live.
- Implementados wrappers dry-run en cada MCP server: `memory`, `finance`, `payments`, `comms`, `security`, `ops`, `relations`.
- Agregados 6 workflows de handoff de colaboración a `workflow_engine.py`: pago→scribe, presupuesto→scribe, acuerdo→ops/estratega, hito→diplomático, rotación de llaves→todos, aprendizaje→héroe objetivo.
- Creados `tests/test_mcp_servers.py` y `tests/test_handoffs.py` con 27 tests pasando.
- Checks PASS: `python -m pytest tests/` (31 tests), `npm run lint`, `npm run build`, secret scan, `bash -n install.sh`.
- Actualizados `TODOS.md`, `MEMORY.md`, brain central y este archivo.

### 2026-06-28 — Fase 1: Hermes-Native Foundation completada
- Renombrado `partenon-core/` a `partenon_core/` y convertido en paquete Python instalable con `pyproject.toml`.
- Creado `distribution.yaml` raíz y `distribution.yaml` dentro de cada uno de los 7 perfiles.
- Agregados skills Hermes `partenon-core`, `partenon-judge`, `partenon-workflows` bajo `skills/`.
- Movido `gbrain/` a `mcp_servers/memory/` como `partenon-memory`; creados wrappers dry-run para `finance`, `payments`, `comms`, `security`, `ops`, `relations`.
- Cableados todos los perfiles a los MCP servers de dominio vía `config.yaml` canónico.
- Verificado `hermes profile install hermes/profiles/partenon-*` para los 7 héroes.
- Actualizado `install.sh`, `scripts/setup_hermes.py`, `README.md`, `CHANGELOG.md`, `TODOS.md`.
- Todos los checks PASS: pytest (4), dashboard lint/build, secret scan, `bash -n install.sh`, py_compile de Python, importación de todos los MCP servers.
- Commit final de Fase 1: `fa491c3`.

### 2026-06-28 — Fase 0: install.sh seguro + CI
- Reescrito `install.sh` para que sea idempotente, seguro y robusto a paths con espacios.
- El instalador ahora detecta Python 3.10+, recrea `.venv` si usa Python obsoleto, genera `DASHBOARD_AUTH_SECRET`, `DASHBOARD_APP_USERNAME` y `DASHBOARD_APP_PASSWORD` en `.env` solo la primera vez, e instala perfiles canónicos en inglés en `$HOME/.hermes/profiles`.
- Agregado `pytest` a `requirements.txt`; `python -m pytest tests/` PASS (4 tests).
- Configurado ESLint en `dashboard` (`eslint-config-next`) y `npm run lint` PASS.
- Dashboard build (`npm run build`) PASS.
- Creado workflow `.github/workflows/ci.yml` y script `.github/scripts/secret_scan.py`.
- Secret scan local PASS; no se detectaron secretos hardcodeados por encima de placeholders.
- Actualizado `TODOS.md`: Fase 0 completada.

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
- Páginas web de marketing y técnica rediseñadas y commiteadas.
- Sistema visual Nous-style aplicado.
- Documentación del proyecto sincronizada.

## Bloqueadores Resueltos
- Ninguno.
