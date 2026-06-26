# Partenon

[![Site](https://img.shields.io/badge/live-hermespartenon.online-00D4FF)](https://hermespartenon.online/)

> Sistema operativo de agentes IA para pymes, presentado como un panteón de héroes al servicio de Hermes. Proyecto para el hackatón Nous Research / NVIDIA / Stripe.
>
> 🌐 **Sitio web**: [https://hermespartenon.online/](https://hermespartenon.online/)
> 📦 **Repositorio**: [https://github.com/cuentadeservicio377-cell/partenon](https://github.com/cuentadeservicio377-cell/partenon)

## Qué es

Partenon organiza agentes de IA como un sistema operativo:

- **Hermes** = la empresa (no un CEO, no un chatbot). Es el dios que publica misiones porque necesita ayuda.
- **Los héroes** = siete agentes especializados que toman misiones del Partenón.
- **El Partenón** = la unión de Hermes + sus héroes.
- **Pegaso** = las herramientas de cada héroe: skills, MCPs, APIs y plataformas open source.
- **G-Brain de Garry Tan** = el cerebro que conecta todo por MCP.
- **Google Workspace** = la superficie donde trabajan empresa y agentes.

## Documentación

- [`docs/for-founders.md`](docs/for-founders.md) — Guía para emprendedores: qué es Partenon, los 7 héroes, ejemplos y plan de crecimiento.
- [`docs/for-developers.md`](docs/for-developers.md) — Guía técnica completa: stack, arquitectura, instalación, API y workshop.
- [`docs/architecture.md`](docs/architecture.md) — Visión general de la arquitectura y flujo de misiones.

## Las tres páginas maestras

La documentación del sistema vive en tres páginas web estáticas migradas desde la app React `Kimi_Agent_10 Storytelling Web Sites/app`.

1. **`web/index.html`** — Página de marketing. Hero gateway de dos paneles, el mito de los arquetipos, los 7 héroes, proceso de 4 pasos, contadores de impacto con milestone bar, growth plan y CTA.
2. **`web/heroes.html`** — Página de detalle de cada héroe: perfiles completos, capacidades, herramientas, matriz comparativa y workflow interconectado.
3. **`web/developers.html`** — Documentación técnica. Arquitectura, especificaciones de héroes, protocolo MCP, patrones de flujo de datos, workshop de instalación, instrucciones de instalación y referencia de CLI/API.

4. **`dashboard/`** — Dashboard de operaciones (Next.js 15 + React 19 + TypeScript + Tailwind CSS). Muestra KPIs, kanban de misiones filtrado por perfil, administrador de cron jobs y auth simple por cookie. Lee y escribe `data/tasks.json` y `data/cron.json`.

Las páginas web usan HTML estático, Tailwind CSS vía CDN, Google Fonts (Cinzel, Inter, JetBrains Mono) y JavaScript vanilla. La paleta es la de la app original: mármol `#F7F5F0`, pergamino `#EDE8DF`, deep-stone `#2A2A2E`, midnight `#1A1A1E`, acentos por héroe.

## Los 7 héroes

| Héroe | Rol | Descripción |
|-------|-----|-------------|
| The Scribe | Finance | Hojas de cálculo, modelos financieros, dashboards y análisis. |
| The Herald | Communication / Marketing | Voz de marca, contenido, redes, SEO/GEO, calendario. |
| The Collector | Payments / Stripe | Cobros, suscripciones, facturas, control de gastos. |
| The Guardian | Security / NVIDIA | API keys, políticas, sandbox, routing de modelos, auditoría. |
| The Strategist | Operations / PM | Calendario, tareas, recordatorios, briefings, cron. |
| The Diplomat | Relations | Clientes, proveedores, contratos, seguimiento. |
| The Brain | Intelligence | G-Brain, memoria colectiva, orquestación del conocimiento. |

## Flujo de trabajo

1. **Hermes pregunta**: ¿qué empresa es? ¿qué necesitas ordenar?
2. **Hermes divide en misiones**: convierte la intención en tareas publicadas en el Partenón.
3. **El héroe toma**: lee su perfil, consulta G-Brain y empieza a trabajar con el emprendedor.
4. **Entrega en Google Workspace**: el resultado vive en Sheets, Docs, Slides o Calendar para que todos lo vean.

## Stack

- **Frontend páginas**: HTML estático + Tailwind CSS CDN + JS vanilla
- **Agent core**: Hermes Agent (Nous Research) + Python skills + `partenon-core` (router, onboarding, workflow, eval loop)
- **Sandbox / orquestación**: NVIDIA NemoClaw + OpenShell (alpha / early preview)
- **Modelos**: NVIDIA Nemotron 3 Ultra / Super, OpenAI, Kimi / Moonshot
- **Dashboard**: Next.js 15 + React 19 + TypeScript + Tailwind (en `dashboard/`)
- **Documentos**: Python + WeasyPrint (Kami v3)
- **Datos**: Google Workspace (Sheets, Docs, Slides, Drive, Calendar, Gmail); plantillas Excel con openpyxl
- **Pagos**: Stripe API + Stripe Skills de Hermes (`stripe-link-cli`, `mpp-agent`, `stripe-projects`)
- **Memoria / orquestación**: G-Brain de Garry Tan vía MCP, Hermes `MEMORY.md`/`USER.md`
- **Mensajería**: Hermes messaging gateway: Telegram, WhatsApp, Slack, Discord, Email y múltiples plataformas más
- **Infraestructura**: Docker / Docker Compose

## Demo funcional

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/demo_tesorero.py
```

Esto crea:

- `data/sample_gastos.xlsx` — libro con hojas Dashboard, Ingresos, Gastos Fijos, Gastos Variables y Proveedores.
- `data/sample_gastos_report.json` — ingresos, gastos fijos, gastos variables, margen y alertas.

## Dashboard

```bash
cd dashboard
npm install
npm run dev
```

Abre http://localhost:3000 y entra con usuario `admin` y contrasena `partenon` (configurable via `DASHBOARD_APP_USERNAME` y `DASHBOARD_APP_PASSWORD`). Lee y escribe `data/tasks.json` y `data/cron.json` relativos a la raiz del proyecto.

## Estado

- Iniciado: 2026-06-23
- **Repositorio público**: [github.com/cuentadeservicio377-cell/partenon](https://github.com/cuentadeservicio377-cell/partenon)
- **Sitio web desplegado**: [https://hermespartenon.online/](https://hermespartenon.online/)
- Fase actual: Repositorio público creado con 7 perfiles de Hermes, documentación completa y scripts de instalación.
- Perfiles implementados: Tesorero (`.finance`), Mensajero (`.design`), Cobrador (`.payments`), Guardian (`.security`), Estratega (`.ops`), Diplomático (`.relations`), Brain (`.brain`).
- Web verificada: `web/index.html`, `web/heroes.html` y `web/developers.html` en desktop (1440px) y mobile (390px). Screenshots actualizadas en `screenshots/`. HTML validado.
- Dashboard verificado: `npm install` y `npm run build` pasan sin errores de TypeScript.
- Demo verificado: `python scripts/demo_tesorero.py` genera Excel + JSON con métricas.
- Próxima tarea: Implementar eval loop funcional en el Tesorero, probar Stripe Skills en sandbox y configurar onboard de NVIDIA NemoClaw.

## Instalación rápida

```bash
git clone https://github.com/cuentadeservicio377-cell/partenon.git
cd partenon

# Opción A: instalador bash
./install.sh

# Opción B: setup con Python
python scripts/setup_hermes.py

# Opción C: onboard con NVIDIA NemoClaw (alpha)
curl -fsSL https://www.nvidia.com/nemoclaw.sh | NEMOCLAW_AGENT=hermes bash
```

Luego:
1. Copia `.env.example` a `.env` y completa tus credenciales.
2. Copia el Google Sheet base desde `templates/google-sheet-base/`.
3. Corre `python scripts/demo_tesorero.py` para verificar la instalación.
4. Abre el dashboard: `cd dashboard && npm install && npm run dev`.

## Repositorios relacionados

- [Hermes Agent](https://hermes-agent.nousresearch.com/)
- [NVIDIA NemoClaw](https://www.nvidia.com/en-us/ai/nemoclaw/)
- [NVIDIA OpenShell](https://github.com/NVIDIA/openshell)
- [Stripe Agent Toolkit](https://github.com/stripe/ai)
- [Open Design](https://github.com/nexu-io/open-design)
- [G-Brain](https://github.com/garrytan/gbrain)

## Memoria del proyecto

Ver [`.kimi-code/memory/`](.kimi-code/memory/)
