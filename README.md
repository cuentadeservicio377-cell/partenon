# Partenon

> Sistema operativo de agentes IA para pymes, presentado como un panteón de héroes al servicio de Hermes. Proyecto para el hackatón Nous Research / Nvidia / Stripe.

## Qué es

Partenon organiza agentes de IA como un sistema operativo:

- **Hermes** = la empresa (no un CEO, no un chatbot).
- **Los héroes** = seis agentes especializados que toman misiones.
- **El Partenón** = el workspace compartido donde colaboran.
- **G-Brain de Garitán** = el cerebro que conecta todo por MCP.
- **Google Workspace** = la superficie donde trabajan empresa y agentes.

## Las dos páginas

La entrega son dos páginas web estáticas que funcionan como manual de marketing + espejo técnico:

1. **`web/index.html`** — Página de marketing. Introducción de marca, arquetipos, cómo funciona, los 6 héroes con ejemplos concretos (construcción y cafetería), G-Brain, contador de impacto 10 → 1M con múltiples métricas por escala, paper de referencia, go-to-market e instalación.
2. **`web/developers.html`** — Página técnica. Arquitectura de agentes, diagramas Mermaid flat, stack, perfiles técnicos de los 6 héroes, diagramas de conexión por perfil, G-Brain/MCP, workshop de 90 min paquetizado, instalación, integraciones y roadmap.

Ambas usan HTML estático, Tailwind CSS vía CDN y JavaScript vanilla, con tipografía Space Grotesk, Geist y JetBrains Mono, iconos Material Symbols Sharp, y estética oscura plana inspirada en Nous Research / Hermes Agent (fondo `#050505`, acento cian `#00D4FF`, sin gradientes ni glows).

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
- **Dashboard futuro**: Next.js 15 + React 19 + TypeScript + Tailwind
- **Documentos**: Python + WeasyPrint (Kami v3)
- **Datos**: Google Workspace (Sheets, Docs, Slides, Drive, Calendar, Gmail)
- **Pagos**: Stripe API
- **Memoria / orquestación**: G-Brain de Garitán vía MCP
- **Mensajería**: Telegram (primario) + WhatsApp Business
- **Infraestructura**: Docker / Docker Compose

## Estado

- Iniciado: 2026-06-23
- Fase actual: Reescritura de `web/index.html` y `web/developers.html` con estética Nous-style / anti-slop: fondo OLED `#050505`, tipografía monospaced técnica, nav flotante, doble-bisel en cards, acento cian `#00D4FF`, layouts asimétricos/bento y copy sin emdashes ni intensificadores. Verificado en desktop (1440px) y mobile (390px).
- Próxima tarea: Construir el repositorio del sistema Partenon basado en Hermes Business OS.

## Instalación rápida

```bash
git clone https://github.com/paolameneses/partenon.git
cd partenon
```

Luego copia el Google Sheet base, sube `apps-script/Hermes.gs` y configura las variables de entorno listadas en `developers.html#install`.

## Repositorios relacionados

- [Hermes Agent](https://hermes-agent.nousresearch.com/)
- [Open Design](https://github.com/NousResearch/open-design)

## Memoria del proyecto

Ver [.kimi/memory/](.kimi/memory/)
