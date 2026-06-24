# SPEC — Partenon Website

## Visión general

Dos páginas web estáticas que sirven como entrada al hackatón de Nous Research, Nvidia y Stripe:

1. **`web/index.html`** — Página de marketing / manual de marca. Storytelling, arquetipos, héroes, impacto, go-to-market.
2. **`web/developers.html`** — Página técnica / espejo técnico. Arquitectura, diagramas, fichas técnicas, workshop.

Estética: Nous Research / Hermes Agent. Oscuro plano, acentos púrpura/teal/coral, diagramas flat, sin glows ni gradientes.

---

## Página 1: Marketing (`web/index.html`)

### 1. Nav
- Logo "Partenon" a la izquierda.
- Links: Historia, Héroes, Impacto, Crecimiento.
- CTA derecho: "Documentación técnica →" a `developers.html`.
- Estilo: nav flotante tipo píldora, fondo surface/80, borde fino.

### 2. Hero / Talk about
- Eyebrow: "Hermes Business OS · Partenon".
- H1: "Hermes es tu empresa. Sus héroes, tu ventaja."
- Subtítulo: Partenon organiza agentes de IA como un panteón operativo. Cada héroe tiene una personalidad, un set de herramientas y una misión.
- CTAs: "Conoce a los héroes" (primary) + "Ver arquitectura" (secondary).
- Pequeño "talk about" debajo o al lado: "Esta es la historia de cómo una empresa latinoamericana deja de pelear con el software y empieza a operar con un panteón de agentes."

### 3. El problema
- Título: "En América Latina, las pymes no necesitan más software."
- Texto: necesitan un socio que hable su idioma, use sus herramientas y entienda que el dueño hace todo al mismo tiempo.
- Datos: 99.5% de empresas son pymes, generan 60% del empleo, 25% del PIB.
- La brecha es de diseño, no de tecnología.

### 4. El mito / arquetipo
- Título: "No es mitología de salón. Son arquetipos de empresa."
- Narrativa:
  - Partenón = templo donde viven los héroes.
  - Los héroes hacen encargos a los dioses.
  - Hermes es un dios.
  - Los héroes de Partenon son los héroes de Hermes.
  - Cada héroe tiene una personalidad.
  - Hermes + sus héroes = Partenon.
  - Hermes es la empresa (no el CEO).
  - Hermes necesita ayuda, no puede solo.
  - Tiene su poderoso campo de operaciones.
- Explicar en tono branding, no cursi, usando arquetipos de marketing.
- Tres tarjetas: Hermes / El Partenón / Los Héroes.

### 5. Cómo funciona
- Título: "Misiones, no menús."
- 3 pasos:
  1. Hermes publica una tarea.
  2. Un héroe la toma.
  3. Entrega en Google Workspace.

### 6. Herramientas de héroe = Pegaso
- Título: "Como Hércules tenía su Pegaso."
- Cada héroe tiene herramientas open source y habilidades.
- Mostrar ejemplos: Google Sheets, Open Design, Stripe, Nvidia APIs, Calendar, Gmail.

### 7. Los 6 héroes (storytelling profundo)

#### Tesorero — `.finance`
- Experto en Google Sheets, dashboards, acomodar información.
- Hermes le pregunta: "¿Qué empresa es? ¿Qué temas usas?"
- Ejemplo construcción: materiales, ganancia, costo, costos variables, costos fijos.
- Ejemplo cafetería: pauta de marketing, impuestos, renta, insumos, empleados.
- Divide la empresa en subtareas/misiones.
- Crea archivo `.finance` con instrucciones financieras.
- Está en misión conjunta con el emprendedor y Hermes.
- Tools: Google Sheets API, Google Drive API, parser de costos.

#### Mensajero — `.design`
- Ventas + comunicación.
- Experto en comunicar y usar herramientas de comunicación.
- Acceso a redes sociales, memoria y marca.
- Archivo `.design` de la empresa.
- Open Design como herramienta.
- Preguntas al emprendedor: qué vendes, cómo ayudas, por qué, cómo solucionas algo de verdad.
- Misiones secundarias de investigación con el emprendedor.
- Construye identidad y estrategia de comunicación, growth, SEO, GEO.
- Campañas, calendarios de contenido orgánico.
- Pide información: sitio web, accesos, WordPress, SSH, skills de WordPress.
- Presentaciones, cartas, mails.
- Se conecta con Google Sheets del Tesorero.
- Tools: Google Docs/Slides, redes sociales, Open Design, `.design`.

#### Cobrador — Stripe
- Lleva cuentas, recibe pagos por Stripe.
- Skills de Stripe completos.
- Se conecta a tienda en línea, servicios, productos físicos.
- Tools: Stripe API, webhooks, Google Sheets.

#### Guardián — `.security`
- Seguridad + Nvidia.
- Administra API keys, modelos, cuentas, permisos.
- Pregunta qué modelos tiene la empresa: API key de Nvidia, cuenta pagada de Twitter/X, OpenAI, Kimi Code, etc.
- Tools: Nvidia APIs, OpenAI, Kimi Code, vault local, permisos por perfil.

#### Estratega — ops
- Administración / project management.
- Acomoda recursos, ayuda a los demás.
- Gerente operativo.
- Google Calendar, Gmail, recordatorios, detalles.
- Tools: Calendar API, Gmail API, task manager.

#### Diplomático — relations
- Relaciones con clientes y proveedores.
- Recordatorios, hitos, coordinación de expectativas.
- Separado del Estratega: uno interno, uno externo.
- Analogía del caballero de Géminis (dos caras, un acuerdo).
- Tools: Gmail, Calendar, Sheets CRM.

### 8. G-Brain de Garitán
- Cerebro conectado por MCP.
- Memoria persistente, instrucciones de perfil, audit log, conocimiento compartido.
- Todos los agentes se conectan con Hermes a través de G-Brain.

### 9. Impacto 10 → 1M
- Contador animado: 10, 100, 1K, 10K, 100K, 1M Hermes.
- Cada milestone con varios datos de impacto:
  - Ingreso mejorado X%.
  - Calidad mejorada.
  - Números en orden.
  - Horas ahorradas.
- Marcador de cuánto ayuda el agente a pymes.

### 10. Paper / article
- Bloque que referencia el paper del usuario.
- Si no se tiene, usar el de Hermes Business OS: "Closing the Gap: Open Artificial Intelligence as Digital Inclusion Infrastructure for Latin American SMEs".

### 11. Go-to-market
- Título: "Cómo llegamos a 1 millón."
- Webinars quincenales: cada 15 días, grupo pre-registrado, instalar cada Hermes.
- Universidades: aceleradores, departamentos de innovación, estudiantes de cualquier carrera, actividad extracurricular, auditorios. Investigar capacidad de auditorios.
- Organizaciones empresariales: BNI, Wayra, cámaras de comercio, Rotarios.
- Coworkings: workshops específicos, alianzas.
- Aceleradoras: Hermes como agente personalizado, respaldado por Stripe, Nvidia, Nous Research.
- CTA a repositorio.

### 12. Fichas de héroes (segunda vuelta)
- Tarjetas detalladas por héroe.
- Qué puede hacer, cómo lo hace, conexiones, MCPs, herramientas, skills, personalidad, perfil.
- Conexión a Drive, Sheets, etc.

### 13. Google Workspace + estructura de repositorio
- Todo ligado a Google Workspace gratuito.
- Estructura de archivos para que los agentes sepan dónde están.
- CTA de instalación: comando `curl`.

### 14. Footer
- Links a historia, héroes, técnico.
- "Basado en Hermes Business OS · Open source".

---

## Página 2: Técnica (`web/developers.html`)

### 1. Nav
- Logo Partenon, links: Arquitectura, Agentes, Flujo, Workshop.
- CTA "← Marketing" a `index.html`.

### 2. Hero
- Título: "Arquitectura de un panteón operativo."
- Subtítulo: Partenon extiende Hermes Business OS con seis perfiles de agentes, conectados por MCP y unificados bajo G-Brain.
- CTAs: "Comando de instalación" + "Repositorio base".

### 3. Arquitectura en capas
- Diagrama Mermaid estilo Nous:
  - UI: Telegram, WhatsApp, Next.js Dashboard.
  - Hermes Agent Core: Context Router, Memory System, Skill Engine.
  - Partenon Profiles: 6 héroes.
  - G-Brain de Garitán (MCP Server).
  - Datos y Pagos: Google Workspace + Stripe.
- Explicación de cada capa.

### 4. Stack
- Agent Core, Dashboard, Documentos, Datos, Mensajería, Pagos, Memoria, Deploy.

### 5. Fichas técnicas de los 6 héroes
- Inputs, outputs, MCPs/tools, dependencias.
- Código de skill real (`hermes-finanzas`, `hermes-ventas`, `stripe-skill`, etc.).

### 6. Diagramas de flujo
- De una idea a un spreadsheet (Tesorero).
- De campaña a pago (Mensajero + Cobrador).
- Onboarding al primer workshop.

### 7. Integraciones
- Google Workspace, Stripe, G-Brain, Telegram/WhatsApp.
- Cómo se conecta cada una.

### 8. Estructura de repositorio
- Árbol completo con perfiles, skills, memory, workspace, web, scripts.

### 9. Workshop técnico de 90 min
- Paquete preparado.
- Pre-instalación: comando, Google Workspace, Docker, API key.
- Onboarding en vivo: `client.yaml`, Telegram/WhatsApp, health check.
- Primera misión: cada uno publica una misión real.
- Requisitos previos.

### 10. Instalación
- Comandos paso a paso.

### 11. Footer
- Links a marketing, arquitectura, agentes.

---

## Notas de implementación

- Usar HTML estático + Tailwind CSS CDN + JS vanilla.
- Tipografía: Clash Display, Geist, JetBrains Mono.
- Colores Nous: púrpura, teal, coral, gris.
- Diagramas Mermaid con tema `base` y colores personalizados.
- Animaciones reveal con IntersectionObserver.
- Mobile-first, colapsar a 1 columna bajo 768px.
