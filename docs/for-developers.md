# Partenon para Developers

> Documentación técnica para instalar, extender y contribuir a Partenon.

## Repositorio

- **Web**: [https://hermespartenon.online/](https://hermespartenon.online/)
- **Código**: [https://github.com/cuentadeservicio377-cell/partenon](https://github.com/cuentadeservicio377-cell/partenon)

## Stack

- **Frontend páginas**: HTML estático + Tailwind CSS CDN + JS vanilla (`web/`)
- **Dashboard**: Next.js 15 + React 19 + TypeScript + Tailwind CSS (`dashboard/`)
- **Agent core**: Hermes Agent (Nous Research) + Python skills + `partenon-core` (`partenon-core/`)
- **Perfiles**: 7 distribuciones de Hermes Agent (`hermes/profiles/`)
- **Sandbox / orquestación**: NVIDIA NemoClaw + OpenShell (alpha / early preview)
- **Modelos**: NVIDIA Nemotron 3 Ultra / Super, OpenAI, Kimi / Moonshot
- **Documentos**: Python + WeasyPrint (Kami v3)
- **Datos**: Google Workspace (Sheets, Docs, Slides, Drive, Calendar, Gmail)
- **Pagos**: Stripe API + Stripe Skills de Hermes (`stripe-link-cli`, `mpp-agent`, `stripe-projects`)
- **Memoria**: G-Brain de Garry Tan vía MCP
- **Infraestructura**: Docker / Docker Compose

## Arquitectura

```text
┌─────────────────────────────────────────────────────────────┐
│                         Hermes (empresa)                    │
└──────────────────────┬──────────────────────────────────────┘
                       │ publica misiones
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                      partenon-core                            │
│  onboarding → router → workflow → eval loop → G-Brain         │
└──────────────────────┬──────────────────────────────────────┘
                       │ asigna misiones
                       ▼
┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
│ Scribe  │ Herald  │Collector│ Guardian│Strategist│Diplomat│ Brain   │
│ (finance)│(comms) │(payments│(security│  (ops)   │(relations)│(memory)│
└────┬────┴────┬────┴────┬────┴────┬────┴────┬────┴────┬────┴────┬────┘
     │         │         │         │         │         │         │
     ▼         ▼         ▼         ▼         ▼         ▼         ▼
Google    Google    Stripe    NVIDIA    Google    Google    G-Brain
Sheets    Docs/     API       NemoClaw  Calendar  Contacts  (MCP)
          Slides                      /Gmail
```

## Estructura del repositorio

```text
partenon/
├── web/                    # Páginas web estáticas
│   ├── index.html          # Marketing
│   ├── heroes.html         # Perfiles de héroes
│   └── developers.html     # Documentación técnica
├── dashboard/              # Dashboard de operaciones (Next.js)
├── hermes/profiles/        # Perfiles de Hermes Agent
│   ├── partenon-tesorero/
│   ├── partenon-mensajero/
│   ├── partenon-cobrador/
│   ├── partenon-guardian/
│   ├── partenon-estratega/
│   ├── partenon-diplomatico/
│   └── partenon-brain/
├── partenon-core/          # Core skill: onboarding, router, workflow
├── scripts/                # Utilidades y demos
│   ├── demo_tesorero.py
│   └── setup_hermes.py
├── templates/              # Plantillas de Google Sheets
├── docs/                   # Documentación
├── install.sh              # Instalador bash
├── .env.example            # Variables de entorno
├── requirements.txt
└── docker-compose.yml
```

## Instalación rápida

### Opción A: Bash

```bash
git clone https://github.com/cuentadeservicio377-cell/partenon.git
cd partenon
./install.sh
```

### Opción B: Python

```bash
git clone https://github.com/cuentadeservicio377-cell/partenon.git
cd partenon
python scripts/setup_hermes.py
```

### Variables de entorno

Copia `.env.example` a `.env` y completa:

```bash
cp .env.example .env
```

Campos obligatorios para empezar:
- `OPENROUTER_API_KEY`
- `GOOGLE_SERVICE_ACCOUNT_JSON`
- `STRIPE_SECRET_KEY` (solo si usas Cobrador)
- `GBRAIN_DATABASE_URL` (solo si usas Brain)

## Perfiles técnicos

Cada perfil es una distribución de Hermes Agent con:

- `SOUL.md` — personalidad, rol, reglas y límites.
- `config.yaml` — modelo default, tools habilitadas, MCP servers.
- `.env.example` — variables de entorno del perfil.
- `skills/<skill>/SKILL.md` — documentación de la skill.
- `skills/<skill>/tools/*.py` — herramientas Python.
- `cron/*.json` — tareas programadas.
- `templates/` — plantillas de configuración.

### Modelos

| Perfil | Default | Fallback |
|--------|---------|----------|
| Tesorero | `openrouter/anthropic/claude-opus-4` | `openrouter/anthropic/claude-sonnet-4` |
| Mensajero | `openrouter/anthropic/claude-opus-4` | `openrouter/anthropic/claude-sonnet-4` |
| Cobrador | `openrouter/anthropic/claude-opus-4` | `openrouter/anthropic/claude-sonnet-4` |
| Guardian | `openrouter/anthropic/claude-opus-4` | `openrouter/anthropic/claude-sonnet-4` |
| Estratega | `openrouter/anthropic/claude-opus-4` | `openrouter/anthropic/claude-sonnet-4` |
| Diplomático | `openrouter/anthropic/claude-opus-4` | `openrouter/anthropic/claude-sonnet-4` |
| Brain | `openrouter/anthropic/claude-opus-4` | `openrouter/anthropic/claude-sonnet-4` |

### MCP servers

- `google_workspace`: acceso a Sheets, Docs, Slides, Calendar, Gmail.
- `gbrain`: servidor MCP de memoria persistente.
- `stripe`: operaciones de pagos (vía Stripe Skills de Hermes).

## Demo

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/demo_tesorero.py
```

Esto genera:
- `data/sample_gastos.xlsx`
- `data/sample_gastos_report.json`

## Dashboard

```bash
cd dashboard
npm install
npm run dev
```

Abre http://localhost:3000. Credenciales default: `admin` / `partenon`.

## Build de producción

```bash
cd dashboard
npm run build
```

## Docker

```bash
docker-compose up --build
```

## API Reference

### CLI de Hermes

```bash
hermes profile use partenon-tesorero
hermes profile use partenon-mensajero
hermes run "Registra un gasto de $500 en publicidad"
```

### G-Brain MCP

Métodos expuestos por el servidor MCP `gbrain`:

| Método | Descripción |
|--------|-------------|
| `put_page` | Guarda o actualiza una página de memoria. |
| `get_page` | Recupera una página por slug. |
| `search_pages` | Búsqueda híbrida por texto. |
| `query_pages` | Query semántico. |
| `graph_query` | Búsqueda en grafo de relaciones. |

## Workshop de 90 minutos

1. **Pre-instalación** (15 min): Python, Node.js, cuentas de Google Workspace y Stripe.
2. **Setup** (20 min): `git clone`, `./install.sh`, configurar `.env`.
3. **Práctica** (40 min): demo del Tesorero, Mensajero y Cobrador.
4. **Q&A y roadmap** (15 min).

## Contribuir

1. Fork el repositorio.
2. Crea una rama: `git checkout -b feat/nombre-feature`.
3. Haz commit con mensaje descriptivo.
4. Abre un PR con evidencia de tests/build.

## Roadmap

- [ ] Eval loop funcional en todos los perfiles.
- [ ] Integraciones live de Google Workspace, Stripe y G-Brain.
- [ ] Validación end-to-end con 10 empresas piloto.
- [ ] Marketplace de perfiles especializados.
