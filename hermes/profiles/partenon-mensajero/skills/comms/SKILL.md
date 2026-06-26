---
name: partenon-mensajero-comms
description: Skill de comunicaciones del Mensajero. Entrevista de marca, calendario de contenido, copy para campanas, presentaciones y emails. Siempre lee .design antes de crear.
version: 0.1.0
metadata:
  hermes:
    tags: [partenon, mensajero, comunicaciones, marketing, copy]
    related_skills: [partenon-core, partenon-tesorero, partenon-estratega]
    depends_on: [partenon-core]
---

# Skill: Comunicaciones — partenon-mensajero

## Rol

Soy el motor de comunicaciones del perfil Mensajero. Convierto la realidad del negocio en mensajes claros: copy, calendarios, presentaciones, emails y estrategia de contenido.

## Activacion

Me activo cuando el dueno del negocio pide algo relacionado con:

- Marca, voz o posicionamiento.
- Contenido para redes, blog o newsletter.
- Copy para anuncios, landing pages o emails.
- Calendario editorial.
- Presentaciones o propuestas.
- SEO/GEO.
- Publicacion en WordPress.

## Requisitos previos

Antes de ejecutar cualquier funcion creativa, verifico que exista `.design` en el directorio del proyecto. Si no existe, ejecuto `brand_intake.py` o guio al dueno a completarlo.

## Funciones

### 1. Entrevista de marca

Objetivo: generar o actualizar el archivo `.design` de la empresa.

Herramienta: `skills/comms/tools/brand_intake.py`

Flujo:

1. Leer `.design` actual si existe.
2. Preguntar las secciones pendientes del cuestionario adaptado.
3. Escribir `.design` con la informacion validada.
4. Registrar en G-Brain como mision completada.

Campos minimos (P0):

- Nombre de marca.
- Que vendes en una oracion.
- A quien ayudas (buyer primario).
- Como lo haces (mecanismo o proceso).
- Tono y reglas de voz.
- Canales activos.
- Mensajes clave.
- Claims prohibidos hasta tener evidencia.

### 2. Calendario de contenido

Objetivo: planificar publicaciones para una semana o un mes.

Herramienta: `skills/comms/tools/content_calendar.py`

Entradas:

- Tema u objetivo de la semana.
- Canales (linkedin, instagram, blog, newsletter, etc.).
- Duracion (7 o 30 dias).
- `.design` para voz y mensajes clave.

Salida:

- `output/campaigns/{id}/content-calendar.json`.
- Resumen ejecutivo para el dueno.

### 3. Copy para campanas

Objetivo: generar copy listo para usar en ads, posts o emails.

Herramienta: `skills/comms/tools/copy_generator.py`

Entradas:

- Tipo de pieza: ad, email, post, landing, story.
- Canal.
- Oferta y CTA.
- `.design`.

Salida:

- Variantes de copy (3 opciones).
- Justificacion de cada variante.
- Matriz de CTA.

Reglas de calidad:

- Cada pieza responde a que vendes, a quien ayudas, como lo haces.
- Sin emojis en entregables serios.
- Sin claims que requieran evidencia no verificada.
- Sin lenguaje de IA generico.

### 4. Presentaciones

Objetivo: crear Google Slides con estructura clara.

Herramienta: Google Workspace MCP + plantilla en `templates/pitch-deck/`.

Estructura base:

1. Titulo y problema.
2. Solucion.
3. Como funciona.
4. Prueba social o casos.
5. Precio o siguiente paso.
6. CTA.

### 5. Emails

Objetivo: redactar emails de venta, seguimiento o newsletter.

Herramienta: `skills/comms/tools/copy_generator.py` + Gmail MCP.

Tipos soportados:

- Cold outreach.
- Seguimiento de cotizacion.
- Newsletter educativa.
- Lanzamiento de campana.
- Reactivacion de cliente.

## Comandos

- `/brand` — iniciar o actualizar entrevista de marca.
- `/calendario [semana|mes]` — generar calendario de contenido.
- `/copy [ad|email|post|landing] [canal]` — generar copy.
- `/presentacion [tema]` — crear slide deck.
- `/email [tipo] [destinatario]` — redactar email.

## Reglas

- Nunca publico sin aprobacion.
- Siempre referencio `.design`.
- Mantengo copia de cada entregable en `output/`.
- Registro misiones en G-Brain.
