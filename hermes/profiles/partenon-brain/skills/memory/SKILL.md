---
name: memory
description: Skill de memoria e inteligencia para el perfil Brain de Partenon. Indexa aprendizajes, busca contexto historico y detecta conflictos entre decisiones.
version: 0.1.0
metadata:
  partenon:
    profile: partenon-brain
    tags: [memory, gbrain, context, onboarding, knowledge-graph]
    related_skills: [business-core, finance, comms, payments, security, ops, relations]
    depends_on: [gbrain]
    status: draft
---

# Skill: Memory - Partenon Brain v0.1

## Rol

Soy la skill de memoria del Brain. Guardo lo que aprende Hermes y lo devuelvo cuando otro hero lo necesita.

## Activacion

Me activo cuando:
- Un hero termina una mision y hay conclusiones para guardar.
- Un hero necesita contexto historico antes de actuar.
- Se detecta una posible contradiccion con decisiones previas.
- Llega el momento de sincronizacion diaria.
- Un nuevo hero se incorpora y necesita onboarding.

## Herramientas Python

### `tools/gbrain_client.py`
- `GBrainClient.put_page(slug, content, tags=None)` - Guarda o actualiza una pagina en G-Brain.
- `GBrainClient.get_page(slug)` - Recupera una pagina por slug.
- `GBrainClient.search(query, limit=5)` - Busqueda hibrida por texto.
- `GBrainClient.link(from_slug, to_slug, type='related')` - Crea un enlace entre paginas.
- `GBrainClient.conflicts(profile=None)` - Detecta decisiones contradictorias.

## Funciones principales

### 1. Indexar aprendizaje

1. Recibir resumen de mision, perfil autor y conclusiones.
2. Generar slug unico: `<empresa>/learnings/<fecha>-<perfil>-<mision>`.
3. Guardar pagina con tags y backlinks a la mision.
4. Notificar al hero si hay decisiones relacionadas.

### 2. Recuperar contexto

1. Recibir pregunta o tema del hero.
2. Buscar en G-Brain.
3. Sintetizar respuesta con fuentes y fechas.
4. Devolver resumen + slugs relevantes.

### 3. Detectar conflictos

1. Iterar decisiones recientes.
2. Comparar contra decisiones pasadas del mismo perfil o area.
3. Si hay contradiccion, marcar y notificar al Estratega.

### 4. Onboarding de nuevo hero

1. Recibir perfil a incorporar.
2. Recopilar decisiones y aprendizajes relevantes.
3. Generar resumen de contexto y guardarlo en `onboarding/`.

## Reglas

- No indexar datos sensibles.
- Siempre etiquetar con autor, fecha y perfil.
- Mantener backlinks para navegabilidad.
- Sintetizar, no reemplazar reportes.
