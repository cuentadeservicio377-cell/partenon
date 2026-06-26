# Memoria del Proyecto: Partenon

> Última sesión: 2026-06-26

## Contexto Actual

- **Proyecto**: Partenon
- **Iniciado**: 2026-06-23
- **Estado**: Repositorio público en GitHub creado y listo para hackathon. Tres páginas web estáticas en `web/` desplegadas en `https://hermespartenon.online/`. Siete perfiles de Hermes en `hermes/profiles/` (Tesorero, Mensajero, Cobrador, Guardian, Estratega, Diplomático, Brain). Documentación completa en `docs/` (for-founders, for-developers, architecture). Scripts de instalación: `install.sh` y `scripts/setup_hermes.py`. Próximo: probar Stripe Skills en sandbox, configurar onboard de NVIDIA NemoClaw/OpenShell e implementar eval loop funcional.

## Braindump

### 1. ¿Qué es este proyecto?

Partenon es un sistema de agentes IA organizado como un panteón de héroes que trabajan para un "dios" llamado Hermes. Hermes representa la empresa/emprendedor. Los héroes son agentes especializados que ejecutan misiones (tareas) para mejorar, organizar y hacer crecer la empresa.

La narrativa de marca usa arquetipos (no la mitología de forma cursi) para dar personalidad a cada perfil. El tono debe ser de storytelling de marketing, no forzado ni geek.

### 2. ¿Quién lo usa?

- **Emprendedores y empresas pequeñas** que necesitan organizar operaciones, finanzas, ventas, comunicación, cobranza, seguridad y administración.
- **Hackathon judges** de Nous Research, Nvidia y Stripe.
- **Desarrolladores** que quieran entender la arquitectura e instalar el sistema.
- **Universidades, aceleradoras, cámaras de comercio, coworkings y organizaciones empresariales** (BNI, Way Pío, Rotary, etc.) para workshops y eventos.

### 3. ¿Qué stack tecnológico prefieres?

**Confirmado para las páginas web:**
- **Páginas web**: HTML estático + Tailwind CSS + JavaScript vanilla. Alojado en GitHub Pages.
- **Estética**: Basada en la app React `Kimi_Agent_10 Storytelling Web Sites/app`: mármol blanco `#F7F5F0`, pergamino `#EDE8DF`, deep-stone `#2A2A2E`, midnight `#1A1A1E`, tipografías Cinzel + Inter + JetBrains Mono.

**Stack del sistema (basado en repositorios analizados):**
- **Agent Core**: Hermes Agent (Nous Research) — Python
- **Sandbox / Orchestration**: NVIDIA NemoClaw + OpenShell
- **Models**: NVIDIA Nemotron 3 Ultra / Super, OpenAI, Kimi / Moonshot
- **Skills nativas**: Hermes Business OS (HBOS) — 6 skills base
- **Payments**: Stripe API + Stripe Skills (`stripe-link-cli`, `mpp-agent`, `stripe-projects`)
- **Dashboard**: Next.js 15 + React 19 + TypeScript + Tailwind CSS
- **Document Engine**: Python + WeasyPrint (Kami v3)
- **Data**: Google Sheets (master data) + JSON local
- **Communication**: Hermes messaging gateway (Telegram, WhatsApp, Slack, Discord, Email, LINE, etc.)
- **Integraciones**: Google Workspace, Stripe, G-Brain vía MCP
- **Infraestructura**: Docker / Docker Compose, opcional AWS EC2

### 4. ¿Hay deadline o prioridad?

- **Prioridad 1**: Construir las tres páginas web para el hackathon (marketing, héroes, técnicos).
- **Prioridad 2**: Definir arquitectura técnica y crear el repositorio del sistema.
- **Deadline**: hackathon (por confirmar fecha exacta).

### 5. ¿Hay algo ya construido?

- Estructura inicial del proyecto Partenon creada por braindump-init.
- **Hermes Business OS (HBOS)** ya existe con 6 skills base:
  - `hermes-business-core` — config, routing, Google Workspace, onboarding
  - `hermes-ventas` — CRM, cotizaciones, pipeline
  - `hermes-operaciones` — proyectos, tareas, logística
  - `hermes-finanzas` — presupuestos, pagos, reportes
  - `hermes-rrhh` — equipos, asistencia, nómina
  - `hermes-documentos` — generación de PDFs/Docs/Slides
- **OpenWork Paola Meneses** es una adaptación operativa con OpenWork + OpenCode + React + FastAPI + Google Workspace + AWS.
- **Agente Marketing Kimi** tiene Campaign Manager, subagentes paralelos, GBrain, Control Center en Sheets y entregables en Drive.
- **Open Design** es una herramienta de diseño con agentes (31 skills, 129 design systems). Posible referencia visual.
- **Hermes Bible** (hermesbible.com) es documentación no oficial de Hermes Agent.
- **Research Paper** de HBOS ya escrito y publicado en el repo.

### 6. ¿Restricciones importantes?

- Debe funcionar con Google Workspace gratuito si es posible.
- Debe sentirse como un subproducto de Nous Research / Nous Research (estética a copiar).
- No debe sentirse cursi ni forzado el tema griego; usar arquetipos de marketing.
- Debe haber tres páginas web claramente diferenciadas: marketing (index.html), héroes (heroes.html) y técnica (developers.html).
- Los empresarios deben poder trabajar en algo que conozcan (Google Workspace), no solo archivos MD en un workspace del agente.
- Primero páginas, luego sistema.

### 7. ¿Qué haría que sea un éxito?

- Tener tres páginas web impactantes para el hackathon.
- Contador de impacto: 10 → 100 → 1,000 → 10,000 → 100,000 → 1,000,000 personas/empresas ayudadas.
- Generar webinars quincenales de instalación.
- Eventos con universidades, aceleradoras, cámaras de comercio, coworkings.
- Que Hermes sea el agente personalizado de aceleradoras, respaldado por Stripe, Nvidia y Nous Research.
- Que 10 empresas pilotos mejoren ingresos, calidad, orden financiero y ahorren horas.

## Concepto de Marca

- **Hermes** = la empresa (no solo el CEO). Es el dios que necesita ayuda.
- **El Partenón** = el conjunto: Hermes + sus héroes.
- **Héroes** = agentes especializados que toman misiones del Partenón.
- **Herramientas de los héroes** = skills, MCPs, APIs y plataformas open source.

## Perfiles de Héroes (agentes)

Los perfiles mapean directamente a skills existentes o propuestas de HBOS:

1. **Héroe de Finanzas / Sheets** (`hermes-finanzas`)
   - Experto en Google Sheets, dashboards, costos fijos/variables, análisis financiero.
   - Crea archivo `.finance` por empresa.
   - Trabaja en conjunto con el emprendedor para acomodar números.

2. **Héroe de Comunicación / Ventas / Marketing** (`hermes-ventas` + marketing)
   - Experto en redes sociales, marca, storytelling, growth.
   - Acceso a archivo `.design` de la empresa.
   - Crea campañas, calendarios de contenido, SEO, presentaciones, mails.
   - Se conecta con Sheets para presupuestos y datos.

3. **Héroe de Cobranza / Stripe**
   - Experto en Stripe y pagos.
   - Se conecta a tiendas en línea, servicios y productos físicos.
   - Maneja suscripciones, pagos, recordatorios.

4. **Héroe de Seguridad / Modelos**
   - Administra API keys, modelos de IA, cuentas (Nvidia, OpenAI, Kimi Code, etc.).
   - Gestiona permisos, seguridad y acceso a servicios.

5. **Héroe de Administración / Operaciones** (`hermes-operaciones`)
   - Gerente operativo, project manager.
   - Acceso a Google Calendar, correo, recordatorios, detalles de clientes/operaciones.
   - Acomoda recursos y ayuda a coordinar a los demás héroes.

6. **Héroe de Relaciones (Clientes y Proveedores)**
   - Gestiona relaciones externas.
   - Coordina entre cliente y operaciones para llegar a puntos medios.
   - Recordatorios, hitos, información pendiente.

7. **Héroe de Documentos** (`hermes-documentos`)
   - Genera contratos, cotizaciones, propuestas, presentaciones.
   - Motor Kami v3 (WeasyPrint) + Google Docs/Slides.

## Integraciones Clave

- Google Workspace (Sheets, Drive, Docs, Slides, Calendar, Gmail)
- Stripe + Stripe Skills (`stripe-link-cli`, `mpp-agent`, `stripe-projects`)
- NVIDIA NemoClaw + OpenShell + Nemotron 3 Ultra / Super
- G-Brain de Garry Tan (cerebro central vía MCP)
- Hermes Agent (Nous Research)
- MCPs para cada héroe
- Hermes messaging gateway (Telegram, WhatsApp, Slack, Discord, Email, LINE, etc.)
- Nous Research / NVIDIA / Stripe (respaldos y jurado)

## Estructura de Archivos por Empresa

- `.finance` → datos financieros y dashboards
- `.design` → identidad, marca y estrategia de comunicación
- `.payments` → configuración de Stripe y pagos
- `.security` → API keys, modelos y permisos
- `.ops` → operaciones, calendario, tareas
- `.relations` → clientes, proveedores, hitos
- `client.yaml` → configuración de la empresa
- Posibles archivos adicionales según necesidad de cada héroe

## Estrategia de Go-to-Market

- Página web con contador de impacto (10, 100, 1K, 10K, 100K, 1M).
- Webinars quincenales de instalación.
- Eventos en universidades y aceleradoras.
- Workshops en cámaras de comercio, BNI, Rotary, coworkings.
- Alianza con aceleradoras para que Hermes sea su agente personalizado.

## Repositorios Analizados

| Repo | Qué es | Reutilizable para Partenon |
|------|--------|---------------------------|
| hermes-business-os | Distribución de skills de negocio para Hermes Agent | Base del sistema, skills, arquitectura, paper |
| paola-meneses-openwork | OpenWork adaptado para eventos (Paola Meneses) | Patrones de Google Workspace, templates, MCPs |
| openwork-paola | Versión más simple de lo anterior | Mismo caso |
| agente-marketing-kimi | Sistema de marketing con Campaign Manager | Patrones de subagentes, GBrain, Control Center |
| open-design / open-design-migration | Herramienta de diseño con agentes | Design systems, referencia visual, skills de landing |
| hermesbible.com | Docs no oficiales de Hermes Agent | Contexto de Hermes Agent |

## Decisiones Arquitectónicas

- Las tres páginas web se construyen primero, antes del sistema.
- `web/index.html` (marketing) explica el concepto, beneficios, perfiles y go-to-market.
- `web/heroes.html` (héroes) detalla los 7 perfiles, sus capacidades, tools, conexiones y workflow de colaboración.
- `web/developers.html` (técnica) explica la arquitectura, MCPs, diagramas y proceso de workshop.
- El sistema se construirá basado en las páginas.
- Google Workspace como superficie de trabajo compartida con el empresario.
- HBOS como base técnica existente; Partenon es la capa de presentación y extensión de perfiles.
- Repositorio público en GitHub: `https://github.com/cuentadeservicio377-cell/partenon`.
- Perfil `partenon-brain` agregado como séptimo héroe para memoria colectiva vía G-Brain.
- `.env.example` global con placeholders seguros para evitar secret scanning de GitHub.
- `install.sh` y `scripts/setup_hermes.py` para instalación automatizada en entornos con Hermes Agent.
- Documentación del repo desacoplada de las páginas web: `docs/for-founders.md`, `docs/for-developers.md`, `docs/architecture.md`.
- Stack del hackathon explícito en las tres páginas: Hermes Agent + NVIDIA NemoClaw/OpenShell/Nemotron 3 Ultra + Stripe Skills.
- Estética Nous Research / manual técnico: fondo `#050505`, acento cian `#00D4FF`, tipografía monospaced en hero, sin emojis ni emdashes.
- Copy anti-AI-slop: verbos concretos, claim + proof, sin intensificadores ni frases de transición dramáticas.

## APIs / Integraciones

- Google Workspace APIs
- Stripe API + Stripe Skills
- NVIDIA NemoClaw / OpenShell / Nemotron
- G-Brain (MCP)
- Hermes Agent APIs
- MCPs de cada herramienta/skill

## Gotchas Conocidos

- El tono mitológico debe ser sutil; evitar cursilería.
- Las páginas deben impresionar a jurado técnico (Nvidia, Stripe, Nous Research).
- Debe quedar claro que Hermes = empresa, no solo CEO.
- El sistema debe entregar valor en herramientas que el empresario ya conoce (Google Workspace).
- open-design es muy grande (331MB); se usará como referencia, no como dependencia.
- Algunos repos privados requieren gh CLI para acceder.

## Links Útiles

- Hermes Bible: https://www.hermesbible.com/
- Hermes Business OS: https://github.com/cuentadeservicio377-cell/hermes-business-os
- Research Paper (EN): https://github.com/cuentadeservicio377-cell/hermes-business-os/blob/main/docs/RESEARCH-PAPER.en.md
- Open Design: https://github.com/cuentadeservicio377-cell/open-design
- OpenWork Paola: https://github.com/cuentadeservicio377-cell/paola-meneses-openwork
- Agente Marketing Kimi: https://github.com/cuentadeservicio377-cell/agente-marketing-kimi
