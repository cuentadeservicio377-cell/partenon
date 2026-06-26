# Tecnologias NVIDIA para "The Hermes Agent Accelerated Business Hackathon"

> Hackathon presentado por Nous Research x NVIDIA x Stripe (Junio 2026)
> Investigacion tecnica para construccion de sistemas multi-agente de negocios

---

## 1. NemoClaw - Blueprint de Seguridad para Agentes Autonomos

### Que es

**NVIDIA NemoClaw** es una coleccion de blueprints (planos) open-source para construir agentes autonomos seguros. NemoClaw ayuda a los equipos a pasar de prototipos de agentes a despliegues gobernados, integrando controles de runtime, enrutamiento de modelos, ejecucion de skills, estado y observabilidad en caminos de configuracion integrados.

En esencia, NemoClaw es el **wrapper de seguridad enterprise** para agentes de IA. No reemplaza al agente -- lo envuelve con controles de grado empresarial. Fue desarrollado por NVIDIA como respuesta a la necesidad de plataformas de agentes seguras, gobernables y cumplidoras de regulaciones despues del auge de OpenClaw.

### Componentes Clave

NemoClaw integra varios componentes del NVIDIA Agent Toolkit:

| Componente | Funcion |
|---|---|
| **OpenShell** | Runtime sandbox con politicas de seguridad declarativas (YAML) que aplica defensa en profundidad en 4 capas: filesystem, red, proceso e inferencia |
| **Privacy Router** | Enrutador inteligente que decide si una consulta se procesa localmente (datos sensibles) o en la nube (datos no sensibles) basado en politicas de privacidad |
| **Nemotron** | Modelos locales de NVIDIA para inferencia privada sin salir de la infraestructura |
| **Nemo** | Framework de especializacion y optimizacion de modelos |

### Como Funciona la Seguridad (OpenShell)

OpenShell es el nucleo de seguridad de NemoClaw. Es un **runtime open-source** que ejecuta agentes de IA en entornos sandboxed con aislamiento a nivel de kernel:

- **Filesystem**: Previene lecturas/escrituras fuera de rutas permitidas (bloqueado en creacion)
- **Network**: Bloquea conexiones salientes no autorizadas (hot-reloadable en runtime)
- **Process**: Bloquea escalada de privilegios y syscalls peligrosas (bloqueado en creacion)
- **Inference**: Redirige llamadas a APIs de modelo a backends controlados (hot-reloadable)

Todas las politicas se definen en archivos YAML declarativos, lo que permite versionado, revision por pares y auditoria. El modelo es **deny-by-default**: todo esta bloqueado salvo lo explicitamente permitido.

### Instalacion con Hermes

```bash
# Instalar Hermes con NemoClaw (un solo comando)
curl -fsSL https://www.nvidia.com/nemoclaw.sh | NEMOCLAW_AGENT=hermes bash
```

El wizard de NemoClaw configura el proveedor de inferencia, modelo, credenciales y nombre del sandbox. Luego registra inferencia, configura canales de mensajeria, construye e inicia el sandbox, configura Hermes y aplica las politicas de red y presets seleccionados.

### Relevancia para Sistemas Multi-Agente de Negocios

- **Gobernanza**: Permite que agentes especializados colaboren con agentes generales frontier manteniendo datos y acciones sensibles bajo politica
- **Aislamiento**: Cada agente corre en su propio sandbox con politicas individuales -- ideal para arquitecturas multi-agente
- **Auditoria**: Trail completo de todas las acciones y decisiones de politica para cumplimiento regulatorio
- **Privacy Router**: Mantiene datos financieros, PII y propietarios en infraestructura local
- **Ideal para**: Servicio al cliente, gestion de cadena de suministro, seguridad IT, operaciones financieras

**Fuentes:**
- https://www.nvidia.com/en-us/ai/nemoclaw/
- https://docs.nvidia.com/openshell/about/overview
- https://github.com/NVIDIA/openshell
- https://docs.nvidia.com/nemoclaw/user-guide/hermes/get-started/quickstart

---

## 2. Nemotron 3 Ultra - Modelo de Razonamiento para Agentes

### Que es

**NVIDIA Nemotron 3 Ultra** es un modelo open-weight de **550B parametros** (55B activos por token) disenado especificamente para **orquestacion y razonamiento frontier en sistemas agenticos**. Es el modelo mas grande y capaz de la familia Nemotron 3, lanzado en junio de 2026.

Emplea una arquitectura **hibrida LatentMoE (Mixture-of-Experts)** con capas intercaladas de Mamba-2 y MoE junto con capas de Atencion selectiva, mas **Multi-Token Prediction (MTP)** para generacion mas rapida. Soporta **hasta 1 millon de tokens de contexto**.

### Capacidades Clave

| Capacidad | Detalle |
|---|---|
| **Parametros** | 550B totales / 55B activos por token (MoE) |
| **Arquitectura** | Hybrid Mamba-2 + MoE + Attention + MTP |
| **Contexto** | Hasta 1M tokens |
| **Razonamiento** | Configurable on/off via chat template |
| **Idiomas** | Ingles, Frances, Espanol, Italiano, Aleman, Japones, Hindi, Coreano, Portugues, Chino |
| **Throughput** | 5x mayor que modelos abiertos comparables |
| **Reduccion de costo** | Hasta 30% menos tokens por tarea agentica |

### Rendimiento en Benchmarks

| Benchmark | Nemotron 3 Ultra | Competidores |
|---|---|---|
| Agent Productivity (PinchBench) | **91%** | GLM 5.1: 84%, Qwen3.5: 89% |
| Instruction Following (IFBench) | **82%** | GLM 5.1: 77%, Kimi K2.6: 74% |
| Long Context (Ruler @1M) | **95%** | Qwen3.5: 90% |
| ProfBench (Search) | **56%** | GLM 5.1: 46% |
| Coding (Terminal-Bench 2.0) | 54% | Kimi K2.6: 67% |
| Long-horizon Planning | 33% | GLM 5.1: 40% |

Artificial Analysis reporto Nemotron 3 Ultra en **48 en su Intelligence Index**, siendo el modelo open-weight lider de EE.UU. en ese momento, con mas de **300 tokens de salida por segundo**.

### Innovaciones Arquitectonicas

1. **Post-entrenamiento para agent harness**: Entrenado con NVIDIA NeMo RL y Gym usando uno de los datasets mas grandes de tareas de larga duracion, resolucion de problemas y uso de herramientas. Optimizado para workflows donde agentes planean, llaman herramientas, leen observaciones, delegan a sub-agentes, validan outputs y se recuperan de errores.

2. **Hybrid Mamba-Transformer**: Capas Mamba mejoran eficiencia de secuencia para workloads de largo contexto; capas Transformer preservan recall preciso.

3. **NVFP4 precision**: Un solo checkpoint corre en Hopper, Blackwell y Ampere GPUs con hasta 5x throughput por GPU.

4. **LatentMoE**: Routing de expertos mas eficiente para workflows de razonamiento, generacion de codigo, llamadas a herramientas y logica de dominio.

5. **Multi-token prediction**: Predice multiples tokens futuros en un solo forward pass, reduciendo tiempo de generacion.

### Relevancia para Agentes de Negocios

- **Orquestador en sistemas multi-agente**: Su escala y calidad de razonamiento lo hacen ideal como coordinador de sub-agentes especializados
- **Razonamiento de frontier**: Maneja las llamadas mas dificiles en workflows agenticos -- planificacion, generacion de codigo, investigacion profunda
- **Costo eficiente**: Reduce costo de tareas agenticas hasta 30% usando menos tokens totales
- **Velocidad**: 5x throughput permite agentes de larga ejecucion que completan tareas mas rapido
- **Contexto largo**: 1M tokens permite mantener estado completo en sesiones largas de negocio

**Fuentes:**
- https://developer.nvidia.com/blog/nvidia-nemotron-3-ultra-powers-faster-more-efficient-reasoning-for-long-running-agents/
- https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16
- https://openrouter.ai/nvidia/nemotron-3-ultra-550b-a55b
- https://developer.nvidia.com/topics/ai/nemotron

---

## 3. NVIDIA Agent Skills - Habilidades Verificadas para Agentes

### Que Son

Las **NVIDIA-Verified Agent Skills** son **conjuntos de instrucciones portatiles** que extienden lo que un agente de IA puede hacer. Ensenan al agente como usar librerias NVIDIA CUDA-X, AI Blueprints, flujos de trabajo Omniverse y Physical AI, herramientas de entrenamiento e inferencia NeMo, y otros componentes de plataforma.

Las skills se basan en la **especificacion abierta Agent Skills** (agentskills.io) y estan disenadas para funcionar entre multiples agentes compatibles: Claude Code, Codex, OpenClaw, Kiro, Aider, Augment, y **Hermes Agent**.

### Tipos de Skills Disponibles

Las skills de NVIDIA cubren multiples categorias:

| Categoria | Ejemplos de Skills |
|---|---|
| **Optimizacion y Programacion** | cuOpt -- routing, scheduling, linear programming, quadratic programming |
| **RAG y Agentes** | Despliegue, configuracion, evaluacion y troubleshooting de RAG, AI-Q, NemoClaw, y sandboxes de agentes |
| **Inferencia y Serving** | Dynamo y NeMo Platform para flujos de inferencia |
| **Entrenamiento de Modelos** | NeMo, Megatron-Core, DALI, Nemotron -- entrenamiento distribuido |
| **Datos y Cientifico** | cuDF, cuPyNumeric, CUDA-Q, Earth2Studio, PhysicsNeMo, TileGym |
| **Vision y Video** | DeepStream, Video Search and Summarization, CAD-to-SimReady |
| **Physical AI** | Omniverse USD workflows, real-time viewing, neural reconstruction |

### Como Funcionan

1. **Instalacion portable**: Se instalan una vez con `npx skills add nvidia/skills`
2. **Activacion condicional**: El agente carga procedimientos, referencias, scripts y limites de seguridad cuando aparece una tarea que coincide
3. **Progressive disclosure**: No cargan hasta que el agente decide que las necesita (eficiencia de tokens)
4. **Gobernanza**: NVIDIA provee verificacion de confianza -- escaneo de riesgos, firmas digitales, y pipeline de validacion

### Distribucion

- **Skills.sh** y **NVIDIA Build** como fuentes oficiales
- **Vercel skills CLI** como vehiculo de entrega
- **Claude Code y Codex marketplaces**
- **Hermes Skillhub** (planificado)

### Relevancia para Negocios

- **Especializacion sin reentrenamiento**: Un agente de negocios puede adquirir capacidades especializadas (optimizacion, analisis de datos, vision) instalando skills
- **Portabilidad**: Las mismas skills funcionan en diferentes agentes del ecosistema
- **Seguridad verificada**: Pipeline de confianza que escanea skills antes de instalacion, verifica firmas, y controla riesgos
- **Acelera desarrollo**: No es necesario programar desde cero integraciones con librerias NVIDIA

**Fuentes:**
- https://docs.nvidia.com/skills
- https://alphasignal.ai/news/nous-research-s-hermes-agent-can-now-spend-real-money-autonomously

---

## 4. Integracion NVIDIA + Hermes (Nous Research)

### Sinergia Tecnica

La integracion entre NVIDIA y Hermes (de Nous Research) se anuncio como parte del hackathon y combina tres lineas de integracion:

**1. NemoClaw + Hermes (Seguridad)**
- Hermes Agent corre dentro del sandbox de OpenShell via NemoClaw
- El loop de skills-and-memory de Nous Research se combina con los controles de runtime de OpenShell
- Los agentes auto-mejorables de Hermes aprenden de la experiencia, reutilizan workflows exitosos, y operan con mayor privacidad, seguridad e inferencia guardada
- Los datos privados permanecen detras de politicas de runtime
- Las skills aprendidas persisten entre despliegues

**2. Nemotron 3 Ultra + Hermes (Velocidad e Inteligencia)**
- Nemotron 3 Ultra es el modelo mas capaz disponible para Hermes via Nous Portal
- Los usuarios de Hermes pueden acceder **gratis** a Nemotron 3 Ultra a traves del Nous Portal
- Hermes soporta 200+ modelos via OpenRouter, Nous Portal, NVIDIA NIM, OpenAI, o endpoints personalizados

**3. NVIDIA Agent Skills + Hermes (Capacidades)**
- Las skills verificadas de NVIDIA se pueden instalar en Hermes Agent
- Hermes ya tiene un ecosistema de skills propio (HermesHub) con 22+ skills disponibles
- Se planea integracion con Hermes Skillhub para distribucion de skills NVIDIA

### Flujo de Trabajo Integrado

```
Usuario -> Hermes Agent -> NemoClaw/OpenShell (sandbox)
                              |
                    +---------+---------+
                    |                   |
              Privacy Router      Policy Engine
                    |                   |
            +-------+-------+    +------+------+
            |               |    |             |
       Nemotron      Cloud Models  Filesystem  Network
       (local)       (frontier)   Controls    Controls
```

### Relevancia para el Hackathon

Para el hackathon "The Hermes Agent Accelerated Business Hackathon", la integracion NVIDIA permite:

- **Seguridad empresarial** desde el primer dia con NemoClaw/OpenShell
- **Modelos frontier** (Nemotron 3 Ultra) para razonamiento complejo de negocios
- **Skills especializadas** para tareas como optimizacion, analisis de datos, vision, etc.
- **Infraestructura lista** para agentes que ganan, gastan y operan negocios reales

**Fuentes:**
- https://x.com/NousResearch/status/2066921443548348436
- https://x.com/NVIDIAAI/status/2061858457519575280
- https://alphasignal.ai/news/nous-research-s-hermes-agent-can-now-spend-real-money-autonomously
- https://docs.nvidia.com/nemoclaw/user-guide/hermes/get-started/quickstart

---

## 5. Resumen para Arquitectura Multi-Agente de Negocios

### Stack Recomendado para el Hackathon

| Capa | Tecnologia NVIDIA | Funcion |
|---|---|---|
| **Seguridad/Runtime** | NemoClaw + OpenShell | Sandbox, politicas, privacy router, auditoria |
| **Modelo de Orquestacion** | Nemotron 3 Ultra | Razonamiento complejo, planificacion, delegacion |
| **Modelos de Ejecucion** | Nemotron 3 Super (120B) o Nano (4B) | Tareas de alto volumen, sub-agentes especializados |
| **Skills/Capacidades** | NVIDIA Agent Skills | Optimizacion, datos, vision, entrenamiento |
| **Framework de Agente** | Hermes (Nous Research) | Loop de auto-mejora, memoria, skills |
| **Pagos/Operaciones** | Stripe Skills | Compras, provision de SaaS, pagos de servicios |

### Ventajas Competitivas

1. **Seguridad sin sacrificar capacidad**: Los agentes pueden ser tan autonomos como se necesite, con controles de seguridad enterprise
2. **Razonamiento de frontier con costo controlado**: Nemotron 3 Ultra maneja las tareas mas duras a 5x velocidad y 30% menos costo
3. **Ecosistema de skills extensible**: Instalar una skill da al agente capacidades nuevas sin programacion adicional
4. **Privacidad de datos financieros**: El Privacy Router mantiene datos sensibles en infraestructura local
5. **Open-source y sin vendor lock-in**: Pesos abiertos, codigo abierto, despliegue en cualquier GPU

### Premios del Hackathon

- **1er lugar**: $10,000 cash + NVIDIA DGX Spark + $5,000 Stripe Credits
- **2do lugar**: $5,000 cash + NVIDIA DGX Spark + $3,000 Stripe Credits
- **3er lugar**: $2,500 cash + NVIDIA DGX Spark + $1,000 Stripe Credits

Criterios de evaluacion: utilidad, viabilidad y presentacion. Jueces: Nous Research, NVIDIA y Stripe.

---

## Fuentes Principales

| # | Fuente | URL |
|---|---|---|
| 1 | NVIDIA NemoClaw Official | https://www.nvidia.com/en-us/ai/nemoclaw/ |
| 2 | NVIDIA OpenShell Docs | https://docs.nvidia.com/openshell/about/overview |
| 3 | OpenShell GitHub | https://github.com/NVIDIA/openshell |
| 4 | Nemotron 3 Ultra Blog | https://developer.nvidia.com/blog/nvidia-nemotron-3-ultra-powers-faster-more-efficient-reasoning-for-long-running-agents/ |
| 5 | Nemotron 3 Ultra HuggingFace | https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16 |
| 6 | NVIDIA Nemotron Overview | https://developer.nvidia.com/topics/ai/nemotron |
| 7 | NVIDIA Agent Skills Docs | https://docs.nvidia.com/skills |
| 8 | Nous Research Hackathon Tweet | https://x.com/NousResearch/status/2066921443548348436 |
| 9 | NVIDIA AI Hermes Tutorial Tweet | https://x.com/NVIDIAAI/status/2061858457519575280 |
| 10 | Hermes + NemoClaw Quickstart | https://docs.nvidia.com/nemoclaw/user-guide/hermes/get-started/quickstart |
| 11 | Alpha Signal Analysis | https://alphasignal.ai/news/nous-research-s-hermes-agent-can-now-spend-real-money-autonomously |
| 12 | Hermes Agent Skills Docs | https://hermes-agent.nousresearch.com/docs/guides/work-with-skills |
| 13 | OpenRouter Nemotron 3 Ultra | https://openrouter.ai/nvidia/nemotron-3-ultra-550b-a55b |

---

*Documento generado para investigacion tecnica del hackathon. Toda la informacion proviene de fuentes publicas oficiales de NVIDIA, Nous Research y documentacion tecnica.*
