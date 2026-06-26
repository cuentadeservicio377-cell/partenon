# partenon-core

Nucleo de Partenon. Adapta `hermes-business-core` de HBOS para enrutar conversaciones a los 6 perfiles, coordinar handoffs y ejecutar el onboarding general.

## Responsabilidades

- `router.py`: Enruta intenciones del usuario a `partenon-tesorero`, `partenon-mensajero`, `partenon-cobrador`, `partenon-guardian`, `partenon-estratega` o `partenon-diplomatico`.
- `onboarding_engine.py`: Wizard de instalacion que crea archivos de perfil y genera misiones iniciales.
- `workflow_engine.py`: Handoffs entre perfiles y registro de misiones en G-Brain.
- `config/mcp/servers.yaml`: Configuracion de MCP servers (Google Workspace, Stripe, Gmail, G-Brain, etc.).

## Uso

```bash
python -m py_compile partenon-core/tools/*.py
```
