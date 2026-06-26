# Arquitectura de Partenon

## Visión general

Partenon es un sistema operativo de agentes IA organizado como un panteón de héroes. Cada héroe es una distribución de Hermes Agent (Nous Research) con una personalidad, un rol y un conjunto de skills. Todos los héroes comparten un cerebro de memoria (G-Brain de Garry Tan) y entregan resultados en Google Workspace.

## Principios de diseño

1. **Hermes = empresa**: el usuario no habla con un chatbot genérico; habla con su empresa representada por agentes especializados.
2. **Un héroe, un territorio**: cada perfil tiene responsabilidades claras y no invade el territorio de otro.
3. **Memoria compartida**: todo aprendizaje se indexa en G-Brain para que los héroes futuros tengan contexto.
4. **Entrega en herramientas conocidas**: Sheets, Docs, Slides, Calendar, Gmail.
5. **Seguridad por diseño**: el Guardian protege claves, modelos y accesos.

## Componentes

### 1. Partenon Core (`partenon-core/`)

- **Onboarding engine**: pregunta tipo de empresa, necesidades y contexto inicial.
- **Router**: asigna misiones al perfil correcto según intención y disponibilidad.
- **Workflow engine**: orquesta misiones que requieren colaboración entre héroes.
- **Eval loop**: mide calidad de salidas con un judge skill y umbral configurable.

### 2. Perfiles de Hermes (`hermes/profiles/`)

Cada perfil incluye:
- `SOUL.md`: identidad y reglas de comportamiento.
- `config.yaml`: modelo, tools, MCP servers.
- `skills/<skill>/`: documentación y herramientas Python.
- `cron/`: tareas programadas.
- `templates/`: plantillas de configuración.

### 3. Dashboard (`dashboard/`)

Aplicación Next.js que muestra:
- KPIs por perfil.
- Kanban de misiones.
- Administrador de cron jobs.
- Auth simple por cookie.

### 4. Páginas web (`web/`)

- `index.html`: marketing para emprendedores.
- `heroes.html`: perfiles de héroes.
- `developers.html`: documentación técnica.

### 5. Memoria (`gbrain/`)

- Servidor MCP local para G-Brain.
- Tools de lectura/escritura de páginas.
- Búsqueda híbrida y grafo de relaciones.

## Flujo de una misión

```text
Usuario
  │
  ▼
Hermes (perfil activo de la empresa)
  │
  ▼
partenon-core: router
  │
  ├──► Tesorero      ──► Google Sheets
  ├──► Mensajero     ──► Google Docs / Slides / Redes
  ├──► Cobrador      ──► Stripe API
  ├──► Guardian      ──► NVIDIA / OpenAI / Kimi keys
  ├──► Estratega     ──► Google Calendar / Tareas
  ├──► Diplomático   ──► Google Contacts / CRM
  └──► Brain         ──► G-Brain (memoria)
```

## Comunicación entre héroes

Los héroes no se llaman directamente entre sí. Se comunican a través de:

1. **G-Brain**: cada hero escribe aprendizajes y lee contexto.
2. **Google Workspace**: hojas, documentos y calendario compartidos actúan como "tablero" visible.
3. **partenon-core**: el workflow engine orquesta misiones multi-héroe.

## Seguridad

- El Guardian administra API keys y rotaciones.
- Ningún perfil expone credenciales en conversaciones.
- `.env` nunca se commitea.
- Google Workspace usa service account con scopes mínimos.

## Escalabilidad

- Cada perfil es independiente; puede ejecutarse en su propio contenedor.
- G-Brain puede migrar de PGLite local a Postgres/Superbase.
- El dashboard escala horizontalmente si se usa una base de datos compartida.

## Tecnologías clave

| Capa | Tecnología |
|------|-----------|
| Agent core | Hermes Agent (Nous Research) |
| Sandbox | NVIDIA NemoClaw + OpenShell |
| Modelos | NVIDIA Nemotron 3 Ultra, OpenAI, Kimi / Moonshot |
| Pagos | Stripe API + Stripe Skills |
| Memoria | G-Brain de Garry Tan (MCP) |
| Datos | Google Workspace |
| Dashboard | Next.js 15 + React 19 + TypeScript |
| Docs/PDF | Python + WeasyPrint |
| Infra | Docker + Docker Compose |
