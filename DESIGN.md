# DESIGN — Partenon High-End Agency

## Identidad

Partenon es un sistema operativo de agentes para pymes latinoamericanas. La interfaz debe sentirse como un producto de elite: oscura, precisa, con aire entre los elementos y sin bullshit. No es un manual de mitología griega; es un dashboard de agentes vivos contado como manual de marketing y espejo técnico.

## Paleta

| Token | Valor | Uso |
|-------|-------|-----|
| `bg` | `#050505` | Fondo base OLED |
| `surface` | `#08080C` | Superficies de sección alternas |
| `panel` | `#0E0E14` | Fondos de código y diagramas |
| `panel-raised` | `#111118` | Cards doble-bisel (inner core) |
| `panel-strong` | `#16161F` | Hover/focus states |
| `text` | `#E8E8ED` | Texto principal |
| `muted` | `#6B6B78` | Texto secundario |
| `dim` | `#45454F` | Metadatos, bordes suaves |
| `accent` | `#00D4FF` | Acento único (cian desaturado) |
| `accent-dim` | `rgba(0, 212, 255, 0.10)` | Fondos de acento |
| `accent-glow` | `rgba(0, 212, 255, 0.20)` | Sombra de acento sutil |
| `live` | `#FFB800` | Estados vivos, pings (uso quirúrgico) |
| `line` | `rgba(255, 255, 255, 0.07)` | Bordes y divisores |
| `line-strong` | `rgba(255, 255, 255, 0.14)` | Bordes hover |

### Reglas de color
- Un solo acento principal. El ámbar (`#FFB800`) aparece en no más de 2 elementos por página.
- Saturación del acento por debajo del 80%.
- No `#000000` puro. El fondo es `#050505`.
- No gradientes masivos. Solo mesh radiales sutiles a ~3% opacity.

## Tipografía

| Rol | Fuente | Pesos |
|-----|--------|-------|
| Display | Space Grotesk | 500, 600, 700 |
| Body | Geist | 400, 500 |
| Mono / data | JetBrains Mono | 400, 500 |
| Icons | Material Symbols Sharp | 300 |

### Escala
- Hero: `clamp(3rem, 10vw, 8.5rem)` / leading `0.88` / tracking `-0.055em`
- H2: `clamp(2.5rem, 5vw, 4rem)` / leading `0.95` / tracking `-0.04em`
- H3: `1.75rem` / leading `1.1` / tracking `-0.02em`
- Body: `1rem` / leading `1.6`
- Small/label: `0.7rem` / uppercase / tracking `0.14em`
- Mono/data: `0.875rem` / leading `1.4`

### Reglas tipográficas
- No Inter, Roboto, Arial, Open Sans, Helvetica.
- Números en `font-variant-numeric: tabular-nums`.
- Headlines con presencia: grandes, tracking ajustado, line-height apretado.
- Body limitado a ~65 caracteres por línea.

## Layout

- Contenedor: `max-w-[1400px] mx-auto px-4 md:px-6`.
- Grid asimétrico por defecto. Bento con combinaciones de `col-span` variables.
- Espaciado: secciones `py-24 md:py-32`.
- Esquinas: doble-bisel exterior `18px`, interior `12px`. Botones `rounded-full` o `0` deliberado.
- Bordes: 1px `line`, transición a `line-strong` en hover.
- Mobile-first: todo layout asimétrico colapsa a `w-full` + `px-4` bajo 768px.

## Background

- Base `#050505`.
- Mesh gradient fijo: 2-3 orbes radiales grandes de acento a ~3% opacity.
- Noise SVG fijo a `opacity-3.5`.
- Scanlines opcionales en secciones de datos: `repeating-linear-gradient` a 2% opacity.

## Componentes

### Nav flotante (fluid island)
- Fijo en top, centrado, `border-radius: 999px`.
- `backdrop-blur: 16px`, fondo `rgba(8,8,12,0.72)`.
- Links `border-radius: 999px`, color muted, hover con fondo sutil.
- Menú móvil: overlay full-screen con staggered reveal.

### Botones
- Primary: fondo `accent`, texto `bg`, peso 500, `rounded-full`, padding `0.875rem 1.5rem`.
  - Hover: `translateY(-2px)` + `box-shadow` tintado acento.
  - Active: `scale(0.98)`.
- Secondary: borde 1px `line`, fondo `rgba(255,255,255,0.02)`, texto `text`, `rounded-full`.
  - Hover: borde `line-strong`, texto `accent`, fondo `rgba(255,255,255,0.04)`.
- Icono interno en botón: círculo `w-7 h-7`, se mueve en hover.

### Cards (doble-bisel)
- Outer shell: fondo `rgba(255,255,255,0.025)`, borde 1px `line`, `border-radius: 18px`, padding `6px`.
- Inner core: fondo `panel-raised`, borde 1px `rgba(255,255,255,0.05)`, `border-radius: 12px`, `box-shadow: inset 0 1px 0 rgba(255,255,255,0.04)`.
- Hover: borde exterior pasa a `line-strong`.

### Labels / Tags
- Mono uppercase, tracking `0.14em`, tamaño `0.7rem`, color `muted`.
- Formato: palabras clave en mayúsculas, precedidas por dot de acento.

## Animaciones

- Transiciones: `cubic-bezier(0.16, 1, 0.3, 1)` duración 350-900ms.
- Scroll reveal: `opacity` + `translateY(32px)`, easing personalizado.
- Contadores: animación numérica con `requestAnimationFrame`.
- Nada de `linear` o `ease-in-out` por defecto.
- Solo `transform` y `opacity`. Nunca `width`, `height`, `top`, `left`.

## Iconografía

- Material Symbols Sharp vía Google Fonts, peso 300.
- Respaldo con SVG inline propios.
- Prohibido: Lucide grueso, FontAwesome genérico, emojis.

## Anti-patterns prohibidos

- No Inter, Roboto, Arial, Open Sans, Helvetica.
- No emojis.
- No gradientes masivos en texto ni fondos.
- No glows de neón por todos lados.
- No cards redondeadas uniformes sin doble-bisel.
- No layouts simétricos de 3 cards iguales.
- No copy con "eleva", "impulsa", "revoluciona", "sin fisuras".
- No emdashes.
- No afirmaciones huecas sin dato concreto.
- No `h-screen` para hero; usar `min-h-[100dvh]`.
- No `z-50` o `z-[9999]` arbitrarios.

## Voz

Directa, técnica, sin adornos. Cada oración termina en un hecho verificable. Los héroes son perfiles operativos, no dioses. Hermes es la empresa. El Partenón es el lugar de trabajo compartido.
