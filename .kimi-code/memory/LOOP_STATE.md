# LOOP STATE: GitHub Repository Build for Partenon

## Goal
Crear un repositorio público en GitHub para Partenon que sea instalable y usable con Hermes Agent, que contenga toda la documentación descrita en las páginas web (para emprendedores y developers), los 7 perfiles de héroes, scripts de setup, y pase verificación de estructura, builds, demo y deploy.

## Verify (gates de éxito)
- [x] Gate 1: Repo creado en GitHub bajo la cuenta activa (`cuentadeservicio377-cell`) con nombre `partenon`, remote configurado y todo el código de `main` subido. (score: 10/10)
- [x] Gate 2: Estructura del repo refleja la arquitectura completa documentada en la web: `web/`, `dashboard/`, `hermes/profiles/` (7 héroes), `docs/`, `scripts/`, `install.sh`, `.env.example`, `README.md`. (score: 9/10)
- [ ] Gate 3: Documentación completa para emprendedores (`docs/for-founders.md`) y developers (`docs/for-developers.md`) basada en el contenido de `web/index.html`, `web/heroes.html` y `web/developers.html`. (score: __/10)
- [ ] Gate 4: Los 7 perfiles de Hermes tienen `SOUL.md`, `config.yaml`, `.env.example`, skills y tools funcionales; faltantes se crean o se marcan explícitamente como stubs con checklist. (score: __/10)
- [ ] Gate 5: Scripts de setup funcionan: `install.sh` descarga dependencias y `scripts/setup_hermes.py` instala perfiles en el directorio de Hermes Agent. (score: __/10)
- [ ] Gate 6: Builds/tests locales pasan: `python scripts/demo_tesorero.py` genera Excel+JSON sin errores y `cd dashboard && npm run build` termina exitosamente. (score: __/10)
- [ ] Gate 7: Directorio `web/` empaquetado (`web-deploy.zip`) y README incluye link al sitio live `https://hermespartenon.online/`. (score: __/10)

## Stop Conditions
- Todos los gates ≥ 7/10.
- Máximo de iteraciones alcanzado: 7.
- Si un mismo gate falla 2 veces seguidas sin progreso → escalación humana.

## Current State
- Iteración: 2 / 7
- Última acción: Completar estructura del repo con perfil Brain, .env.example global y setup script.
- Último resultado: 7 perfiles disponibles, install.sh y scripts/setup_hermes.py listos.

## Attempt Log
### Iteración 0
- Acción: Ajustar LOOP_STATE.md al scope completo de repositorio usable e instalable.
- Resultado: Spec ampliado a 7 gates y aprobado por usuario.
- Score: N/A
- Próximo paso: Iteración 1.

### Iteración 1
- Acción: Crear repo remoto y subir código base.
- Plan:
  1. Verificar autenticación `gh`.
  2. Crear repo `partenon` público.
  3. Limpiar secreto de Stripe del historial con `git filter-repo`.
  4. Configurar remote y push force.
- Resultado: Repo creado. Secreto `sk_test_[REDACTED]` eliminado del historial. Push exitoso.
- Score: Gate 1 = 10/10
- Próximo paso: Iteración 2 — completar estructura (`.env.example`, perfil Brain, setup script, limpiar pycache).

### Iteración 2
- Acción: Completar estructura del repo.
- Plan:
  1. Crear `.env.example` global con placeholders seguros.
  2. Crear perfil `partenon-brain` con SOUL.md, config.yaml, skill memory y cron.
  3. Actualizar `install.sh` para instalar 7 perfiles.
  4. Crear `scripts/setup_hermes.py` como helper de instalacion.
  5. Limpiar `__pycache__`.
- Resultado: `.env.example` global creado, perfil Brain completo, install.sh y setup script actualizados.
- Score: Gate 2 = 9/10
- Próximo paso: Iteración 3 — documentación completa para founders y developers.

## Human Escalation
Si durante la ejecución se requiere decisión sobre credenciales reales (Google Workspace, Stripe, G-Brain, NVIDIA) o cambio de arquitectura, se pausa el loop para input humano.
