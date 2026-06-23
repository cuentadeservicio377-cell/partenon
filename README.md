# Partenon

> Proyecto de Kimi Code — Sistema de agentes IA para empresas, presentado como un panteón de héroes al servicio de Hermes.

## Descripción

Partenon es un ecosistema de agentes IA especializados (los "héroes") que trabajan para una empresa representada como Hermes. Cada héroe tiene una personalidad, herramientas y skills definidas, y toma "misiones" del Partenón para organizar finanzas, comunicación, ventas, cobranza, seguridad, administración y relaciones.

El proyecto se está construyendo para un hackathon. La primera entrega son dos páginas web:

1. **Página de marketing** — storytelling, arquetipos, beneficios, perfiles y plan de crecimiento.
2. **Página técnica** — arquitectura, diagramas, MCPs, integraciones y proceso de workshop.

Después de las páginas se construirá el repositorio del sistema, basado en [Hermes Business OS](https://github.com/cuentadeservicio377-cell/hermes-business-os).

## Stack Técnico

- **Frontend (páginas web)**: HTML estático + Tailwind CSS (CDN) + JavaScript vanilla
- **Agentes / backend**: Hermes Agent (Nous Research) + Hermes Business OS skills
- **Dashboard**: Next.js 15 + React 19 + TypeScript + Tailwind CSS
- **Documentos**: Python + WeasyPrint (Kami v3)
- **Integraciones**: Google Workspace, Stripe, G-Brain, Telegram, WhatsApp, MCPs
- **Infraestructura**: Docker / Docker Compose

## Estado

- Iniciado: 2026-06-23
- Fase actual: Diseño e implementación de las dos páginas web
- Próxima tarea: Crear página de marketing (`web/index.html`)

## Memoria

Ver [.kimi/memory/](.kimi/memory/)

## Repositorios Relacionados

- [Hermes Business OS](https://github.com/cuentadeservicio377-cell/hermes-business-os)
- [OpenWork Paola Meneses](https://github.com/cuentadeservicio377-cell/paola-meneses-openwork)
- [Agente Marketing Kimi](https://github.com/cuentadeservicio377-cell/agente-marketing-kimi)
- [Open Design](https://github.com/cuentadeservicio377-cell/open-design)
