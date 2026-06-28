# Plan Maestro — Partenon Final Transformation

> Estado: Fase 3 completada. Preparando Fase 4 — Real-Time Dashboard + API.
> Plan detallado: `docs/superpowers/plans/2026-06-28-partenon-final-master-plan.md`

## Fases

### Fase 0 — Contaminants Cleanup ✅
- [x] Escanear y eliminar secretos, PII y datos contaminantes
- [x] Borrar código muerto y stubs
- [x] Anonimizar datos de workshop y ejemplos
- [x] Renombrar perfiles a nombres canónicos en inglés
- [x] Estandarizar `config.yaml` de todos los perfiles
- [x] Eliminar credenciales por defecto del dashboard
- [x] Reemplazar llamadas a `gbrain` binary por MCP server local
- [x] Agregar `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, `NOTICE.md`
- [x] Hacer `install.sh` idempotente y seguro
- [x] Verificar CI: lint, tests, build, secret scan

### Fase 1 — Hermes-Native Foundation (3 semanas)
- [ ] Crear root `distribution.yaml` y `pyproject.toml`
- [ ] Convertir `partenon-core/tools/` en skills de Hermes
- [ ] Construir `mcp_servers/` wrappers para cada dominio
- [ ] Empaquetar G-Brain como `partenon-memory` MCP server
- [ ] Cablear perfiles a MCP servers vía `config.yaml` canónico
- [ ] Verificar `hermes profile install` end-to-end

### Fase 2 — Hero Final Design + MCP Wrappers (4 semanas)
- [ ] Finalizar tool lists y comportamiento dry-run/live de los 7 héroes
- [ ] Reescribir `SOUL.md` y `SKILL.md` para cada héroe
- [ ] Implementar dry-run wrappers en cada MCP server
- [ ] Definir eventos de handoff de colaboración
- [ ] Agregar tests de interacción de ejemplo para cada héroe

### Fase 3 — Real Integrations (6 semanas)
- [ ] Seleccionar y fijar un Google Workspace MCP server
- [ ] Conectar Google Workspace a Scribe, Herald, Strategist, Diplomat
- [ ] Conectar Stripe MCP a Collector
- [ ] Conectar Gmail/Calendar MCP
- [ ] Agregar Slack MCP para notificaciones del Strategist
- [ ] Implementar auditoría de keys y recomendaciones de modelos del Guardian
- [ ] Agregar handler de Stripe webhooks

### Fase 4 — Real-Time Dashboard + API (4 semanas)
- [ ] Construir backend FastAPI con misiones, héroes, cron, integraciones, búsqueda de memoria, SSE
- [ ] Refactorizar dashboard Next.js para consumir la API
- [ ] Implementar Server-Sent Events para actualizaciones de misión
- [ ] Agregar auth JWT con secret generado
- [ ] Agregar fundamento de aislamiento por workspace/empresa

### Fase 5 — Gateway Messaging (3 semanas)
- [ ] Configurar gateway de Hermes para Telegram y Email
- [ ] Definir namespace de comandos e intent routing fallback
- [ ] Agregar routing de archivos adjuntos
- [ ] Agregar reglas de group-chat y allowlists
- [ ] Construir onboarding conversacional progresivo

### Fase 6 — Deployment World (4 semanas)
- [ ] Reescribir `docker-compose.yml` con todos los servicios
- [ ] Dockerfiles con usuarios non-root y health checks
- [ ] GitHub Actions CI/CD
- [ ] Expandir test suite (unit, integration, E2E)
- [ ] Logging estructurado, métricas Prometheus, health endpoints
- [ ] Proceso de release: SemVer, changelog, tags firmados

### Fase 7 — Website Reality (2 semanas)
- [ ] Auditar cada claim en las páginas de marketing
- [ ] Reescribir copy para distinguir live/credentials/roadmap
- [ ] Crear `web/capabilities.html` desde `docs/CAPABILITIES.md`
- [ ] Actualizar screenshots y README

## Criterios de Éxito

- Fase 1 entrega un paquete instalable por `hermes profile install` con skills y MCP servers funcionando en dry-run.
- Cada héroe tiene un `config.yaml` canónico, `SOUL.md` y `SKILL.md` coherentes.
- El dashboard puede autenticarse con secret generado y mostrar estado local.
- CI pasa en cada push (tests, lint, build, secret scan).
- No hay secretos reales, PII ni datos contaminantes en el repositorio.

## Riesgos

- Integraciones live requieren credenciales reales y cuentas de prueba.
- Poco tiempo antes del hackathon/deadline.
- Riesgo de sobre-ingeniería si no se mantiene scope-guard activo.
