# Partenon

> Sistema operativo de agentes IA para pymes, presentado como un panteón de héroes al servicio de Hermes. Proyecto para el hackatón Nous Research / Nvidia / Stripe.

## Qué es

Partenon organiza agentes de IA como un sistema operativo:

- **Hermes** = la empresa (no un CEO, no un chatbot).
- **Los héroes** = seis agentes especializados que toman misiones.
- **El Partenón** = el workspace compartido donde colaboran.
- **G-Brain de Garitán** = el cerebro que conecta todo por MCP.
- **Google Workspace** = la superficie donde trabajan empresa y agentes.

## Las superficies

La entrega incluye dos páginas web estáticas y un dashboard operativo:

1. **`web/index.html`** — Página de marketing. Introducción de marca, arquetipos, cómo funciona, los 6 héroes con ejemplos concretos (construcción y cafetería), G-Brain, contador de impacto 10 → 1M con múltiples métricas por escala, paper de referencia, go-to-market e instalación.
2. **`web/developers.html`** — Página técnica. Arquitectura de agentes, diagramas Mermaid flat, stack, perfiles técnicos de los 6 héroes, diagramas de conexión por perfil, G-Brain/MCP, workshop de 90 min paquetizado, instalación, integraciones y roadmap.
3. **`dashboard/`** — Dashboard de operaciones (Next.js 15 + React 19 + TypeScript + Tailwind CSS). Muestra KPIs, kanban de misiones filtrado por perfil, administrador de cron jobs y auth simple por cookie. Lee y escribe `data/tasks.json` y `data/cron.json`.

Las páginas web usan HTML estático, Tailwind CSS vía CDN y JavaScript vanilla. El dashboard usa Tailwind CSS con la misma paleta: tipografía Space Grotesk y Geist Mono, fondo `#050505`, acento cian `#00D4FF`, sin gradientes ni glows.

## Los 6 héroes

| Héroe | Perfil | Archivo | Stack clave |
|-------|--------|---------|---------------|
| Tesorero | Finanzas y Google Sheets | `.finance` | Google Sheets, dashboards, costos fijos/variables |
| Mensajero | Ventas y comunicación | `.design` | Redes sociales, Open Design, SEO/GEO, WordPress/SSH |
| Cobrador | Pagos y suscripciones | `.payments` | Stripe API, payment links, webhooks |
| Guardián | Seguridad y modelos | `.security` | Nvidia / OpenAI / Kimi APIs, API keys, permisos |
| Estratega | Operaciones y PM | `.ops` | Calendar, Gmail, tareas, recordatorios |
| Diplomático | Clientes y proveedores | `.relations` | Gmail, Sheets, hitos, recordatorios |

## Stack

- **Frontend páginas**: HTML estático + Tailwind CSS CDN + JS vanilla
- **Agent core**: Hermes Agent (Nous Research) + Python skills
- **Dashboard**: Next.js 15 + React 19 + TypeScript + Tailwind (en `dashboard/`)
- **Documentos**: Python + WeasyPrint (Kami v3)
- **Datos**: Google Workspace (Sheets, Docs, Slides, Drive, Calendar, Gmail)
- **Pagos**: Stripe API
- **Memoria / orquestación**: G-Brain de Garitán vía MCP
- **Mensajería**: Telegram (primario) + WhatsApp Business
- **Infraestructura**: Docker / Docker Compose

## Estado

- Iniciado: 2026-06-23
- Fase actual: Construccion del repositorio del sistema Partenon basado en Hermes Business OS.
- Perfiles implementados: Tesorero (`.finance`), Mensajero (`.design`), Cobrador (`.payments`), Guardian (`.security`), Estratega (`.ops`), Diplomatico (`.relations`).
- Web verificada: `web/index.html` y `web/developers.html` en desktop (1440px) y mobile (390px).
- Dashboard verificado: `npm install` y `npm run build` pasan sin errores de TypeScript.
- Próxima tarea: Integrar Google Workspace, Stripe y G-Brain con los perfiles y validar flujos end-to-end.

## Instalación rápida

```bash
git clone https://github.com/paolameneses/partenon.git
cd partenon
```

Luego copia el Google Sheet base, sube `apps-script/Hermes.gs` y configura las variables de entorno listadas en `developers.html#install`.

### Dashboard

```bash
cd dashboard
npm install
npm run dev
```

Abre http://localhost:3000 y entra con usuario `admin` y contrasena `partenon` (configurable via `DASHBOARD_APP_USERNAME` y `DASHBOARD_APP_PASSWORD`). Lee y escribe `data/tasks.json` y `data/cron.json` relativos a la raiz del proyecto.

## Repositorios relacionados

- [Hermes Agent](https://hermes-agent.nousresearch.com/)
- [Open Design](https://github.com/NousResearch/open-design)

## Memoria del proyecto

Ver [.kimi/memory/](.kimi/memory/)
