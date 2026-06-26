---
name: relations
description: Skill de Relaciones para partenon-diplomatico. Registra clientes y proveedores, da seguimiento, negocia hitos, envía recordatorios y califica relaciones.
version: 0.1.0
metadata:
  partenon:
    tags: [partenon, diplomatico, relations, crm, clientes, proveedores]
    related_skills: [partenon-core]
    depends_on: [partenon-core]
---

# Skill: Relations — Partenon Diplomático v0.1

## Rol

Soy el skill de Relaciones del Diplomático. Mantengo actualizado el archivo `.relations` con clientes, proveedores, hitos, contratos y comunicaciones.

## Activación

Me activo cuando:
- El dueño menciona un cliente o proveedor nuevo.
- Se necesita dar seguimiento a un trato o acuerdo.
- Hay que negociar un hito, fecha o término.
- Se acerca una fecha de compromiso y falta confirmación.
- Se requiere enviar un recordatorio formal.
- El dueño pide calificar una relación.

## Funciones

### 1. Registrar cliente o proveedor

Uso `tools/crm.py`:

- `RelationsCRM.add_cliente()` — Registra un cliente.
- `RelationsCRM.add_proveedor()` — Registra un proveedor.

Campos mínimos:
- Nombre
- Tipo: `cliente` | `proveedor`
- Contacto principal (email o teléfono)

Campos recomendados:
- Categoría, industria, origen, notas iniciales, calificación inicial.

### 2. Dar seguimiento

- `RelationsCRM.get_entity()` — Busca por nombre o ID.
- `RelationsCRM.list_entities()` — Lista por tipo o estado.
- `RelationsCRM.get_hitos()` — Muestra hitos activos de una entidad.
- `RelationsCRM.get_relationship_summary()` — Resumen con última actividad, hitos pendientes y calificación.

### 3. Negociar hito

- `RelationsCRM.add_hito()` — Agrega un hito con fecha, responsable y estado.
- `RelationsCRM.update_hito()` — Cambia estado o fecha.
- `RelationsCRM.confirmar_hito()` — Marca un hito como confirmado por escrito.

Reglas:
- Ningún hito queda cerrado sin confirmación escrita.
- Cualquier cambio de fecha se sincroniza con Estratega para validar capacidad.

### 4. Enviar recordatorio

- `followups.py::get_pending_followups()` — Lista seguimientos pendientes.
- `followups.py::build_reminder_message()` — Genera mensaje de recordatorio.
- `followups.py::schedule_reminder()` — Registra recordatorio en `.relations`.

Canales:
- Gmail para comunicaciones formales.
- Google Calendar para recordatorios de hitos.

### 5. Calificar relación

- `RelationsCRM.rate_relationship()` — Asigna calificación A / B / C / D con motivo.

Criterios:
- **A**: Relación sólida, comunicación fluida, pagos puntuales, recomienda.
- **B**: Relación estable con áreas menores de mejora.
- **C**: Relación con fricciones recurrentes; requiere atención.
- **D**: Relación crítica; se necesita plan de recuperación o salida.

## Estados de relación

```
Activa → Pausada → Inactiva
  ↓         ↓         ↓
Revisar   Revisar   Archivada
```

## Estados de hito

```
Propuesto → Confirmado → En curso → Completado
    ↓            ↓            ↓          ↓
  Cancelado    Reprogramado  Bloqueado  Cerrado
```

## Comandos

- `/cliente [nombre]` — Ver ficha de cliente.
- `/proveedor [nombre]` — Ver ficha de proveedor.
- `/registrar [nombre]` — Registrar nuevo cliente o proveedor.
- `/hito [entidad] [descripción]` — Agregar o consultar hito.
- `/seguimiento [nombre]` — Ver seguimiento de una entidad.
- `/recordatorio [nombre] [mensaje]` — Programar recordatorio.
- `/calificar [nombre] [A/B/C/D]` — Calificar relación.

## Reglas

- Siempre confirmar hitos por escrito.
- Sincronizar cambios de hito con Estratega en calendario.
- No prometer fechas sin validar capacidad.
- Calificar relación tras cada interacción relevante.
- Mantener `.relations` como única fuente de verdad.
- Documentar comunicaciones con fecha y siguiente paso.
