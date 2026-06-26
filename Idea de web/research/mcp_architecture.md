# Model Context Protocol (MCP) y Arquitecturas Multi-Agente

> Investigacion tecnica preparada para el hackathon **"Hermes Agent Accelerated Business Hackathon"** presentado por NVIDIA x Stripe x Nous Research.
> Fecha: Junio 2026

---

## Tabla de Contenidos

1. [Model Context Protocol (MCP)](#1-model-context-protocol-mcp)
2. [Arquitectura Multi-Agente](#2-arquitectura-multi-agente)
3. [Herramientas y APIs via MCP](#3-herramientas-y-apis-via-mcp)
4. [Sistemas de Brain / Memoria Central](#4-sistemas-de-brain--memoria-central)
5. [Arquitectura Propuesta: Hermes Central + Heroes + MCP](#5-arquitectura-propuesta-hermes-central--heroes--mcp)
6. [Relevancia para el Hackathon](#6-relevancia-para-el-hackathon)
7. [Fuentes y Referencias](#7-fuentes-y-referencias)

---

## 1. Model Context Protocol (MCP)

### 1.1 Que es MCP?

**Model Context Protocol (MCP)** es un protocolo abierto estandarizado (JSON-RPC sobre HTTP o STDIO) desarrollado originalmente por **Anthropic** en noviembre de 2024 y donado a la **Linux Foundation (AAIF - Agentic AI Foundation)** en diciembre de 2025. Su proposito es conectar aplicaciones de IA (agentes, asistentes, IDEs) con fuentes de datos externas y herramientas de forma estandarizada.

> **Analogia clave:** MCP es como **USB-C para aplicaciones de IA**. Antes de USB-C, cada dispositivo necesitaba su propio cable. MCP hace lo mismo para integraciones de IA: en lugar de construir conectores personalizados para cada fuente de datos (Google Drive, Salesforce, APIs internas), se construye contra un unico protocolo.

**Problema que resuelve:** La pesadilla de integracion M x N, donde M aplicaciones necesitan conectar con N fuentes de datos. MCP colapsa eso en **M + N implementaciones**.

**Estado actual (junio 2026):**
- 87,130+ estrellas en el repositorio de servidores MCP
- Soportado por Claude, ChatGPT, VS Code, Cursor, JetBrains IDEs, y mas
- Especificacion 2025-11-25 activa, con revision mayor en camino (2026-07-28)
- Adoptado por OpenAI, Google DeepMind, Microsoft y miles de desarrolladores

### 1.2 Arquitectura de MCP: Componentes Principales

MCP sigue una arquitectura **cliente-servidor** con cuatro componentes distintos:

```
┌─────────────────────────────────────────────────────────────────────┐
│                         HOST (Aplicacion IA)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                │
│  │ MCP Client  │  │ MCP Client  │  │ MCP Client  │  ...           │
│  │   (stdio)   │  │  (HTTP/SSE) │  │  (HTTP/SSE) │                │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                │
│         │                │                │                         │
│         └────────────────┴────────────────┘                         │
│                          Transport Layer                             │
└─────────────────────────────────────────────────────────────────────┘
         │                │                │
         ▼                ▼                ▼
   ┌──────────┐    ┌──────────┐    ┌──────────┐
   │ MCP Server│    │ MCP Server│    │ MCP Server│
   │ Filesystem│    │  GitHub   │    │  Stripe   │
   └──────────┘    └──────────┘    └──────────┘
```

#### Host
La aplicacion de IA que el usuario utiliza directamente: Claude Desktop, ChatGPT, Cursor, VS Code. Es el orquestador central que:
- Gestiona uno o mas clientes MCP
- Coordina las interacciones entre el usuario, el modelo de lenguaje y los servidores
- Controla permisos y autorizaciones (que herramientas puede usar el agente)
- Solicita aprobacion del usuario para acciones sensibles

#### Cliente MCP
Componente dentro del host que mantiene una conexion dedicada 1:1 con un servidor MCP. Maneja:
- Inicializacion y negociacion de capacidades
- Intercambio de mensajes JSON-RPC
- Subscripciones y notificaciones
- Desconexiones y timeouts

Cada cliente se conecta a exactamente un servidor. Si el host se conecta a 3 servidores, mantiene 3 clientes independientes.

#### Servidor MCP
Programa ligero que expone capacidades especificas. Recibe peticiones JSON-RPC, ejecuta operaciones y retorna resultados. Expone tres primitivas:

| Primitiva | Descripcion | Ejemplo |
|-----------|-------------|---------|
| **Tools** | Funciones ejecutables que el LLM puede invocar | `query_database`, `send_email`, `create_file` |
| **Resources** | Datos de solo lectura que proporcionan contexto | Archivos, esquemas de BD, respuestas de API |
| **Prompts** | Plantillas de instrucciones reutilizables | Templates para generar reportes, analizar codigo |

#### Transporte
Capa de comunicacion entre cliente y servidor:

| Transporte | Uso | Caracteristicas |
|------------|-----|-----------------|
| **STDIO** | Servidores locales | Proceso local, stdin/stdout, sin red, sin latencia |
| **Streamable HTTP** | Servidores remotos | HTTP POST, autenticacion OAuth, multiples clientes |

### 1.3 Ciclo de Vida de una Sesion MCP

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│     1.      │───▶│     2.      │───▶│     3.      │───▶│     4.      │───▶│     5.      │
│Inicializacion│    │  Descubrimiento  │    │  Provision   │    │ Invocacion  │    │ Ejecucion   │
│ (handshake) │    │(tools/list, etc.)│    │ de Contexto │    │ (tools/call)│    │ (result)    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

1. **Inicializacion:** Cliente envia `initialize` con version de protocolo y capacidades. Servidor responde con las suyas.
2. **Descubrimiento:** Cliente solicita lista de tools, resources y prompts disponibles.
3. **Provision de Contexto:** Recursos se exponen al usuario; tool definitions se convierten a formato que el LLM puede llamar.
4. **Invocacion:** El modelo decide que necesita una herramienta y el host enruta la peticion al servidor correspondiente.
5. **Ejecucion:** El servidor ejecuta la logica subyacente y retorna resultados estructurados.

**Diferencia clave vs REST:** MCP mantiene una **sesion stateful** abierta a traves de multiples usos de herramientas. REST trata cada peticion como independiente y stateless.

### 1.4 Como se Conectan Agentes con Herramientas Externas via MCP

El flujo de comunicacion es:

```
Usuario ──▶ Host (Claude Desktop, etc.)
              │
              ▼
         LLM/Agente (razona sobre la tarea)
              │
              ▼
         "Necesito buscar en Gmail"
              │
              ▼
         Host enruta a MCP Client (Gmail)
              │
              ▼
         JSON-RPC: tools/call → MCP Server Gmail
              │
              ▼
         Servidor ejecuta API call a Gmail
              │
              ▼
         Resultado ──▶ Host ──▶ LLM ──▶ Usuario
```

**Seguridad:** El modelo de IA **nunca ve** las credenciales (API keys, tokens OAuth). La autenticacion ocurre dentro del servidor MCP antes de que cualquier respuesta llegue al modelo. Esto crea un limite de seguridad que limita lo que un ataque de prompt injection puede extraer.

**Ejemplo real de mensaje JSON-RPC:**

```json
// Request (LLM quiere consultar base de datos)
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "query_database",
    "arguments": {
      "query": "SELECT count(*) FROM orders WHERE status = 'pending'"
    }
  }
}

// Response
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "There are 42 pending orders."
      }
    ]
  }
}
```

---

## 2. Arquitectura Multi-Agente

### 2.1 Por que Sistemas Multi-Agente?

Un sistema multi-agente organiza multiples agentes de IA especializados que colaboran para resolver tareas complejas. En lugar de un unico agente generalista que intenta hacer todo, se dividen roles y responsabilidades.

**Beneficios:**
- **Especializacion:** Cada agente domina un dominio especifico
- **Paralelismo:** Multiples tareas se ejecutan simultaneamente
- **Escalabilidad:** Se agregan agentes segun se necesitan
- **Resiliencia:** Fallo de un agente no colapsa todo el sistema
- **Modularidad:** Facil de extender y mantener

### 2.2 Patrones de Orquestacion

Los cinco patrones principales usados en produccion:

#### Patron 1: Orchestrator-Workers (Centralizado con fan-out)

```
                    ┌─────────────┐
                    │ Orchestrator│
                    │   (Central)  │
                    └──────┬──────┘
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
       ┌────────┐    ┌────────┐    ┌────────┐
       │Worker 1│    │Worker 2│    │Worker N│
       │(research)    │(write) │    │(review)│
       └────────┘    └────────┘    └────────┘
            │              │              │
            └──────────────┼──────────────┘
                           ▼
                    (Resultados agregados)
```

- Un agente orquestador central recibe la tarea y la distribuye a agentes trabajadores especializados
- Los workers ejecutan en paralelo y retornan resultados al orquestador
- El orquestador sintetiza los resultados
- **Ejemplo:** LangGraph Supervisor, CrewAI (Process.hierarchical)
- **Pros:** Control centralizado, facil de razonar sobre el flujo
- **Contras:** El orquestador es un punto unico de fallo y cuello de botella

#### Patron 2: Hub-and-Spoke (Similar a Orchestrator)

```
              ┌─────────────┐
              │   Hub       │
              │ (Central)   │
              │ Coordinator │
              └──────┬──────┘
                     │
       ┌─────┬──────┼──────┬─────┐
       ▼     ▼      ▼      ▼     ▼
     ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐
     │ A │ │ B │ │ C │ │ D │ │ E │
     └───┘ └───┘ └───┘ └───┘ └───┘
```

- Variante del patron orquestador donde el Hub coordina pero los spokes pueden comunicarse indirectamente via el hub
- Cada spoke es un agente especializado con herramientas propias
- **Pros:** Flexible, facil de agregar nuevos agentes
- **Contras:** Carga concentrada en el hub

#### Patron 3: Mesh (Peer-to-Peer)

```
     ┌───┐ ◄─────────► ┌───┐
     │ A │─────────────►│ B │
     └───┘◄─────────────┘▲  │
      ▲ │                 │  │
      │ ▼                 │  ▼
     ┌┴───┐◄─────────────┘ ┌───┐
     │ D  │────────────────►│ C │
     └────┘                 └───┘
```

- Los agentes se comunican directamente entre si sin coordinador central
- Transferencia de control (handoffs) directa entre agentes
- **Ejemplo:** OpenAI Swarm (handoff pattern)
- **Pros:** Maxima flexibilidad, minima latencia de coordinacion
- **Contras:** Dificil de depurar, puede generar ciclos, complejidad de routing

#### Patron 4: Jerarquico (Arbol)

```
                    ┌─────────┐
                    │  Boss   │
                    │(Planner)│
                    └────┬────┘
           ┌───────────┼───────────┐
           ▼           ▼           ▼
      ┌────────┐ ┌────────┐ ┌────────┐
      │Manager1│ │Manager2│ │Manager3│
      │(Tech)  │ │(Biz)   │ │(Ops)   │
      └───┬────┘ └───┬────┘ └───┬────┘
          │          │          │
        ┌─┴─┐      ┌─┴─┐      ┌─┴─┐
        ▼   ▼      ▼   ▼      ▼   ▼
       ┌─┐ ┌─┐   ┌─┐ ┌─┐   ┌─┐ ┌─┐
       │W│ │W│   │W│ │W│   │W│ │W│
       └─┘ └─┘   └─┘ └─┘   └─┘ └─┘
```

- Estructura de arbol con niveles de delegacion
- Un agente "boss" de alto nivel delega a managers de nivel medio
- Los managers a su vez delegan a workers ejecutores
- **Ejemplo:** LangGraph hierarchical, sistemas enterprise
- **Pros:** Escalable, organizacion clara, adecuado para equipos grandes
- **Contras:** Mayor latencia por niveles de delegacion, complejidad

#### Patron 5: Pipeline (Secuencial por Etapas)

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Stage 1 │───▶│  Stage 2 │───▶│  Stage 3 │───▶│  Stage 4 │
│ (Input)  │    │ (Process)│    │ (Review) │    │ (Output) │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

- Los datos fluyen secuencialmente a traves de etapas
- Cada etapa es un agente especializado que transforma la entrada
- **Ejemplo:** CrewAI (Process.sequential), procesamiento de documentos
- **Pros:** Simple, predecible, facil de depurar
- **Contras:** Sin paralelismo, etapas lentas bloquean todo el pipeline

### 2.3 Como se Comunican los Agentes Entre Si

#### Metodos de Comunicacion

| Metodo | Descripcion | Uso |
|--------|-------------|-----|
| **Message Passing** | Mensajes estructurados entre agentes | Sistemas desacoplados, mesh |
| **Shared State** | Estado global compartido que todos leen/escriben | LangGraph, CrewAI |
| **Function Calling** | Un agente invoca a otro como herramienta | Patron supervisor-workers |
| **Event Bus** | Publicacion/suscripcion de eventos | Sistemas a gran escala |
| **Handoffs** | Transferencia directa de control | OpenAI Swarm |

#### Frameworks Principales

**LangGraph (LangChain):**
- Grafo de estado dirigido donde nodos = agentes/herramientas y aristas = flujo de control
- Estado centralizado persistente (checkpointing)
- Soporta ciclos, ramificaciones, interrupciones human-in-the-loop
- Patron `langgraph-supervisor-py` para orquestacion jerarquica

**CrewAI:**
- Framework Python para orquestar agentes con roles autonomos
- Conceptos: Agent (rol + herramientas), Task (tarea), Crew (equipo), Process (secuencial/jerarquico)
- Memoria compartida integrada
- Flows para orquestacion compleja con estado estructurado

**OpenAI Swarm:**
- Framework ligero de agentes con handoffs
- Cada agente tiene instrucciones + herramientas
- Los agentes pueden transferirse el control entre si
- Ideal para flujos conversacionales

### 2.4 Diagrama Conceptual: Arquitectura Multi-Agente Completa

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           CAPA DE PRESENTACION                                   │
│  (Usuario final, Chat UI, API REST, WebSocket, Messaging: Telegram/Discord/Slack)│
└─────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         CAPA DE ORQUESTACION (Brain)                             │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                    ORQUESTADOR CENTRAL (Hermes)                          │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │    │
│  │  │  Planner │  │ Router   │  │ Memory   │  │User Model│  │Security  │  │    │
│  │  │          │  │          │  │ Manager  │  │          │  │& Auth    │  │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                       │                                          │
│                    ┌──────────────────┼──────────────────┐                       │
│                    ▼                  ▼                  ▼                       │
│              ┌──────────┐      ┌──────────┐      ┌──────────┐                   │
│              │ Memoria  │      │  Estado  │      │  Skills  │                   │
│              │ Episodic │      │  Global  │      │  Store   │                   │
│              │(historial)      │(shared)  │      │(procedural)                  │
│              └──────────┘      └──────────┘      └──────────┘                   │
└─────────────────────────────────────────────────────────────────────────────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           CAPA DE AGENTES (Heroes)                               │
│                                                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│  │  Research   │ │  Analytics  │ │  Comms      │ │  Finance    │ │  Code     │ │
│  │  Agent      │ │  Agent      │ │  Agent      │ │  Agent      │ │  Agent    │ │
│  │             │ │             │ │             │ │             │ │           │ │
│  │ • Web search│ │ • Data proc │ │ • Email     │ │ • Stripe    │ │ • Write   │ │
│  │ • Analysis  │ │ • Reports   │ │ • Calendar  │ │ • Invoicing │ │ • Review  │ │
│  │ • Summarize │ │ • Visualize │ │ • Social    │ │ • Payments  │ │ • Deploy  │ │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └─────┬─────┘ │
│         │               │               │               │              │       │
└─────────┼───────────────┼───────────────┼───────────────┼──────────────┼───────┘
          │               │               │               │              │
          ▼               ▼               ▼               ▼              ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          CAPA DE MCP SERVERS (Tools)                              │
│                                                                                  │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │ Google WS MCP│ │ Stripe MCP   │ │ Social Media │ │  Custom MCP  │            │
│  │  Server      │ │  Server      │ │  MCP Server  │ │  Servers     │            │
│  │              │ │              │ │              │ │              │            │
│  │ • Gmail      │ │ • Payments   │ │ • Twitter/X  │ │ • Database   │            │
│  │ • Drive      │ │ • Invoices   │ │ • LinkedIn   │ │ • Internal   │            │
│  │ • Calendar   │ │ • Billing    │ │ • Instagram  │ │   APIs       │            │
│  │ • Docs       │ │ • Customers  │ │ • TikTok     │ │ • Filesystem │            │
│  │ • Sheets     │ │ • Products   │ │ • YouTube    │ │ • Browser    │            │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘            │
│                                                                                  │
│  Protocolo: MCP (JSON-RPC) | Transporte: STDIO (local) / HTTP (remoto)            │
│  Auth: OAuth 2.1 | Seguridad: Credenciales nunca expuestas al LLM                │
└─────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         CAPA DE SERVICIOS EXTERNOS                                │
│                                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │  Gmail   │  │  Drive   │  │  Stripe  │  │  Social  │  │  Custom  │         │
│  │  API     │  │  API     │  │  API     │  │  APIs    │  │  APIs    │         │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Herramientas y APIs via MCP

### 3.1 Google Workspace API (Sheets, Calendar, Drive, Docs, Gmail)

Google Workspace es uno de los ecosistemas empresariales mas integrados via MCP. Existen multiples servidores MCP disponibles:

#### Google Workspace MCP Server (Oficial y Comunitario)

**Servicios soportados (12 servicios, 100+ herramientas):**

| Servicio | Herramientas Principales |
|----------|--------------------------|
| **Gmail** | Buscar emails, leer conversaciones, enviar/draft, gestionar labels |
| **Google Drive** | Buscar archivos, leer contenido, crear archivos, compartir, permisos |
| **Google Calendar** | Listar calendarios, crear eventos, verificar disponibilidad, recordatorios |
| **Google Docs** | Leer contenido, crear documentos, formatear, insertar tablas/imagenes |
| **Google Sheets** | Leer/escribir celdas, crear hojas, formatear, reglas condicionales |
| **Google Slides** | Crear presentaciones, actualizar contenido, batch update |
| **Google Chat** | Gestionar espacios, enviar mensajes, buscar historial |
| **Google Tasks** | Gestionar listas de tareas, crear tareas con jerarquia y fechas |
| **Contacts** | Buscar/crear contactos, gestionar grupos |

**Autenticacion:**
- **OAuth 2.0/2.1:** Para uso personal/CLI. Flujo PKCE para clientes publicos.
- **Service Accounts:** Para uso servidor/automatizado.
- **Multi-user:** Soporta tokens Bearer para multiples usuarios en modo stateless.

**Ejemplo de uso con agente:**
```
Usuario: "Revisa mi Gmail por emails de 'bug report' de las ultimas 48h 
          y crea un resumen en Google Docs"

Agente:
  1. Llama a MCP tool: gmail_search(query="bug report newer:2d")
  2. Lee threads relevantes con gmail_get_thread
  3. Llama a MCP tool: docs_create(title="Resumen Bug Reports", content=...)
  4. Informa al usuario con el link al documento
```

**Servidores MCP disponibles:**
- `workspacemcp` (Python, mas completo): 12 servicios, 100+ tools
- `google_workspace_mcp` (comunitario, Node.js): Oficial de Google
- `go-google-mcp` (Go): Servidor unificado en Go

**Repositorio principal:** [github.com/taylorwilsdon/google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp)

### 3.2 Stripe API

Stripe ha desarrollado un ecosistema completo para **agentic commerce**, con multiples protocolos y un MCP server oficial.

#### Productos de Stripe para Agentes (2026)

| Producto | Descripcion | Estado |
|----------|-------------|--------|
| **MCP Server** | Servidor MCP oficial para Stripe. Expone Payments, Customers, Invoices, Billing, Products | **Activo** |
| **Agentic Commerce Protocol (ACP)** | Protocolo abierto (con OpenAI) para checkout entre agentes y merchants. Define como agentes descubren y compran productos | Activo |
| **Agentic Commerce Suite** | Solucion turnkey para merchants que quieren soportar compras dirigidas por agentes | Activo |
| **Machine Payments Protocol (MPP)** | Estandar abierto (con Tempo) para billing de agentes sobre HTTP. Sesiones con pre-autorizacion y streaming de micropagos | Activo (marzo 2026) |
| **x402 Integration** | Integracion con x402 para pagos en stablecoin (USDC) sobre Base y Solana | Activo |
| **Link Agent Wallet** | Wallet para consumidores que permite delegar gasto a agentes via tarjetas de un solo uso | Activo |
| **Shared Payment Tokens (SPT)** | Tokens de pago scoped para autorizacion limitada de agentes | Activo |

**Servidor MCP de Stripe:**
- Expone herramientas para: Payments, PaymentIntents, Customers, Products, Prices, Invoices, Subscriptions, Refunds
- Permite a agentes crear pagos, gestionar clientes, facturar, suscribir
- Autenticacion via API keys de Stripe

**Ejemplo de uso:**
```
Usuario: "Crea un Payment Intent de $50 para el cliente ejemplo@email.com"

Agente:
  1. MCP tool: stripe_search_customers(query="email:ejemplo@email.com")
  2. MCP tool: stripe_create_payment_intent(amount=5000, currency="usd", 
                                              customer=customer_id)
  3. Retorna client_secret para confirmar el pago
```

**Documentacion:** [docs.stripe.com/agents](https://docs.stripe.com/agents)

### 3.3 APIs de Redes Sociales

Existen multiples servidores MCP para redes sociales, que permiten a agentes publicar, analizar y gestionar contenido:

#### Opciones Disponibles

| Servidor | Plataformas | Tools | Tipo |
|----------|-------------|-------|------|
| **Ayrshare MCP** | 13+ plataformas (X, FB, IG, LI, YT, etc.) | 75+ | Comercial |
| **bundle.social MCP** | 14+ plataformas | 30+ | Comercial |
| **SocialCrawl MCP** | 42 plataformas, 264 endpoints | 100+ | Comercial |
| **Postiz MCP** | X, LI, IG, FB (open-source) | Variable | Self-hosted |
| **Xpoz MCP** | X, IG, TikTok (datos) | 20+ | Remoto |
| **GetXAPI MCP** | X/Twitter completo | 44 | Comercial |

**Plataformas cubiertas:**
- X (Twitter), Instagram, TikTok, LinkedIn, YouTube, Facebook
- Pinterest, Reddit, Threads, Bluesky, Mastodon
- Discord, Slack, Telegram, WhatsApp
- Google Business Profile

**Ejemplo de uso con agente:**
```
Usuario: "Publica un resumen de nuestro lanzamiento en Twitter y LinkedIn"

Agente:
  1. MCP tool: social_create_post(platform="twitter", content="...")
  2. MCP tool: social_create_post(platform="linkedin", content="...")
  3. MCP tool: social_schedule_post(post_id=..., schedule_time="...")
```

### 3.4 Como se Conectan Estas Herramientas via MCP

**Patron de integracion:**

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         AGENTE / HOST                                       │
│  (Claude, ChatGPT, Hermes, LangGraph, CrewAI, etc.)                        │
│                                                                            │
│  Perfil de herramientas disponibles:                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │ • google_gmail_search    • stripe_create_payment_intent            │  │
│  │ • google_drive_read      • stripe_create_customer                  │  │
│  │ • google_calendar_create • social_create_post                      │  │
│  │ • google_docs_write      • social_analyze_engagement               │  │
│  │ • google_sheets_update   • stripe_create_invoice                   │  │
│  │ • ...                    • ...                                     │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘
        │                    │                    │
        ▼                    ▼                    ▼
  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
  │ MCP Server   │   │ MCP Server   │   │ MCP Server   │
  │ Google WS    │   │ Stripe       │   │ Social Media │
  │              │   │              │   │              │
  │ Transport:   │   │ Transport:   │   │ Transport:   │
  │ HTTP/STDIO   │   │ HTTP         │   │ HTTP         │
  │ Auth: OAuth  │   │ Auth: API Key│   │ Auth: API Key│
  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
         │                  │                  │
         ▼                  ▼                  ▼
  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
  │ Google APIs  │   │ Stripe API   │   │ Social APIs  │
  │ (REST/gRPC)  │   │ (REST)       │   │ (REST)       │
  └──────────────┘   └──────────────┘   └──────────────┘
```

**Flujo de configuracion:**
1. El host configura los servidores MCP en su configuracion (archivo JSON o UI)
2. En el inicio, el host se conecta a cada servidor via su transporte
3. Cada servidor declara sus herramientas durante el handshake
4. Las herramientas se exponen al LLM como funciones disponibles
5. El LLM razona sobre que herramienta usar y cuando

---

## 4. Sistemas de Brain / Memoria Central

### 4.1 Concepto de Sistema Central (Brain)

Un **sistema brain** o **coordinador central** es el componente que:
- Recibe las peticiones del usuario
- Decide que agentes especializados activar
- Mantiene el estado global del sistema
- Gestiona la memoria compartida entre agentes
- Coordina la comunicacion entre agentes

Es el **equivalente al cortex prefrontal** en un sistema multi-agente: planifica, decide, y coordina.

### 4.2 Tipos de Memoria en Sistemas Multi-Agente

#### Las Tres Capas de Memoria (inspirado en Hermes Agent)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CAPA 1: MEMORIA EPISODICA                       │
│  (SQLite FTS5 database - ~/.hermes/state.db)                       │
│                                                                    │
│  • Historial completo de conversaciones                            │
│  • Full-text search sobre interacciones pasadas                    │
│  • Cada interaccion con timestamp, contexto, resultado             │
│  • Permite al agente "recordar" conversaciones especificas         │
│                                                                    │
│  Uso: "Que me dijo el usuario sobre X la semana pasada?"          │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    CAPA 2: MEMORIA SEMANTICA                         │
│  (MEMORY.md + USER.md files)                                       │
│                                                                    │
│  • Hechos, preferencias, lecciones aprendidas                      │
│  • Perfil de usuario: estilo de comunicacion, timezone, idioma     │
│  • Conocimiento acumulado sobre el dominio                         │
│  • Actualizada periodicamente por el agente mismo                  │
│                                                                    │
│  Uso: "El usuario prefiere los reportes en espanol"               │
│       "La deadline del proyecto X es el viernes"                  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    CAPA 3: MEMORIA PROCEDURAL                        │
│  (Skills auto-generadas en ~/.hermes/skills/)                       │
│                                                                    │
│  • Plantillas de razonamiento creadas de tareas exitosas           │
│  • Cada skill: nombre, descripcion, procedimiento paso a paso      │
│  • Mejoradas continuamente con el uso                              │
│  • El agente las lee/desccubre automaticamente                     │
│                                                                    │
│  Uso: "Como generar un reporte de ventas" -> Skill predefinida     │
└─────────────────────────────────────────────────────────────────────┘
```

#### Estrategias de Merge de Memoria

Cuando multiples agentes escriben en memoria compartida concurrentemente:

| Estrategia | Descripcion | Uso |
|------------|-------------|-----|
| **Last-Write-Wins (LWW)** | La escritura mas reciente sobreescribe | OpenAI Swarm, implementaciones simples |
| **Orchestrator-Mediated** | El supervisor secuencia todas las escrituras | Arquitecturas jerarquicas |
| **Reducer Functions** | Funcion explicita de merge por clave de estado | LangGraph (deterministico, type-safe) |
| **LLM-Assisted** | Un LLM evalua y consolida entradas nuevas | CrewAI, Mem0 (maneja conflictos semanticos) |
| **Event Sourcing** | Se almacenan operaciones, no estado actual | Enterprise (audit trail completo) |

#### Patrones de Sincronizacion

| Patron | Descripcion | Framework |
|--------|-------------|-----------|
| **Immediate Consistency** | Todos leen del mismo store. Escrituras visibles inmediatamente | LangGraph, CrewAI |
| **Event-Driven** | Cambios emiten eventos, agentes suscritos reciben notificaciones | Agent-MCP |
| **Checkpoint-Based** | Agentes trabajan independientemente y sincronizan periodicamente | LangGraph checkpointing |
| **Polling Semantico** | Agentes consultan periodicamente cambios relevantes via embeddings | Implementaciones custom |

### 4.3 Arquitectura de Memoria Recomendada por Escala

**Pequenos equipos (2-5 agentes):**
- Memoria compartida con scoping ligero
- CrewAI unified memory o LangGraph centralized state
- Prefijos de scope para evitar ruido

**Equipos medianos (5-20 agentes):**
- Memoria jerarquica de tres capas:
  - `/global/` - Objetivos de proyecto, decisiones compartidas
  - `/team/<dominio>/` - Conocimiento especifico por equipo
  - `/agent/<id>/` - Memoria de trabajo privada por agente
- Backend: PostgreSQL + pgvector

**Enterprise (20+ agentes, multi-tenant):**
- Capa de memoria dedicada (Mem0 o similar)
- Aislamiento estricto por tenant
- Event sourcing para auditoria
- Acceso zero-trust con verificacion por query

### 4.4 Estado Global

El **estado global** es el conjunto de datos compartidos que todos los agentes pueden leer y (algunos) escribir:

```python
# Ejemplo en LangGraph
class GlobalState(TypedDict):
    messages: Annotated[list, add_messages]  # Historial de mensajes
    user_query: str                          # Consulta actual
    research_results: list                   # Resultados de investigacion
    draft_content: str                       # Borrador en progreso
    approved: bool                           # Flag de aprobacion
    current_agent: str                       # Agente activo
    error_count: int                         # Conteo de errores
```

**Caracteristicas del estado global:**
- Tipado (Pydantic/TypedDict)
- Funciones de reduccion para merges deterministicos
- Persistencia (checkpointing)
- Recuperacion ante fallos (resumability)

---

## 5. Arquitectura Propuesta: Hermes Central + Heroes + MCP

### 5.1 Vision General

Propuesta de arquitectura para el hackathon inspirada en **Hermes Agent** de Nous Research, integrando MCP como capa de herramientas:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                        SISTEMA HERMES CENTRAL                                │
│                     "El cerebro que coordina todo"                           │
│                                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  Perfil  │  │  Router  │  │  Planner │  │  Memory  │  │  Skill   │      │
│  │  Builder │  │          │  │          │  │  System  │  │  Manager │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
│                                                                              │
│  • Perfiles aislados (coding, research, business)                            │
│  • Routing inteligente de tareas a heroes                                    │
│  • Planificacion multi-paso con objetivos claros                             │
│  • Memoria episodica + semantica + procedural                                │
│  • Skills auto-generadas + MCP servers                                       │
│                                                                              │
│  Soporta: OpenRouter, NVIDIA NIM, OpenAI, AWS Bedrock, Ollama (local)       │
│                                                                              │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   HEROE FINANZAS │ │  HEROE COMMS     │ │  HEROE ANALISIS │
│   (Stripe Agent) │ │  (Google WS +    │ │  (Research +    │
│                  │ │   Social Media)  │ │   Data Agent)   │
│  • MCP Stripe    │ │                  │ │                  │
│  • Pagos         │ │  • MCP Gmail      │ │  • MCP Search    │
│  • Facturas      │ │  • MCP Calendar   │ │  • MCP Browser   │
│  • Clientes      │ │  • MCP Drive      │ │  • MCP Docs      │
│  • Suscripciones │ │  • MCP Docs       │ │  • Code exec     │
│  • x402/MPP pay  │ │  • MCP Sheets     │ │  • Data analysis │
│                  │ │  • MCP Social     │ │                  │
│  Tools:          │ │    (X, LI, IG)    │ │  Tools:          │
│  create_payment  │ │                  │ │  web_search      │
│  create_customer │ │  Tools:          │ │  extract_data    │
│  create_invoice  │ │  send_email       │ │  generate_report │
│  create_refund   │ │  create_event     │ │  analyze_trends  │
│  get_balance     │ │  share_file       │ │  write_code      │
│  ...             │ │  write_doc        │ │  ...             │
│                  │ │  post_social      │ │                  │
│                  │ │  schedule_post    │ │                  │
└─────────────────┘ └─────────────────┘ └─────────────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │  Stripe  │ │  Google  │ │  Social  │
        │  API     │ │  APIs    │ │  APIs    │
        └──────────┘ └──────────┘ └──────────┘
```

### 5.2 Flujo de Trabajo Ejemplo

```
Usuario: "Necesito que generes un reporte mensual de ventas, 
          lo envies por email al equipo y programe una reunion 
          para discutirlo, todo para el cliente Acme Corp."

┌─────────────────────────────────────────────────────────────────────────────┐
│ PASO 1: HERMES CENTRAL recibe la peticion                                    │
│ • Parsea la intencion: generar reporte + enviar email + crear reunion       │
│ • Consulta memoria: "Acme Corp es cliente premium, contacto: juan@acme.com" │
│ • Crea plan de 3 pasos                                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              ▼                     ▼                     ▼
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│ HEROE ANALISIS       │ │ HEROE FINANZAS       │ │ HEROE COMMS          │
│                      │ │                      │ │                      │
│ 1. MCP Sheets: lee   │ │ 1. MCP Stripe:       │ │ 1. MCP Docs: crea    │
│    datos de ventas   │ │    obtiene transac-  │ │    documento con     │
│    del mes           │ │    ciones de Acme    │ │    reporte           │
│                      │ │    Corp              │ │                      │
│ 2. Analiza tenden-   │ │ 2. Calcula totales   │ │ 2. MCP Gmail: envia  │
│    cias, genera      │ │    y métricas        │ │    email al equipo   │
│    insights          │ │                      │ │    con el reporte    │
│                      │ │                      │ │                      │
│ 3. Genera graficos   │ │                      │ │ 3. MCP Calendar:     │
│    y visualiza-      │ │                      │ │    crea reunion para │
│    ciones            │ │                      │ │    discutir reporte  │
│                      │ │                      │ │    (invita al equipo)│
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘
              │                     │                     │
              └─────────────────────┼─────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PASO 3: HERMES CENTRAL agrega resultados                                    │
│ • Almacena en memoria: "Reporte Acme Corp enviado el [fecha]"              │
│ • Actualiza USER.md si hay nuevas preferencias                             │
│ • Crea skill si detecta patron repetitivo: "monthly_sales_report"          │
│ • Responde al usuario: "Listo. Reporte generado, email enviado a 5        │
│   personas, y reunion programada para el martes 10am."                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.3 Componentes Clave de Implementacion

| Componente | Tecnologia | Descripcion |
|------------|-----------|-------------|
| **Hermes Core** | Python/TypeScript | Orquestador central basado en Hermes Agent |
| **MCP Client** | Oficial MCP SDK | Conexion a servidores MCP |
| **MCP Servers** | Google WS, Stripe, Social | Servidores de herramientas |
| **Memory Store** | SQLite + Filesystem | Memoria episodica, semantica, procedural |
| **LLM Provider** | OpenRouter / NVIDIA NIM | Acceso a 200+ modelos |
| **State Management** | LangGraph / Custom | Estado global con checkpointing |
| **Transport** | STDIO / HTTP | Comunicacion local y remota |

---

## 6. Relevancia para el Hackathon

### 6.1 Contexto: Hermes Agent Accelerated Business Hackathon

> **Organizadores:** Nous Research x NVIDIA x Stripe
> **Enfoque:** Construir agentes que pueden ganar, gastar y operar negocios reales a cualquier escala
> **Premios:** 1er lugar: $10,000 + NVIDIA DGX Spark + $5,000 Stripe Credits

**Recursos proporcionados:**
- **NVIDIA NeMoClaw:** Ejecutar agentes de forma segura con acceso a skills extensivas
- **Stripe Skills para Hermes:** Agentes pueden comprar lo que necesitan, aprovisionar su propio SaaS, pagar por servicios que usan
- **Hermes Agent Framework:** Open-source, self-improving, con soporte MCP integrado

### 6.2 Por que esta Arquitectura es Relevante

1. **Hermes ya tiene soporte MCP integrado:** El framework acepta servidores MCP via URL (HTTP) o comando local (STDIO). Hay un catalogo de instalacion one-click.

2. **Stripe Skills nativas:** Las nuevas Stripe Skills para Hermes permiten que los agentes realicen pagos, facturen, gestionen suscripciones, y usen x402 para stablecoins.

3. **NVIDIA NeMoClaw:** Proporciona un entorno seguro para ejecutar agentes con acceso a un ecosistema de skills pre-construidas.

4. **Perfiles aislados:** Hermes permite crear perfiles separados (coding, research, business) que no comparten estado - perfecto para el patron Central + Heroes.

5. **El learning loop de Hermes:** El agente mejora automaticamente con el uso, creando skills reutilizables - ideal para un negocio que opera continuamente.

### 6.3 Oportunidades de Proyecto

| Idea | Descripcion | Herramientas MCP |
|------|-------------|------------------|
| **Agente de Negocio Autonomo** | Agente que opera un negocio completo: gestiona clientes (Stripe), comunicaciones (Gmail), agenda (Calendar), marketing (Social) | Stripe, Google WS, Social |
| **Sistema de Facturacion Inteligente** | Lee contratos en Drive, genera facturas en Stripe, envia por Gmail, programa seguimiento | Google Docs, Stripe, Gmail, Calendar |
| **Agente de Marketing** | Analiza tendencias, crea contenido, publica en redes, reporta resultados | Social Media MCP, Google Sheets |
| **Concierge Empresarial** | Recibe peticiones por Slack/Email, coordina multiples heroes para ejecucion | Google WS, Slack MCP, Stripe |

### 6.4 Ventajas Competitivas de esta Arquitectura

1. **Modularidad:** Cada heroe es independiente, se pueden agregar/quitar sin afectar al sistema
2. **Extensibilidad:** Nuevas herramientas se integran via MCP sin cambiar codigo de agentes
3. **Seguridad:** Credenciales nunca expuestas al LLM, sandboxing por container
4. **Aprendizaje:** El sistema mejora con cada tarea ejecutada (skills auto-generadas)
5. **Escalabilidad:** Arquitectura probada que escala de 1 a 20+ agentes

---

## 7. Fuentes y Referencias

### Documentacion Oficial

| Recurso | URL |
|---------|-----|
| **MCP Specification (GitHub)** | https://github.com/modelcontextprotocol |
| **MCP Servers Repository** | https://github.com/modelcontextprotocol/servers |
| **MCP Python SDK** | https://github.com/modelcontextprotocol/python-sdk |
| **MCP TypeScript SDK** | https://github.com/modelcontextprotocol/typescript-sdk |
| **MCP Official Docs** | https://modelcontextprotocol.io |
| **Stripe Agents Docs** | https://docs.stripe.com/agents |
| **Stripe MCP Server** | https://github.com/stripe/ai |
| **Hermes Agent Repo** | https://github.com/nousresearch/hermes-agent |
| **Hermes Agent Docs** | https://hermes-agent.nousresearch.com/docs |
| **CrewAI Docs** | https://docs.crewai.com |
| **LangGraph Docs** | https://langchain-ai.github.io/langgraph |
| **Nous Research Twitter** | https://x.com/NousResearch |

### Articulos y Guias

| Recurso | URL | Tema |
|---------|-----|------|
| A Year of MCP: 2025 Review | https://www.pento.ai/blog/a-year-of-mcp-2025-review | Estado del ecosistema MCP |
| MCP Server Architecture Explained | https://www.skyvern.com/blog/mcp-server-architecture-explained/ | Arquitectura de servidores MCP |
| What Is an MCP Server (Zuplo) | https://zuplo.com/learning-center/what-is-an-mcp-server | Guia completa MCP |
| MCP Explained (CodiLime) | https://codilime.com/blog/model-context-protocol-explained/ | Overview tecnico practico |
| Agent Orchestration Patterns | https://gurusup.com/blog/agent-orchestration-patterns | Patrones de orquestacion |
| Multi-Agent Memory Architectures | https://zylos.ai/research/2026-03-09-multi-agent-memory-architectures-shared-isolated-hierarchical | Memoria en sistemas multi-agente |
| Google Workspace MCP Server | https://github.com/taylorwilsdon/google_workspace_mcp | Servidor MCP para Google WS |
| Google Workspace MCP (workspacemcp) | https://workspacemcp.com | Sitio oficial del servidor |
| bundle.social MCP for Social Media | https://bundle.social/social-media-api-for-ai-agents | API social para agentes |
| Ayrshare MCP Server | https://github.com/ayrshare/mcp-server | Servidor MCP multi-plataforma social |
| SocialCrawl MCP | https://github.com/socialcrawl/mcp | 42 plataformas sociales |
| Hermes Agent: What It Is | https://openhosst.com/blog/hermes-agent | Guia completa de Hermes |
| Hermes Agent Breakdown | https://techjacksolutions.com/ai-tools/hermes/hermes-breakdown/ | Guia definitiva Hermes |
| Hermes Reference Architecture | https://chatbotkit.com/examples/hermes-agent-reference-architecture | Arquitectura de referencia |
| Agentic Commerce Protocols Tracker | https://agenticplug.ai/current-state-of-agentic-commerce | Estado de protocolos de comercio |
| x402 and AI Agents | https://www.galaxy.com/insights/research/x402-ai-agents-crypto-payments | x402 y pagos de agentes |
| Stripe Link Agents and x402 | https://eco.com/support/en/articles/14839406-stripe-link-agents-and-x402-explained | Explicacion de productos Stripe |
| MPP vs x402 Comparison | https://www.crossmint.com/learn/agentic-payments-protocols-compared | Comparacion de protocolos de pago |
| The Agentic Web | https://www.emergingfintech.co/p/the-agentic-web-inside-the-protocol | Carrera de protocolos M2M |
| Nous Research Profile Builder | https://www.marktechpost.com/2026/06/11/nous-research-ships-hermes-agent-profile-builder-identity-model-skills-and-mcp-servers-in-one-dashboard-flow/ | Nuevo dashboard de Hermes |

### Repositorios Relevantes

| Repositorio | URL | Descripcion |
|-------------|-----|-------------|
| NousResearch/hermes-agent | https://github.com/nousresearch/hermes-agent | Framework de agente open-source |
| crewAIInc/crewAI | https://github.com/crewaiinc/crewai | Framework multi-agente Python |
| langchain-ai/langgraph | https://github.com/langchain-ai/langgraph | Orquestacion con grafos de estado |
| langchain-ai/langgraph-supervisor-py | https://github.com/langchain-ai/langgraph-supervisor-py | Patron supervisor para LangGraph |
| stripe/ai | https://github.com/stripe/ai | Integraciones de Stripe para AI |
| taylorwilsdon/google_workspace_mcp | https://github.com/taylorwilsdon/google_workspace_mcp | MCP server para Google Workspace |
| socialcrawl/mcp | https://github.com/socialcrawl/mcp | MCP para redes sociales |
| TensorBlock/awesome-mcp-servers | https://github.com/TensorBlock/awesome-mcp-servers | Lista curada de servidores MCP |

---

## Anexo: Glosario de Terminos

| Termino | Definicion |
|---------|------------|
| **MCP** | Model Context Protocol - Protocolo estandar para conectar IA con herramientas |
| **Host** | Aplicacion de IA que el usuario utiliza (Claude Desktop, etc.) |
| **MCP Client** | Componente dentro del host que se conecta a un servidor MCP |
| **MCP Server** | Programa que expone herramientas, recursos y prompts via MCP |
| **Tool** | Funcion ejecutable que un LLM puede invocar |
| **Resource** | Fuente de datos de solo lectura para contexto |
| **Prompt** | Plantilla de instrucciones reutilizable |
| **STDIO** | Transporte local via entrada/salida estandar |
| **Hero** | Agente especializado en la arquitectura propuesta |
| **Brain** | Sistema central coordinador (Hermes) |
| **Skill** | Plantilla de procedimiento reutilizable auto-generada |
| **x402** | Protocolo HTTP-native para pagos con stablecoins |
| **MPP** | Machine Payments Protocol (Stripe & Tempo) |
| **ACP** | Agentic Commerce Protocol (Stripe & OpenAI) |
| **SPT** | Shared Payment Token (autorizacion scoped de pago) |
| **Handoff** | Transferencia de control entre agentes |
| **Checkpoint** | Punto de guardado del estado para recuperacion |
| **Event Sourcing** | Almacenar operaciones en lugar de estado actual |

---

*Documento preparado para investigacion tecnica del hackathon "Hermes Agent Accelerated Business Hackathon" por Nous Research x NVIDIA x Stripe. Junio 2026.*
