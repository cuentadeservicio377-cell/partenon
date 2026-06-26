# Nous Research - Analisis de Estetica Visual, Tono y Patrones de Diseno

> Investigacion realizada para inspirar la landing page de "Hermes Parthenon"
> Fecha: Julio 2026

---

## 1. RESUMEN EJECUTIVO: EL "LOOK AND FEEL" DE NOUS RESEARCH

Nous Research ha construido una identidad visual unica en el ecosistema de IA open source. Su estetica se puede resumir como:

**"Academic Cyberpunk meets Classical Mythology"** -- una fusion deliberada entre:
- La estetica cruda de terminal/computadora retro (tipografia monoespaciada, metadatos tipo "OUTPUT/SEED")
- Referencias a la mitologia clasica griega (Hermes, Psyche, Atropos, Nomos)
- Cultura visual japonesa (anime/manga como "The Nous Girl")
- Un compromiso inquebrantable con el open source y la comunidad

No es limpio ni corporativo como OpenAI o Anthropic. Es **raw, autentico, nerd y orgulloso de serlo**.

---

## 2. PALETA DE COLORES

### 2.1 Colores Principales (Nous Research - Home Page)

| Uso | Color Aproximado | Hex (Estimado) | Observacion |
|-----|-----------------|----------------|-------------|
| **Texto primario** | Teal/Cyan oscuro | `#006B8F` | Usado para todo el texto en la home |
| **Fondo** | Blanco puro | `#FFFFFF` | Fondo limpio, minimalista |
| **Acento/Links** | Azul teal | `#007BA7` | Hover states, enlaces |
| **Separadores** | Teal claro (dashed) | `#5BA4B4` | Lineas punteadas entre secciones |
| **Iconos** | Teal medio | `#4A90A4` | Iconos Unicode decorativos |

### 2.2 Colores Principales (Hermes Agent Page)

| Uso | Color Aproximado | Hex (Estimado) | Observacion |
|-----|-----------------|----------------|-------------|
| **Fondo principal** | Azul electrico/cobalto intenso | `#0000EE` | Fondo DOMINANTE, muy atrevido |
| **Texto sobre fondo azul** | Blanco puro | `#FFFFFF` | Alto contraste |
| **Texto secundario** | Blanco translucido | `rgba(255,255,255,0.8)` | Para subtitulos |
| **Fondo de bloques UI** | Blanco | `#FFFFFF` | Bloques de codigo, botones |
| **Texto en bloques UI** | Negro/Azul oscuro | `#000033` | Codigo, texto de terminal |
| **Borde de bloques** | Gris claro | `#E0E0E0` | Separacion sutil |

### 2.3 Paleta Extendida (de la tienda y branding)

| Uso | Color Aproximado | Hex (Estimado) |
|-----|-----------------|----------------|
| **Azul merch (serigrafia)** | Azul cobalto | `#0047AB` |
| **Fondo crema (shop)** | Blanco roto | `#F5F5F0` |
| **Negro (productos)** | Negro puro | `#000000` |
| **Blanco (sol/logo)** | Blanco puro | `#FFFFFF` |

### 2.4 Patron de Uso de Color

- **Pagina corporativa (home)**: Fondo blanco + texto teal/azul. Limpio, academico, distante.
- **Pagina de producto (Hermes Agent)**: Fondo azul electrico intenso + texto blanco. Atrevido, impactante, memorable.
- **Portal**: Blanco con acentos azules suaves. Funcional, minimalista.
- **Tienda**: Blanco roto/crema con azul cobalto. Streetwear, cultural.

**Clave**: El cambio drastico de blanco->azul entre la home y la pagina de Hermes Agent crea una experiencia inmersiva. No es un gradiente sutil; es un cambio de mundo.

---

## 3. TIPOGRAFIA

### 3.1 Fuentes Oficiales (del Branding Booklet)

| Rol | Fuente | Estilo | Uso |
|-----|--------|--------|-----|
| **Primaria corporativa** | **Courier Pro Bold** | Monoespaciada, bold | Logo "NOUS RESEARCH", headlines tecnicos |
| **Primaria corporativa (light)** | **Courier Pro Regular** | Monoespaciada, regular | Cuerpo de texto, descripciones |
| **Display/Headlines** | **Courier (variante display)** | Monoespaciada, condensada | Titulos grandes en releases, titulos de seccion |

### 3.2 Fuentes en la Web

| Pagina | Fuente de Headlines | Fuente de Body | Observacion |
|--------|-------------------|----------------|-------------|
| **nousresearch.com (home)** | Monoespaciada (Courier-like) | Monoespaciada | Todo en mono, estilo terminal |
| **hermes-agent.nousresearch.com** | Serif elegante (Times/Didot-like) | Monoespaciada | "THE AGENT THAT GROWS WITH YOU" en serif grande y elegante |
| **Releases** | Monoespaciada display | Monoespaciada | Tabla de datos estilo spreadsheet |

### 3.3 Jerarquia Tipografica

```
H1 (Hero): Serif elegante, 48-72px, tracking ligero, MAYUSCULAS
  Ejemplo: "THE AGENT THAT GROWS WITH YOU"

H2 (Seccion): Monoespaciada bold, 14-18px, MAYUSCULAS, subrayado
  Ejemplo: "LANGUAGE MODELS", "COMMITMENT TO DEVELOPMENT"

Body: Monoespaciada regular, 12-14px, interlineado amplio
  Ejemplo: Descripciones de mision y valores

Caption/Meta: Monoespaciada, 10-12px, color secundario
  Ejemplo: "OUTPUT 96", "SEED: 3573860127"

UI/Code: Monoespaciada, 12-14px, fondo blanco sobre azul
  Ejemplo: Bloques de instalacion por terminal
```

### 3.4 Caracteristicas Tipograficas Clave

- **Todo en MAYUSCULAS** para titulos y navegacion
- **Subrayado simple** bajo los titulos de seccion (border-bottom)
- **Metadatos decorativos** "OUTPUT" y "SEED" que parecen datos de generacion de imagen/modelo
- **Espaciado amplio** entre letras en navegacion y etiquetas
- **Interlineado generoso** que da aire al texto

---

## 4. LAYOUT Y ESPACIADO

### 4.1 Estructura de la Home Page

```
+----------------------------------------------------------+
|  NAV: HOME | HERMES AGENT | NOUS PORTAL | ...  (centrado)|
+----------------------------------------------------------+
|  ------------------------------------------------------  |  <- separador dashed
|                                                          |
|  [IMAGEN]    |  LANGUAGE MODELS        |  OUTPUT 96      |
|  (B&W+azul)  |  -----------------      |  SEED: ...      |
|              |  Descripcion...         |  [icono]        |
|                                                          |
|  ------------------------------------------------------  |
|                                                          |
|  [IMAGEN]    |  COMMITMENT TO          |  OUTPUT 288     |
|  (B&W+azul)  |  DEVELOPMENT            |  SEED: ...      |
|              |  -----------------      |  [icono]        |
|              |  Mision...              |                 |
|                                                          |
|  ------------------------------------------------------  |
|                                                          |
|  [IMAGEN]    |  APPLIED AI RESEARCH    |  OUTPUT 317     |
|              |  -----------------      |  SEED: ...      |
|              |  Focus areas...         |  [icono]        |
+----------------------------------------------------------+
```

**Patron**: 3-columnas (imagen | contenido | metadatos), separadas por lineas dashed horizontales.

### 4.2 Estructura de Releases

- **Tabla estilo spreadsheet/database** con columnas: # | PROJECT NAME | TYPE | DETAILS | RELEASE DATE | SIZE
- Header con "NOUS RELEASES" en tipografia grande, pixelada/display
- Buscador simple en esquina superior derecha
- Fila numerada (0-indexed!)

### 4.3 Estructura de Hermes Agent

```
+----------------------------------------------------------+
| NOUS    DOCS    HERMES AGENT    PORTAL    INSTALL ->       |
|                       [Discord] [GitHub]                   |
|                                                          |
|  OPEN SOURCE . MIT LICENSE                               |
|                                                          |
|  THE            [Ilustracion de Hermes (dios)]           |
|  AGENT          con rayos/burst azul y blanco            |
|  THAT                                                    |
|  GROWS                                                   |
|  WITH                                                    |
|  YOU                                                     |
|                                                          |
|  INSTALL DESKTOP APP                                     |
|  [INSTALAR VIA TERMINAL]                                 |
|                                                          |
|  curl -fsSL https://... | bash                           |
+----------------------------------------------------------+
```

### 4.4 Principios de Espaciado

- **Separadores dashed** como elemento distintivo (border-bottom: 1px dashed)
- **Espaciado generoso** entre secciones (padding vertical amplio)
- **Contenedor centrado** con max-width moderado (no full-bleed excepto Hermes Agent)
- **Grid consistente** con columnas bien definidas

---

## 5. ELEMENTOS VISUALES CLAVE

### 5.1 Iconografia y Simbolos

| Elemento | Descripcion | Uso |
|----------|-------------|-----|
| **The Nous Girl** | Personaje anime/manga femenino, estilo ilustracion retro japonesa | Logo principal, merch, avatar social |
| **Hermes (dios griego)** | Ilustracion clasica de Hermes con multiples brazos y rayos | Hero de la pagina Hermes Agent |
| **White Sun** | Sol con rayos estilizados | Simbolo recurrente en merch y branding |
| **Nous Loop** | Simbolo circular/bucle sobre el sol | Logo estilizado avanzado |
| **Iconos Unicode** | ♫ (musica), ◊ (rombo), otros simbolos simples | Elementos decorativos junto a metadatos OUTPUT/SEED |
| **Globo** | Icono de globo terraqueo simple | Seccion "Language Models" |

### 5.2 Tratamiento de Imagenes

- **Fotografias**: Blanco y negro con filtro azul/teal aplicado. Estetica fria, tecnica, casi de documental.
- **Ilustraciones**: Line art clasico (estilo grabado) con tratamiento monocromatico azul. Referencias mitologicas.
- **Anime/Manga**: Estilo retro japones, lineas limpias, tinta azul sobre blanco.
- **Sin fotos de equipo**: No muestran fotos de los fundadores. La identidad es colectiva, no personal.

### 5.3 Elementos UI Distintivos

| Elemento | Descripcion |
|----------|-------------|
| **OUTPUT / SEED** | Metadatos ficticios que parecen salidos de un generador de imagenes. "OUTPUT 96", "SEED: 3573860127". Refuerzan la estetica de "proceso de generacion". |
| **Bloques de codigo** | Fondo blanco, texto monoespaciada, bordes redondeados. Comandos de terminal reales (curl, bash). |
| **Botones** | Rectangulares, bordes sutiles, texto monoespaciada MAYUSCULAS. Sin gradients ni sombras. |
| **Tablas** | Bordes finos, celdas con padding generoso, tipografia monoespaciada. Estilo spreadsheet/data. |
| **Separadores dashed** | Lineas horizontales punteadas entre secciones. Patron visual recurrente. |

### 5.4 Patrones Decorativos

- **ASCII art sutil**: En algunas paginas se ven elementos tipo `/-_=+|<-/= ~:*-/` como decoracion
- **Numeracion 0-indexed**: Las releases empiezan en 0, no en 1. Detalle "nerd" que refuerza la identidad
- **Formato tecnico**: Los nombres de productos siguen convenciones tecnicas (Hermes-3-Llama-3.1-70B, etc.)

---

## 6. TONO DE VOZ

### 6.1 Caracteristicas Principales

| Caracteristica | Ejemplo | Descripcion |
|----------------|---------|-------------|
| **Casual/Autentico** | *"A bunch of nerds making progress toward open source AI"* (bio de X) | No se toman en serio a si mismos como empresa |
| **Tecnico pero accesible** | *"The agent that grows with you"* | Explican complejidad sin arrogancia |
| **Comunidad-first** | *"discord.gg/nousresearch"* en la bio | La comunidad es tan importante como el producto |
| **Anti-corporativo** | Nada de "solutions", "enterprise", "synergy" | Lenguaje directo, sin marketing corporativo |
| **Orgullosamente nerd** | "0-indexed" releases, ASCII art, referencias a mitologia griega | Celebran la cultura hacker/developer |
| **Filosoficamente comprometido** | *"advance human rights and freedoms by creating and proliferating open source language models"* | Mision con proposito mas alla del negocio |

### 6.2 Frases Clave que Definen el Tono

- *"Better today than yesterday, better tomorrow than today"* (mantra recurrente)
- *"The agent that grows with you"* (Hermes Agent)
- *"A bunch of nerds making progress toward open source AI"* (bio oficial)
- *"Small but mighty 30B SOTA mathematician"* (descripcion de Nomos 1)
- *"Model that can run on most modern hardware"* (descripcion accesible)

### 6.3 Como NO Hablan

- No usan lenguaje corporativo ("leverage", "synergy", "scalable solutions")
- No prometen "transformar industrias" o "revolucionar"
- No usan testimonios de clientes enterprise
- No tienen pagina de "precios" con tiers empresariales
- No usan fotos de stock de personas sonriendo

### 6.4 Como Presentan Productos

1. **Nombre tecnico claro**: Hermes-4-Llama-3.1-70B (no "Pro" o "Enterprise")
2. **Descripcion directa**: "Frontier hybrid-mode reasoning model"
3. **Datos duros**: tamaño en GB, fecha, benchmarks
4. **Open source primero**: Siempre mencionan MIT license, HuggingFace, GitHub
5. **Enfasis en accesibilidad**: "Small and dense Hermes variant for local inference"

---

## 7. COMPARATIVA: HOME vs HERMES AGENT vs PORTAL

| Aspecto | Home (nousresearch.com) | Hermes Agent | Portal |
|---------|------------------------|--------------|--------|
| **Fondo** | Blanco | Azul electrico intenso | Blanco |
| **Tipografia headlines** | Monoespaciada | Serif elegante + Mono | Sans-serif limpia |
| **Energia** | Contenida, academica | Explosiva, atrevida | Funcional, sobria |
| **Imagenes** | Fotos B&W con filtro azul | Ilustracion clasica de Hermes | Ninguna, solo UI |
| **Layout** | 3-columnas con separadores | Hero fullscreen + scroll | Modal centrado |
| **Proposito** | Presentar la organizacion | Vender/vistiar el producto | Acceso a herramientas |
| **CTA principal** | Navegacion a secciones | "Install via terminal" | "Sign In" |

**Insight clave**: Cada producto/pagina tiene su propia personalidad visual dentro del sistema de marca. No es un design system rigido sino una familia de estilos coherentes.

---

## 8. RECOMENDACIONES PARA "HERMES PARTHENON"

### 8.1 Paleta de Colores Recomendada

Basada en la estetica de Nous pero adaptada para "Hermes Parthenon":

| Rol | Color | Hex | Inspiracion |
|-----|-------|-----|-------------|
| **Fondo principal** | Azul Parthenon (electric) | `#1B1BFF` | Del hero de Hermes Agent, ligeramente ajustado |
| **Fondo alternativo** | Blanco Parthenon | `#F8F8F5` | Blanco roto de la tienda Nous |
| **Texto sobre azul** | Blanco puro | `#FFFFFF` | Alto contraste |
| **Texto sobre blanco** | Azul oscuro | `#0A0A2E` | Derivado del azul electrico |
| **Acento dorado** | Dorado Parthenon | `#C9A84C` | Referencia a la columnata dorada del Parthenon (columnas griegas) |
| **Acento cobalto** | Azul cobalto | `#0047AB` | De la serigrafia de la tienda Nous |
| **Codigo/Terminal** | Gris oscuro | `#1A1A2E` | Fondo para bloques de codigo |
| **Exito** | Verde terminal | `#00C853` | Estetica de terminal retro |

### 8.2 Tipografia Recomendada

| Rol | Fuente | Alternativa Libre |
|-----|--------|-------------------|
| **Headlines display** | Times New Roman o Didot | `Playfair Display` (Google Fonts) |
| **Cuerpo/UI** | Courier Pro | `Courier Prime`, `JetBrains Mono` |
| **Codigo/Terminal** | JetBrains Mono | `Fira Code`, `Source Code Pro` |

### 8.3 Elementos Visuales a Reutilizar

1. **Ilustracion clasica estilo grabado**: Hermes (el dios) como figura central, con columnas griegas (Parthenon) integradas en el arte
2. **Separadores dashed**: Lineas horizontales punteadas entre secciones
3. **Metadatos estilo generacion**: "OUTPUT", "SEED", "STATUS: ACTIVE" como elementos decorativos
4. **Bloques de codigo reales**: Mostrar comandos reales de instalacion/usage
5. **Tipografia en MAYUSCULAS** para navegacion y titulos de seccion
6. **Numeracion 0-indexed** para listas de features (detalle nerd)

### 8.4 Tono de Voz Recomendado

Adaptar el tono Nous para Hermes Parthenon:

| De Nous Research | Para Hermes Parthenon |
|-----------------|----------------------|
| "A bunch of nerds" | "Built by builders, for builders" |
| "The agent that grows with you" | "The architecture that thinks with you" |
| "Open Source . MIT License" | "Open Source . Apache 2.0" (o la licencia que aplique) |
| "Better today than yesterday" | "Codigo que evoluciona, como los pensamientos" |

**Principios de copy**:
- Corto y directo. Sin relleno.
- Cada palabra debe aportar valor.
- Usar metaforas arquitectonicas griegas (fundamentos, columnas, estructura, pilares)
- Hablar de "sistema" y "arquitectura" en lugar de "plataforma" y "solucion"
- Incluir referencias tecnicas reales (nombres de modelos, comandos, arquitecturas)

### 8.5 Layout Recomendado para Landing Page

```
+----------------------------------------------------------+
|  HERMES PARTHENON    [Docs] [GitHub] [Install]           |
+----------------------------------------------------------+
|                                                          |
|  OPEN SOURCE . APACHE 2.0                                |
|                                                          |
|  THE ARCHITECTURE     [Ilustracion: Hermes sobre         |
|  THAT REASONS          columnas del Parthenon con          |
|  WITH YOU              rayos de luz azul/blanco]         |
|                                                          |
|  [Install via terminal]                                  |
|  $ pip install hermes-parthenon                          |
|                                                          |
+----------------------------------------------------------+
|  ------------------------------------------------------  |
|                                                          |
|  PILLAR 1        |  PILLAR 2        |  PILLAR 3          |
|  --------------  |  --------------  |  --------------    |
|  Reasoning       |  Memory          |  Execution         |
|  ...             |  ...             |  ...               |
|  OUTPUT 001      |  OUTPUT 002      |  OUTPUT 003        |
|                                                          |
+----------------------------------------------------------+
|  ------------------------------------------------------  |
|  BENCHMARKS         [Tabla de datos estilo Nous]         |
|  0  Model X  ...                                              |
+----------------------------------------------------------+
```

### 8.6 Animaciones y Transiciones Recomendadas

Siguiendo el estilo Nous (minimalista, casi ausente):

- **Sin animaciones de entrada dramaticas** (no fade-ins largos, no slides)
- **Hover states simples**: Cambio de color de texto, subrayado
- **Transiciones de pagina**: Ninguna (comportamiento nativo del navegador)
- **Loading**: Spinner simple o texto "LOADING..." en monoespaciada
- **Cursor**: Cursor por defecto (no custom cursors)
- **Scroll**: Smooth scroll opcional, pero sin parallax ni efectos

La estetica Nous es **anti-animacion**. La informacion esta ahi, lista para consumirse. No hay que "revelarla" con efectos.

---

## 9. INSIGHTS CLAVE PARA EL DISEÑO

### 9.1 Lo que Hace Unica a la Estetica de Nous

1. **La contradiccion deliberada**: Mitologia griega + terminal de computadora + anime japones. No deberia funcionar, pero funciona porque es autentico.
2. **La simplicidad extrema**: No hay efectos, no hay gradients complejos, no hay animaciones. Solo color, tipografia y contenido.
3. **El detalle nerd**: 0-indexed, ASCII art, metadatos OUTPUT/SEED. Pequenos detalles que solo la comunidad tecnica aprecia.
4. **La consistencia inconsistente**: Cada pagina (home, agent, portal, shop) tiene su propia paleta y estilo, pero todos se sienten "Nous".

### 9.2 Lo que NO Debe Hacerse

- No usar gradients complejos (van contra la estetica plana y cruda)
- No usar animaciones de scroll o parallax (anti-Nous)
- No usar fotos de stock de personas (Nous nunca lo hace)
- No usar lenguaje corporativo o de "enterprise sales"
- No usar cards con sombras y bordes redondeados exagerados
- No usar iconos de Font Awesome o similares (mejor Unicode o SVG custom)

### 9.3 Checklist de Aplicacion

- [ ] Fondo azul electrico intenso para el hero
- [ ] Ilustracion clasica de Hermes/mitologia griega integrada
- [ ] Tipografia monoespaciada para todo el cuerpo de texto
- [ ] Serif elegante para el headline principal
- [ ] Separadores dashed entre secciones
- [ ] Metadatos estilo "OUTPUT X / SEED: Y" como decoracion
- [ ] Bloque de instalacion por terminal real y funcional
- [ ] Todo en MAYUSCULAS para navegacion y titulos
- [ ] Texto corto, directo, sin relleno
- [ ] Mencion de open source y licencia prominente
- [ ] Links a GitHub, Discord, Docs visibles siempre
- [ ] Sin animaciones, sin efectos, sin ruido visual

---

## 10. REFERENCIAS Y FUENTES

- **Home page**: https://nousresearch.com
- **Hermes Agent**: https://hermes-agent.nousresearch.com
- **Portal**: https://portal.nousresearch.com
- **Psyche Network**: https://psyche.network
- **Shop**: https://shop.nousresearch.com
- **Releases**: https://nousresearch.com/releases
- **X/Twitter**: https://x.com/NousResearch
- **GitHub**: https://github.com/NousResearch
- **Branding Booklet (PDF)**: https://nousresearch.com/wp-content/uploads/2024/03/NOUS-BRAND-BOOKLET-firstedition_1.pdf
- **Hermes 3 Technical Report**: https://nousresearch.com/wp-content/uploads/2024/08/Hermes-3-Technical-Report.pdf

---

*Analisis preparado para el equipo de diseno de Hermes Parthenon. Este documento sirve como referencia visual y conceptual para mantener coherencia con la estetica de Nous Research mientras se construye una identidad propia.*
