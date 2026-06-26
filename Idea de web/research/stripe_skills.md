# Stripe Skills for Hermes - Resumen de Integraciones para Agentes de IA

> **Hackathon:** The Hermes Agent Accelerated Business Hackathon  
> **Presentado por:** Nous Research x NVIDIA x Stripe  
> **Fecha:** Junio 2026  
> **Investigacion:** Julio 2025

---

## 1. Que son Stripe Skills for Hermes

**Stripe Skills for Hermes** son un conjunto de tres skills (habilidades) opcionales que integran las capacidades de pago y aprovisionamiento de Stripe directamente en el agente de IA Hermes de Nous Research. Estas skills permiten que el agente opere de forma autonoma en la economia real: comprar productos, pagar por APIs, provisionar servicios SaaS y gestionar suscripciones, todo con controles de seguridad configurables y aprobacion humana cuando sea necesario.

Cada skill es modular e independiente. Se instalan via CLI con `hermes skills install official/payments/<skill>` y estan disponibles para Linux y macOS. Las tres skills son: **`stripe-link-cli`** (compras en la web via tarjetas virtuales de un solo uso), **`mpp-agent`** (pagos programaticos a APIs que usan HTTP 402 / Machine Payments Protocol), y **`stripe-projects`** (aprovisionamiento autonomo de infraestructura SaaS como bases de datos, hosting, telefonia, etc.). La combinacion de estas tres skills transforma a Hermes de un asistente conversacional a un "agente de negocios" capaz de ejecutar operaciones financieras y tecnicas de forma autonoma.

---

## 2. Las 3 Stripe Skills Desglosadas

### 2.1 stripe-link-cli - Compras en la Web

Permite a Hermes realizar compras en sitios web reales usando **tarjetas virtuales de un solo uso** emitidas via Stripe Link. El agente nunca accede a las credenciales de pago reales del usuario.

**Flujo de trabajo:**
1. El usuario pide: "Compra un dominio .com por menos de $15"
2. Hermes evalua el comercio y crea una "spend request"
3. El usuario aprueba la compra en la app de Link (iOS/Android/web)
4. Se genera una tarjeta virtual de un solo uso
5. Hermes completa el checkout y limpia las credenciales

**Cobertura:** US-only (requiere cuenta Link). Soporta tarjetas virtuales (card) y Shared Payment Tokens (SPT) para comercios con MPP.

**Instalacion:**
```bash
hermes skills install official/payments/stripe-link-cli
npm install -g @stripe/link-cli
```

**Fuente:** [https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/payments/payments-stripe-link-cli](https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/payments/payments-stripe-link-cli)

---

### 2.2 mpp-agent - Pagos Programaticos (Pay-per-Call)

Permite a Hermes pagar por APIs y servicios que usan el **Machine Payments Protocol (MPP)**, respondiendo a codigos HTTP 402 "Payment Required". Ideal para APIs de pago por uso, llamadas a modelos de IA, y microtransacciones.

**Como funciona:**
1. Hermes hace una peticion a una API protegida
2. El servidor responde con HTTP 402 + header `WWW-Authenticate: Payment`
3. La skill decodifica el challenge, crea un spend request y obtiene un Shared Payment Token (SPT)
4. Hermes reintenta la peticion con el SPT incluido
5. El servidor verifica el pago y entrega el recurso

**Cobertura:** Global. No requiere cuenta Link. Funciona con cualquier servicio que implemente MPP.

**Instalacion:**
```bash
hermes skills install official/payments/mpp-agent
```

**Ejemplo de uso:** "Hazme 10 llamadas a la API de traduccion" - el agente pagara automaticamente cada llamada HTTP 402.

**Fuente:** [https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/payments/payments-mpp-agent](https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/payments/payments-mpp-agent)

---

### 2.3 stripe-projects - Aprovisionamiento de SaaS

Permite a Hermes **provisionar infraestructura y servicios SaaS de forma autonoma**: crear bases de datos, configurar numeros de telefono, desplegar en hosting, etc. Usa el CLI de Stripe Projects para gestionar 49+ proveedores desde un solo lugar.

**Proveedores soportados (49+):**
- **Bases de datos:** Neon (Postgres), Redis, MongoDB, ClickHouse
- **Hosting/VPS:** Vercel, DigitalOcean, AWS
- **Comunicaciones:** Twilio (SMS/voz)
- **Observabilidad:** ClickHouse para LLM observability
- **Facturacion:** Metronome (usage-based billing de Stripe)
- **E-commerce:** Wix para storefronts

**Flujo:**
1. Usuario dice: "Crea una base de datos Postgres para este proyecto"
2. Hermes usa `stripe projects provision` para crear el recurso
3. Las credenciales se sincronizan automaticamente al `.env` del proyecto
4. La facturacion se centraliza en Stripe

**Instalacion:**
```bash
hermes skills install official/payments/stripe-projects
# Requiere: Stripe CLI + Stripe Projects plugin
```

**Fuente:** [https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/payments/payments-stripe-projects](https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/payments/payments-stripe-projects)

---

## 3. APIs y Herramientas Relevantes de Stripe para Agentes

### 3.1 Stripe Agent Toolkit
SDK oficial (Python y TypeScript) que expone las APIs de Stripe como **funciones llamables por agentes** via function calling. Soporta:

| Framework | Soporte |
|-----------|---------|
| OpenAI Agents SDK | ✅ Nativo |
| LangChain | ✅ Nativo |
| CrewAI | ✅ Nativo |
| Vercel AI SDK | ✅ Nativo |
| MCP (Model Context Protocol) | ✅ Nativo |

**Acciones disponibles:** Crear cobros (PaymentIntents), enviar facturas, gestionar suscripciones, crear productos/precios, emitir reembolsos, consultar balances, y mas.

**Instalacion:**
```bash
pip install stripe-agent-toolkit      # Python
npm install @stripe/agent-toolkit     # TypeScript
```

**Fuente:** [https://github.com/stripe/ai](https://github.com/stripe/ai)

### 3.2 Machine Payments Protocol (MPP)
Protocolo abierto co-autorado por Stripe y Tempo para **pagos maquina-a-maquina**. Estandariza el uso del codigo HTTP 402 "Payment Required" para que agentes paguen programaticamente por recursos, APIs y servicios.

**Caracteristicas:**
- **Dos modos de pago:** `charge` (pago unico inmediato) y `session` (pago por flujo/streaming)
- **Multi-metodo:** Soporta stablecoins (USDC en Tempo blockchain), tarjetas via Stripe, Bitcoin Lightning
- **Settle en <1 segundo** via Tempo blockchain
- **Costo objetivo:** $0.001 por transaccion

**Fuente:** [https://stripe.com/blog/machine-payments-protocol](https://stripe.com/blog/machine-payments-protocol)

### 3.3 Issuing for Agents
Permite emitir **tarjetas virtuales con controles programaticos** para que agentes gasten de forma autonoma.

**Capacidades:**
- **Tarjetas de un solo uso:** Se invalidan automaticamente despues de la primera transaccion
- **Controles de gasto:** Limites por transaccion/mes, categorias de comercio permitidas
- **Autorizacion en tiempo real:** Webhooks para aprobar/declinar cada transaccion
- **Visibilidad completa:** Track de todas las transacciones con metadatos del agente
- **Fraud signals:** Scores de riesgo ML en cada autorizacion

```bash
# Ejemplo: Crear tarjeta virtual para un agente
curl https://api.stripe.com/v1/issuing/cards \
  -u "sk_..." \
  -d cardholder=ich_123 \
  -d currency=usd \
  -d type=virtual \
  -d status=active \
  -d "spending_controls[allowed_categories][]"=computer_software_stores \
  -d "spending_controls[spending_limits][0][amount]"=50000 \
  -d "spending_controls[spending_limits][0][interval]"=monthly
```

**Fuente:** [https://docs.stripe.com/issuing/agents](https://docs.stripe.com/issuing/agents)

### 3.4 Stripe Projects
Plataforma para **aprovisionar y gestionar servicios SaaS desde el CLI**. Conecta con 49 proveedores y centraliza billing, credenciales y costos.

**Comandos clave:**
```bash
stripe projects init                    # Inicializar proyecto
stripe projects providers list          # Ver proveedores disponibles
stripe projects provision neon          # Crear base de datos
stripe projects link twilio             # Conectar servicio existente
stripe projects cost                    # Ver costos por proyecto
```

**Controles de seguridad:** Limites de gasto por proveedor, entornos aislados (dev/staging/prod), y credenciales scoped por entorno.

**Fuente:** [https://stripe.com/blog/stripe-projects-adds-new-agents-providers-developer-controls](https://stripe.com/blog/stripe-projects-adds-new-agents-providers-developer-controls)

### 3.5 Link Wallet for Agents
Wallet que permite a los agentes acceder programaticamente a los metodos de pago guardados en Link (200M+ consumidores). Emite tarjetas de un solo uso o SPT sin exponer credenciales reales.

**Fuente:** [https://stripe.com/blog/giving-agents-the-ability-to-pay](https://stripe.com/blog/giving-agents-the-ability-to-pay)

---

## 4. Casos de Uso para Negocios

### 4.1 Cobrar Pagos (Agente como Vendedor)
| Caso | Como funciona |
|------|---------------|
| **E-commerce autonomo** | El agente crea productos en Stripe, genera Payment Links y procesa checkout para clientes |
| **SaaS con billing por uso** | Usa Stripe Billing + Metronome para medir consumo (tokens, API calls) y facturar automaticamente |
| **Facturacion recorrente** | Crea y gestiona suscripciones, envia invoices, procesa pagos fallidos |
| **Agentes de cobranza** | Identifica pagos pendientes, envia recordatorios, procesa reembolsos |

**APIs clave:** PaymentIntents, Billing/Subscriptions, Invoicing, Payment Links

### 4.2 Gestion de Suscripciones
| Caso | Como funciona |
|------|---------------|
| **Onboarding autonomo** | El agente crea el customer, asocia el metodo de pago, y activa la suscripcion |
| **Upsells/downgrades** | Detecta cambios de uso y propone/modifica planes automaticamente |
| **Retention** | Identifica churn risk y ofrece descuentos o pausas de suscripcion |
| **Usage-based billing** | Monitorea consumo en tiempo real y ajusta facturacion con Metronome |

### 4.3 Pagar por Servicios (Agente como Comprador)
| Caso | Como funciona |
|------|---------------|
| **Compras web** | Usa `stripe-link-cli` para comprar productos, reservar servicios, contratar freelancers |
| **APIs de pago por uso** | Usa `mpp-agent` para pagar llamadas a APIs (traduccion, modelos LLM, datos) |
| **Gastos operativos** | Emite tarjetas virtuales scoped para categorias especificas (cloud, software, viajes) |
| **Compras recurrentes** | Configura pagos automaticos para suscripciones a herramientas SaaS |

### 4.4 Provisionar SaaS (Agente como DevOps)
| Caso | Como funciona |
|------|---------------|
| **Despliegue completo** | "Crea una app web con Next.js en Vercel + Postgres en Neon + Auth en Clerk" - todo autonomo |
| **Escalamiento** | Detecta carga alta y provisiona recursos adicionales automaticamente |
| **Rotacion de credenciales** | Gestiona API keys, las rota periodicamente y sincroniza al `.env` |
| **Monitoreo** | Configura ClickHouse para observabilidad de LLM costos, latencia y calidad |

### 4.5 Casos del Hackathon Hermes
El hackathon busca agentes que puedan:
- **Ganar dinero:** Crear servicios que cobren por uso o suscripcion
- **Gastar dinero:** Comprar recursos necesarios para operar
- **Operar a cualquier escala:** Provisionar su propia infraestructura sin intervencion humana

---

## 5. Seguridad y Permisos

### 5.1 Principios de Seguridad
Stripe aplica una filosofia de **"seguridad por diseño"** en todas las interacciones con agentes:

| Principio | Implementacion |
|-----------|---------------|
| **Nunca exponer credenciales reales** | El agente recibe tarjetas virtuales de un solo uso o tokens scoped, nunca el PAN real |
| **Aprobacion humana obligatoria** | Cada compra via Link requiere aprobacion en la app del usuario |
| **Principio de minimo privilegio** | API keys restringidas (`rk_*`) con permisos granulares |
| **Aislamiento de entornos** | Dev/staging/prod separados; el agente defaultea a dev |
| **Auditoria completa** | Cada transaccion trazable con metadatos del agente, tarea y orden |

### 5.2 Controles Programaticos

**Issuing for Agents:**
- Limites de gasto por transaccion, mensual, o por intervalo personalizado
- Categorias de comercio permitidas/bloqueadas (MCC codes)
- Tarjetas de un solo uso con invalidacion automatica
- Congelamiento de tarjetas via API en tiempo real
- Webhooks de autorizacion con timeout de 2 segundos

**Stripe Projects:**
- Limites de gasto **por proveedor** (ej: max $100/mes en AI models, $500/mes en hosting)
- Entornos nombrados con credenciales aisladas
- Vista unificada de costos por proyecto
- Default a entorno `development` para prevenir accidentes en produccion

**Link Wallet:**
- Aprobacion in-app para cada spend request
- Tarjetas de un solo uso (PAN se elimina tras el checkout)
- Scope limitado a comercio, monto y tiempo especificos
- Revocacion instantanea de SPTs

### 5.3 Mejores Practicas Recomendadas

1. **Usar Restricted API Keys (RAK)** con permisos minimos necesarios
2. **Ejecutar en test mode** durante desarrollo y evaluacion
3. **Configurar webhooks** para monitoreo de transacciones en tiempo real
4. **Implementar limites de gasto** tanto en Stripe como en la capa de aplicacion
5. **Separar logs** de transacciones iniciadas por agentes vs humanos
6. **Dar a los usuarios** un dashboard para revisar y revocar acceso de agentes
7. **Usar idempotency keys** para prevenir pagos duplicados
8. **Auditar periodicamente** transacciones con metadatos del agente

### 5.4 Compliance
- **PCI DSS Level 1** compliant
- **SOC 1 y SOC 2** certified
- **KYC/AML** integrado en el flujo de onboarding
- Transacciones heredan reportes regulatorios automaticos

---

## 6. El Hackathon: The Hermes Agent Accelerated Business Hackathon

### Premios
| Puesto | Premio |
|--------|--------|
| 1er lugar | $10,000 cash + NVIDIA DGX Spark + $5,000 Stripe Credits |
| 2do lugar | $5,000 cash + NVIDIA DGX Spark + $3,000 Stripe Credits |
| 3er lugar | $2,500 cash + NVIDIA DGX Spark + $1,000 Stripe Credits |

### Integraciones NVIDIA
- **NemoClaw:** Ejecutar agentes de forma segura
- **Nemotron 3 Ultra:** Modelo LLM de alta velocidad
- **Agent Skills:** Acceso a skills extensos del ecosistema NVIDIA

### Criterios de Evaluacion
- **Utilidad:** Que tan util es el agente para un negocio real
- **Viabilidad:** Que tan factible es operar a escala
- **Presentacion:** Calidad del demo video (1-3 minutos)

### Participacion
1. Tweetear un video demo de 1-3 minutos taggeando @NousResearch
2. Enviar el link al canal de submissions en Discord
3. Completar el formulario de submission

**Fuente:** [https://x.com/NousResearch/status/2066921443548348436](https://x.com/NousResearch/status/2066921443548348436)

---

## 7. Datos Relevantes: El Auge del Trafico de Agentes

- El trafico de agentes supero al trafico humano en internet por primera vez en junio 2026
- El trafico de agentes a la documentacion de Stripe crecio **10x en 2025** y representa ~40% del total
- **70% de las peticiones** al Stripe CLI provienen de agentes
- Los agentes son capaces de escribir codigo e integrar APIs de forma independiente

---

## 8. URLs de Fuentes

### Documentacion Oficial
- **Stripe Skills for Hermes (catalogo):** https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog
- **stripe-link-cli skill:** https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/payments/payments-stripe-link-cli
- **mpp-agent skill:** https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/payments/payments-mpp-agent
- **stripe-projects skill:** https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/payments/payments-stripe-projects

### Stripe Oficial
- **Stripe Agent Toolkit (GitHub):** https://github.com/stripe/ai
- **Issuing for Agents:** https://docs.stripe.com/issuing/agents
- **Machine Payments Protocol:** https://stripe.com/blog/machine-payments-protocol
- **MPP Docs:** https://docs.stripe.com/payments/machine/mpp
- **Giving Agents the Ability to Pay:** https://stripe.com/blog/giving-agents-the-ability-to-pay
- **Stripe Projects + Agent Integrations:** https://stripe.com/blog/stripe-projects-adds-new-agents-providers-developer-controls
- **Stripe Agent Toolkit Blog:** https://stripe.dev/blog/adding-payments-to-your-agentic-workflows

### Hackathon
- **Anuncio del Hackathon:** https://x.com/NousResearch/status/2066921443548348436
- **Hermes Agent GitHub:** https://github.com/nousresearch/hermes-agent
- **Stripe Link CLI GitHub:** https://github.com/stripe/link-cli

### Protocolos y Estandares
- **Machine Payments Protocol (MPP):** https://mpp.dev/
- **Tempo Blockchain:** https://tempo.xyz/
- **Stripe Sessions 2026 - Machine Payments:** https://stripe.com/sessions/2026/machine-payments-and-the

---

*Documento generado para investigacion tecnica - Julio 2025*
