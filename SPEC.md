# SPEC — Partenon Website Rebuild

## Checklist del transcrip

### Página de marketing (`web/index.html`)

- [x] Talk about / introducción de marca al inicio.
- [x] Explicar que son dos páginas y que sirven como manual de marketing.
- [x] Narrativa filosófica: Partenón = donde están los héroes; héroes hacen encargos a los dioses; Hermes = dios; Partenón = unión de dios + héroes.
- [x] Explicado como branding/arquetipos de marketing, sin cursilería griega.
- [x] Hermes = la empresa (no CEO). Necesita ayuda. Tiene un canvas poderoso.
- [x] Hermes publica tareas; héroes las toman del Partenón.
- [x] Herramientas de héroe = Pegaso: open source + habilidades.
- [x] **Tesorero**:
  - [x] Experto en Google Sheets, dashboards, acomodar información.
  - [x] Ejemplo empresa de construcción: materiales, ganancia, costo, costos variables/fijos.
  - [x] Ejemplo cafetería: pauta marketing, impuestos, renta, insumos, empleados.
  - [x] Divide a Hermes en subtareas/misiones.
  - [x] Misión conjunta con emprendedor y Hermes.
  - [x] Archivo `.finance`.
- [x] **Mensajero**:
  - [x] Ventas + comunicación.
  - [x] Redes sociales, memoria y marca.
  - [x] Archivo `.design`.
  - [x] Open Design.
  - [x] Preguntas de investigación: ¿qué empresa?, ¿qué vendes?, ¿qué ayudas?, ¿por qué?, ¿cómo solucionas?, ¿cómo ayuda tu proyecto?
  - [x] Misiones secundarias con el emprendedor.
  - [x] Campañas, calendario orgánico, SEO, GEO.
  - [x] WordPress / SSH / skills de WordPress.
  - [x] Presentaciones, cartas, mails.
  - [x] Se conecta a Google Sheets del Tesorero.
- [x] **Cobrador**:
  - [x] Stripe, payment links, suscripciones.
  - [x] Tienda online, servicios, productos físicos.
- [x] **Guardián**:
  - [x] Seguridad + Nvidia.
  - [x] Administra modelos, API keys, cuentas (Twitter/X, OpenAI, Kimi Coding, etc.).
  - [x] Archivo `.security`.
- [x] **Estratega**:
  - [x] Administración / gerente operativo / project management.
  - [x] Google Calendar, Gmail, recordatorios, detalles de clientes/operaciones.
- [x] **Diplomático**:
  - [x] Relaciones con clientes y proveedores.
  - [x] Analogía del caballero de Géminis (dos lados, punto medio).
  - [x] Hitos, recordatorios, coordinación con Estratega.
- [x] **G-Brain de Garitán**:
  - [x] Cerebro conectado por MCP.
  - [x] Todos los agentes conectados a Hermes.
- [x] **Contador 10 → 1M**:
  - [x] Números progresivos y coherentes.
  - [x] Múltiples métricas por escala (ingreso, calidad, números en orden, horas ahorradas, trabajos creados).
- [x] **Paper/article de referencia** — placeholder: Hermes Business OS.
- [x] **Go-to-market**:
  - [x] Webinars quincenales con pre-registrados.
  - [x] Universidades: aceleradores, departamentos de innovación, estudiantes de negocios/cualquier carrera, actividad extracurricular en auditorios (con datos de capacidad).
  - [x] Organizaciones empresariales: BNI, Way/Pio, cámaras de comercio, Rotary.
  - [x] Coworkings: workshops específicos y alianzas.
  - [x] Aceleradoras: Hermes como agente personalizado respaldado por Stripe, Nvidia, Nous Research.
- [x] **Repositorio / instalación**:
  - [x] Comando "instala Hermes" (`curl -fsSL ... | bash`).
  - [x] Google Workspace gratuito como superficie común.
  - [x] Estructura de repositorio.
- [x] **Fichas de héroes**:
  - [x] Qué hace, cómo lo hace, conexiones, MSP, herramientas, skills, Drive.

### Página técnica (`web/developers.html`)

- [x] Espejo exacto de marketing pero técnico.
- [x] Arquitectura completa con diagramas de flujo (Mermaid).
- [x] Especificaciones técnicas por héroe:
  - [x] Framework, skills, herramientas, MSP, personalidad, profile.
  - [x] Cómo se conecta, según documentación, interconexiones.
- [x] Diagramas punto a punto por héroe.
- [x] G-Brain/MCP técnico.
- [x] Stack y estructura de repositorio.
- [x] Workshop técnico paquetizado de 90 min:
  - [x] Pre-instalación con comando.
  - [x] Revisión inicial.
  - [x] Onboarding técnico.
  - [x] Explicación gráfica del proceso.

### Diseño

- [x] Rediseño aprobado: Dark Premium Cyberpunk.
- [x] Fondo oscuro no puro: `#0A0A0A` y `#0C0C0F`, con texturas de mesh/grain sutiles.
- [x] Acento único quirúrgico cian `#00E0FF` / magenta `#FF2A6D` / ámbar `#FFB800`, sin gradientes masivos ni glows genéricos.
- [x] Tipografía display: Space Grotesk / Syne; body: Geist / Satoshi; mono/data: JetBrains Mono.
- [x] Esquinas 90° o radio mínimo; grids asimétricos y bento visibles.
- [x] Bordes finos 1px en slate/800, paneles con fondo `#0C0C0F` o `#111114`.
- [x] Copy anti-AI-slop: sin em-dashes tipográficos, intensificadores ni frases de relleno.
- [x] No emojis, no Inter/Roboto/Arial, no clichés de copywriting.

## Notas de validación

- Revisado en Chrome/Chromium vía Playwright a 1440px y 390px.
- Mermaid renderiza con tema `base` y colores planos Partenon (cian/magenta/ámbar sobre fondo oscuro).
- Contadores de milestones se animan al entrar en viewport; screenshots forzaron estado final para captura estática.
- Hero glitch y marquee animados con `transform`/`opacity`; no animaciones de layout.
