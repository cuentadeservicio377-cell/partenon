# LOOP STATE: Partenon — Reparación completa (3 fases)

## Goal
Reconstruir Partenon a partir de los transcripts del usuario: primero las dos páginas web como especificación maestra, luego el repositorio alineado. Que todo refleje la narrativa de arquetipos, Hermes=empresa, 6 héroes con Pegasos, ejemplos concretos, contador 10→1M, go-to-market y carta de intención.

## Verify (gates de éxito)

- [x] **Gate 1 — Página de marketing (`web/index.html`)** (score: 8/10)
  - Refleja la narrativa del transcript: Partenón = Hermes (dios/empresa) + héroes; héroes toman misiones del Partenón.
  - Explica arquetipos sin cursilería; usa tono de storytelling de marketing.
  - Presenta los 6 héroes con ficha de héroe: personalidad, Pegaso (herramientas), misión, conexiones.
  - Incluye ejemplos concretos de construcción y cafetería.
  - Incluye sección "Pegaso" como concepto de herramientas de héroe.
  - Contador 10 → 1M con métricas coherentes (ingreso, calidad, orden, horas ahorradas, trabajos creados).
  - Go-to-market detallado: webinars quincenales, universidades/aceleradores, organizaciones (BNI, Way/Pio, cámaras, Rotary), coworkings, aceleradoras.
  - Carta de intención / paper de Pablo: analogía PlayStation, LATAM, wsc.lat, puesto de investigador de implementación, meta 1M instalaciones.
  - Talk about / dos páginas al inicio.
  - Estética Nous Research / anti-slop; responsive 1440px y 390px.
  - Build/visual check: screenshots desktop/mobile generados sin errores de render.

- [x] **Gate 2 — Página técnica (`web/developers.html`)** (score: 8/10)
  - Es espejo técnico de la página de marketing.
  - Arquitectura completa con diagramas Mermaid: flujo general, secuencia de misión, MCP/G-Brain, conexiones por perfil.
  - Ficha técnica por héroe: framework, skills, Pegaso/herramientas, MCPs, inputs/outputs, conexiones con otros héroes y APIs.
  - Workshop técnico de 90 min paquetizado: pre-instalación, onboarding, práctica.
  - Estructura de repositorio y comando de instalación.
  - Roadmap.
  - Mermaid renderiza sin errores en screenshots desktop/mobile.
  - Responsive y estética consistente con marketing.

- [x] **Gate 3 — Repositorio alineado con las páginas** (score: 7/10)
  - Perfiles `partenon-*` actualizados: se agregó sección "Pegaso" a cada SOUL.md con herramientas y conexiones descritas en las páginas.
  - `partenon-core` refleja el flujo: onboarding pregunta tipo de empresa y genera misiones iniciales para los 6 héroes.
  - Demo Tesorero funcional (`scripts/demo_tesorero.py`) genera Excel + JSON con métricas.
  - README.md reescrito con narrativa nueva, Pegasos, flujo y estado.
  - TODOS.md actualizado.
  - Dashboard Next.js `npm run build` pasa sin errores.
  - Demo Python corre sin errores.
  - Commit final realizado.

## Stop Conditions
- Todos los gates ≥ 7/10.
- Máximo de iteraciones alcanzado: 5 por gate.
- Costo/tiempo por iteración cae bajo umbral de utilidad.
- El usuario dice "para" / "stop" / "basta".

## Current State
- Iteración: 3 / 5
- Última acción: Gate 3 verificado y aprobado.
- Último resultado: Repositorio alineado, tests/build pasan, commit realizado.

## Attempt Log

### Iteración 0
- Acción: Crear LOOP_STATE.md con gates de las 3 fases.
- Resultado: Spec aprobado por usuario.
- Score: N/A
- Próximo paso: Ejecutar Fase 1.

### Iteración 1 — Fase 1: Marketing
- Acción: Reescribir `web/index.html` desde cero basado en el transcript.
- Resultado: Archivo reescrito. Screenshots desktop/mobile correctos.
- Score: 8/10
- Próximo paso: Iniciar Fase 2.

### Iteración 2 — Fase 2: Técnica
- Acción: Reescribir `web/developers.html` como espejo técnico.
- Resultado: Archivo reescrito. Mermaid y layout correctos.
- Score: 8/10
- Próximo paso: Iniciar Fase 3.

### Iteración 3 — Fase 3: Repositorio
- Acción: Alinear repositorio con las páginas web.
- Plan:
  1. Reescribir README.md con narrativa nueva.
  2. Actualizar TODOS.md.
  3. Agregar sección "Pegaso" a cada SOUL.md.
  4. Verificar demo Python y dashboard build.
  5. Commit final.
- Resultado: README y TODOS actualizados. Seis SOUL.md actualizados con Pegaso. Demo Python PASS. Dashboard build PASS. Commit realizado.
- Score: 7/10
- Próximo paso: Cerrar loop, actualizar PROGRESS.md y brain central.

## Human Escalation
_Ninguna por ahora_
