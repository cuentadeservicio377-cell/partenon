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
  - [x] Framework, skills, herramientas, MCP, personalidad, profile.
  - [x] Cómo se conecta, según documentación, interconexiones.
- [x] Diagramas punto a punto por héroe (Tesorero/Sheets, Cobrador/Stripe, Guardián/modelos, Mensajero/canales).
- [x] G-Brain/MCP técnico con diagrama de perfiles read/write.
- [x] Stack y estructura de repositorio con archivos `.finance`, `.design`, `.payments`, `.security`, `.ops`, `.relations`.
- [x] Workshop técnico paquetizado de 90 min:
  - [x] Pre-instalación con comando.
  - [x] Revisión inicial.
  - [x] Onboarding técnico.
  - [x] Explicación gráfica del proceso con diagrama de secuencia.

### Diseño

- [x] Rediseño aprobado: estilo Nous Research / manual técnico open source con anti-slop.
- [x] Fondo OLED `#050505` / `#08080C`, con mesh radial sutil, noise SVG y scanlines opcionales.
- [x] Acento único cian `#00D4FF` (saturación <80%); ámbar `#FFB800` en no más de 2 elementos por página.
- [x] Tipografía display: Space Grotesk; body: Geist; mono/data: JetBrains Mono (usado también en hero para efecto técnico); icons: Material Symbols Sharp.
- [x] Cards con doble-bisel (outer shell 18px + inner core 12px); botones `rounded-full`.
- [x] Nav flotante tipo "fluid island" con backdrop blur y menú móvil staggered.
- [x] Layouts asimétricos y bento; colapso agresivo a una columna bajo 768px.
- [x] Copy anti-AI-slop: sin em-dashes, intensificadores, filler phrases, transiciones dramáticas ni clichés de IA.
- [x] No emojis, no Inter/Roboto/Arial/Open Sans/Helvetica, no Lucide grueso.

## Notas de validación

- Revisado en Chrome/Chromium vía Playwright a 1440px y 390px.
- Mermaid renderiza con tema `base` y `themeVariables` custom (fondos `#111118`, bordes `#00D4FF`, texto `#E8E8ED`).
- Contadores de milestones se animan al entrar en viewport.
- Reveals con `IntersectionObserver` + CSS `transform`/`opacity`; sin animaciones de layout.
- Pre-flight anti-slop: sin emdashes, intensificadores ni headings dramáticos.
