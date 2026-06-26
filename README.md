# Partenon

> Sistema operativo de agentes IA para pymes, presentado como un panteón de héroes al servicio de Hermes. Proyecto para el hackatón Nous Research / NVIDIA / Stripe.

## Qué es

Partenon organiza agentes de IA como un sistema operativo:

- **Hermes** = la empresa (no un CEO, no un chatbot). Es el dios que publica misiones porque necesita ayuda.
- **Los héroes** = seis agentes especializados que toman misiones del Partenón.
- **El Partenón** = la unión de Hermes + sus héroes.
- **Pegaso** = las herramientas de cada héroe: skills, MCPs, APIs y plataformas open source.
- **G-Brain de Garitán** = el cerebro que conecta todo por MCP.
- **Google Workspace** = la superficie donde trabajan empresa y agentes.

## Las dos páginas maestras

La documentación del sistema vive primero en dos páginas web estáticas. A partir de ellas se construye el repositorio.

1. **`web/index.html`** — Página de marketing con arco narrativo: problema (pyme sin sistema), promesa (una mesa de trabajo viva), caso concreto (un día con Hermes en Cafetería Aurora), stack del hackathon (Hermes + NVIDIA NemoClaw/OpenShell + Nemotron 3 Ultra + Stripe Skills), héroes en tabs/acordeón, G-Brain, auto-mejora, messaging gateway, impacto sin números inventados, carta de intención abreviada, go-to-market enfocado e instalación.
2. **`web/developers.html`** — Página técnica. Arquitectura de agentes con NVIDIA NemoClaw/OpenShell, Eval Loop, diagramas Mermaid flat, stack, stack del hackathon, perfiles técnicos de los 6 héroes en tabs/acordeón, diagramas de conexión por perfil, G-Brain/MCP, Hermes Core (skills, memory, cron, subagents, gateway, MCP, self-improvement), demo funcional del Tesorero, workshop de 90 min paquetizado, instalación, estructura de repositorio y roadmap.
3. **`dashboard/`** — Dashboard de operaciones (Next.js 15 + React 19 + TypeScript + Tailwind CSS). Muestra KPIs, kanban de misiones filtrado por perfil, administrador de cron jobs y auth simple por cookie. Lee y escribe `data/tasks.json` y `data/cron.json`.

Las páginas web usan HTML estático, Tailwind CSS vía CDN y JavaScript vanilla. El dashboard usa Tailwind CSS con la misma paleta: tipografía Space Grotesk y Geist Mono, fondo `#050505`, acento cian `#00D4FF`, sin gradientes ni glows.

## Los 6 héroes

| Héroe | Perfil | Archivo | Pegaso |
|-------|--------|---------|--------|
| Tesorero | Finanzas y Google Sheets | `.finance` | Google Sheets, dashboards, plantillas Excel, parsers de gastos, NVIDIA cuDF, cuOpt |
| Mensajero | Ventas y comunicación / marketing | `.design` | Open Design, redes sociales, SEO/GEO, WordPress/SSH, Google Docs/Slides |
| Cobrador | Pagos, suscripciones y gastos autorizados | `.payments` | Stripe API, payment links, `stripe-link-cli`, `mpp-agent`, `stripe-projects`, webhooks |
| Guardián | Seguridad, sandbox y modelos | `.security` | NVIDIA NemoClaw, OpenShell, Nemotron, OpenAI / Kimi APIs, API keys, permisos |
| Estratega | Administración y operaciones / PM | `.ops` | Calendar, Gmail, tareas, recordatorios, checklists, briefings, cron, subagentes |
| Diplomático | Clientes y proveedores | `.relations` | Gmail, Sheets, CRM ligero, hitos, recordatorios |

## Flujo de trabajo

1. **Hermes pregunta**: ¿qué empresa es? ¿qué necesitas ordenar?
2. **Hermes divide en misiones**: convierte la intención en tareas publicadas en el Partenón.
3. **El héroe toma**: lee su archivo de perfil, consulta G-Brain y empieza a trabajar con el emprendedor.
4. **Entrega en Google Workspace**: el resultado vive en Sheets, Docs, Slides o Calendar para que todos lo vean.

## Stack

- **Frontend páginas**: HTML estático + Tailwind CSS CDN + JS vanilla
- **Agent core**: Hermes Agent (Nous Research) + Python skills + `partenon-core` (router, onboarding, workflow, eval loop)
- **Sandbox / orquestación**: NVIDIA NemoClaw + OpenShell
- **Modelos**: NVIDIA Nemotron 3 Ultra / Super, OpenAI, Kimi Coding
- **Dashboard**: Next.js 15 + React 19 + TypeScript + Tailwind (en `dashboard/`)
- **Documentos**: Python + WeasyPrint (Kami v3)
- **Datos**: Google Workspace (Sheets, Docs, Slides, Drive, Calendar, Gmail); plantillas Excel con openpyxl
- **Pagos**: Stripe API + Stripe Skills (`stripe-link-cli`, `mpp-agent`, `stripe-projects`)
- **Memoria / orquestación**: G-Brain de Garitán vía MCP (FastMCP), Hermes `MEMORY.md`/`USER.md`
- **Mensajería**: Hermes messaging gateway: Telegram, WhatsApp, Slack, Discord, Email y 18 plataformas más
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
- Fase actual: Páginas web enriquecidas con stack del hackathon (Hermes + NVIDIA NemoClaw/OpenShell/Nemotron 3 Ultra + Stripe Skills), auto-mejora, messaging gateway y perfiles técnicos actualizados.
- Perfiles implementados: Tesorero (`.finance`), Mensajero (`.design`), Cobrador (`.payments`), Guardian (`.security`), Estratega (`.ops`), Diplomatico (`.relations`).
- Web verificada: `web/index.html` y `web/developers.html` en desktop (1440px) y mobile (390px). Screenshots actualizadas en `screenshots/`.
- Dashboard verificado: `npm install` y `npm run build` pasan sin errores de TypeScript.
- Demo verificado: `python scripts/demo_tesorero.py` genera Excel + JSON con métricas.
- Próxima tarea: Implementar eval loop funcional en el Tesorero (test cases + judge skill + threshold 0.7), probar Stripe Skills en sandbox y configurar onboard de NVIDIA NemoClaw.

## Instalación rápida

```bash
git clone https://github.com/paolameneses/partenon.git
cd partenon

# Opción A: instalador local
curl -fsSL https://partenon.dev/install.sh | bash

# Opción B: onboard con NVIDIA NemoClaw
curl -fsSL https://www.nvidia.com/nemoclaw.sh | NEMOCLAW_AGENT=hermes bash

# Stripe Skills oficiales
hermes skills install official/payments/stripe-link-cli
hermes skills install official/payments/mpp-agent
hermes skills install official/payments/stripe-projects
```

Luego copia el Google Sheet base, configura las variables de entorno listadas en `.env.example` y define el tipo de empresa en el onboarding.

## Repositorios relacionados

- [Hermes Agent](https://hermes-agent.nousresearch.com/)
- [Hermes Business OS](https://github.com/cuentadeservicio377-cell/hermes-business-os)
- [Open Design](https://github.com/cuentadeservicio377-cell/open-design)

## Memoria del proyecto

Ver [`.kimi-code/memory/`](.kimi-code/memory/)
