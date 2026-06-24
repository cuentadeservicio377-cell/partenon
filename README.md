# Partenon

> Sistema de agentes IA para empresas, presentado como un panteón de héroes al servicio de Hermes. Proyecto para hackathon.

## Qué es

Partenon organiza agentes de IA como un panteón operativo:

- **Hermes** = la empresa.
- **Los héroes** = seis agentes especializados que toman misiones.
- **El Partenón** = el sistema donde comparten herramientas, memoria y conocimiento.
- **G-Brain de Garitán** = el cerebro que conecta todo por MCP.
- **Google Workspace** = la superficie donde trabajan empresa y agentes.

## Las dos páginas

La entrega actual son dos páginas web estáticas que funcionan como manual de marca + espejo técnico:

1. **`web/index.html`** — Página de marketing. Storytelling, arquetipos, los 6 héroes, contador de impacto 10 → 1M, go-to-market e instalación.
2. **`web/developers.html`** — Página técnica. Arquitectura en capas, diagramas, fichas técnicas de agentes, flujos, integraciones, estructura de repositorio y workshop de 90 min.

Ambas usan HTML estático, Tailwind CSS vía CDN y JavaScript vanilla, con tipografía premium (Clash Display, Geist, Instrument Serif) y estética oscura tipo Nous Research.

## Los 6 héroes

| Héroe | Perfil | Archivo | Stack clave |
|-------|--------|---------|---------------|
| Tesorero | Finanzas y Google Sheets | `.finance` | Google Sheets API, dashboards |
| Mensajero | Ventas y comunicación | `.design` | Redes sociales, Open Design, SEO |
| Cobrador | Pagos y suscripciones | Stripe | Stripe API |
| Guardián | Seguridad y modelos | `.security` | Nvidia / OpenAI / Kimi APIs, vault |
| Estratega | Operaciones y PM | Ops | Calendar, Gmail, tasks |
| Diplomático | Clientes y proveedores | CRM | Gmail, Sheets, hitos |

## Stack

- **Frontend páginas**: HTML estático + Tailwind CSS CDN + JS vanilla
- **Agent core**: Hermes Agent (Nous Research) + Python skills
- **Dashboard**: Next.js 15 + React 19 + TypeScript + Tailwind
- **Documentos**: Python + WeasyPrint (Kami v3)
- **Datos**: Google Workspace (Sheets, Docs, Slides, Drive, Calendar, Gmail)
- **Pagos**: Stripe API
- **Memoria / orquestación**: G-Brain de Garitán vía MCP
- **Mensajería**: Telegram (primario) + WhatsApp Business
- **Infraestructura**: Docker / Docker Compose

## Estado

- Iniciado: 2026-06-23
- Fase actual: Páginas web de marketing y documentación técnica completadas y verificadas visualmente.
- Próxima tarea: Construir el repositorio del sistema Partenon basado en Hermes Business OS.

## Instalación rápida

```bash
curl -fsSL https://partenon.dev/install.sh | bash
```

## Repositorios relacionados

- [Hermes Business OS](https://github.com/cuentadeservicio377-cell/hermes-business-os)
- [Open Design](https://github.com/cuentadeservicio377-cell/open-design)

## Memoria del proyecto

Ver [.kimi/memory/](.kimi/memory/)
