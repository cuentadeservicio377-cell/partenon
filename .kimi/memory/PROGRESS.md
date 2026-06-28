# Progreso

## Historial de Sesiones

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
