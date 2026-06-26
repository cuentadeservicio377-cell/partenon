# Partenon

> Sistema operativo de agentes IA para pymes, presentado como un panteón de héroes al servicio de Hermes. Proyecto para el hackatón Nous Research / Nvidia / Stripe.

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

1. **`web/index.html`** — Página de marketing. Introducción de marca, narrativa de arquetipos, Hermes como empresa, los 6 héroes con personalidad y Pegaso, ejemplos concretos (construcción y cafetería), G-Brain, contador de impacto 10 → 1M, carta de intención de Pablo Meneses, go-to-market e instalación.
2. **`web/developers.html`** — Página técnica. Arquitectura de agentes, diagramas Mermaid flat, stack, perfiles técnicos de los 6 héroes con Pegaso/MCP/I/O, diagramas de conexión por perfil, G-Brain/MCP, workshop de 90 min paquetizado, instalación, estructura de repositorio y roadmap.
3. **`dashboard/`** — Dashboard de operaciones (Next.js 15 + React 19 + TypeScript + Tailwind CSS). Muestra KPIs, kanban de misiones filtrado por perfil, administrador de cron jobs y auth simple por cookie. Lee y escribe `data/tasks.json` y `data/cron.json`.

Las páginas web usan HTML estático, Tailwind CSS vía CDN y JavaScript vanilla. El dashboard usa Tailwind CSS con la misma paleta: tipografía Space Grotesk y Geist Mono, fondo `#050505`, acento cian `#00D4FF`, sin gradientes ni glows.

## Los 6 héroes

| Héroe | Perfil | Archivo | Pegaso |
|-------|--------|---------|--------|
| Tesorero | Finanzas y Google Sheets | `.finance` | Google Sheets, dashboards, plantillas Excel, parsers de gastos |
| Mensajero | Ventas y comunicación / marketing | `.design` | Open Design, redes sociales, SEO/GEO, WordPress/SSH, Google Docs/Slides |
| Cobrador | Pagos y suscripciones | `.payments` | Stripe API, payment links, webhooks |
| Guardián | Seguridad y modelos | `.security` | Nvidia / OpenAI / Kimi APIs, API keys, permisos |
| Estratega | Administración y operaciones / PM | `.ops` | Calendar, Gmail, tareas, recordatorios, checklists, briefings |
| Diplomático | Clientes y proveedores | `.relations` | Gmail, Sheets, CRM ligero, hitos, recordatorios |

## Flujo de trabajo

1. **Hermes pregunta**: ¿qué empresa es? ¿qué necesitas ordenar?
2. **Hermes divide en misiones**: convierte la intención en tareas publicadas en el Partenón.
3. **El héroe toma**: lee su archivo de perfil, consulta G-Brain y empieza a trabajar con el emprendedor.
4. **Entrega en Google Workspace**: el resultado vive en Sheets, Docs, Slides o Calendar para que todos lo vean.

## Stack

- **Frontend páginas**: HTML estático + Tailwind CSS CDN + JS vanilla
- **Agent core**: Hermes Agent (Nous Research) + Python skills + `partenon-core` (router, onboarding, workflow)
- **Dashboard**: Next.js 15 + React 19 + TypeScript + Tailwind (en `dashboard/`)
- **Documentos**: Python + WeasyPrint (Kami v3)
- **Datos**: Google Workspace (Sheets, Docs, Slides, Drive, Calendar, Gmail); plantillas Excel con openpyxl
- **Pagos**: Stripe API
- **Memoria / orquestación**: G-Brain de Garitán vía MCP (FastMCP)
- **Mensajería**: Telegram (primario) + WhatsApp Business
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
- Fase actual: Páginas web reconstruidas como especificación maestra. Repositorio en alineación.
- Perfiles implementados: Tesorero (`.finance`), Mensajero (`.design`), Cobrador (`.payments`), Guardian (`.security`), Estratega (`.ops`), Diplomatico (`.relations`).
- Web verificada: `web/index.html` y `web/developers.html` en desktop (1440px) y mobile (390px).
- Dashboard verificado: `npm install` y `npm run build` pasan sin errores de TypeScript.
- Demo verificado: `python scripts/demo_tesorero.py` genera Excel + JSON con métricas.
- Próxima tarea: Integrar Google Workspace, Stripe y G-Brain con credenciales reales y validar flujos end-to-end.

## Instalación rápida

```bash
git clone https://github.com/paolameneses/partenon.git
cd partenon

curl -fsSL https://partenon.dev/install.sh | bash
```

Luego copia el Google Sheet base, configura las variables de entorno listadas en `.env.example` y define el tipo de empresa en el onboarding.

## Repositorios relacionados

- [Hermes Agent](https://hermes-agent.nousresearch.com/)
- [Hermes Business OS](https://github.com/cuentadeservicio377-cell/hermes-business-os)
- [Open Design](https://github.com/cuentadeservicio377-cell/open-design)

## Memoria del proyecto

Ver [`.kimi-code/memory/`](.kimi-code/memory/)
