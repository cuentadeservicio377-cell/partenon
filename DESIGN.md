# DESIGN — Partenon Dark Premium Cyberpunk

## Identidad

Partenon es un sistema operativo de agentes para pymes latinoamericanas. La interfaz debe sentirse como una herramienta de elite: oscura, densa de información donde cuenta, y sin bullshit. No es un manual de mitología griega; es un dashboard de agentes vivos.

## Paleta

| Token | Valor | Uso |
|-------|-------|-----|
| `bg` | `#08080C` | Fondo base |
| `bg-elevated` | `#0E0E14` | Superficies elevadas |
| `panel` | `#13131A` | Paneles y cards |
| `panel-strong` | `#1A1A22` | Hover/focus states |
| `text` | `#E8E8ED` | Texto principal |
| `text-muted` | `#6B6B78` | Texto secundario |
| `text-dim` | `#45454F` | Metadatos, bordes suaves |
| `accent` | `#00E0FF` | Acento principal (cian eléctrico) |
| `accent-dim` | `rgba(0, 224, 255, 0.12)` | Fondos de acento |
| `accent-glow` | `rgba(0, 224, 255, 0.25)` | Sombra de acento sutil |
| `secondary` | `#FF2D92` | Estados vivos, alertas, pings (uso quirúrgico) |
| `line` | `rgba(255, 255, 255, 0.08)` | Bordes y divisores |
| `line-strong` | `rgba(255, 255, 255, 0.14)` | Bordes hover |

## Tipografía

| Rol | Fuente | Pesos |
|-----|--------|-------|
| Display | Space Grotesk | 500, 600, 700 |
| Body | Geist | 400, 500 |
| Mono | JetBrains Mono | 400, 500 |

### Escala

- Hero: `clamp(3.5rem, 8vw, 7rem)` / leading `0.9` / tracking `-0.04em`
- H2: `clamp(2.5rem, 5vw, 4rem)` / leading `0.95` / tracking `-0.03em`
- H3: `1.75rem` / leading `1.1` / tracking `-0.02em`
- Body: `1rem` / leading `1.6`
- Small/label: `0.75rem` / uppercase / tracking `0.12em`
- Mono/data: `0.875rem` / leading `1.4`

## Layout

- Contenedor: `max-w-[1400px] mx-auto px-6 md:px-10`
- Grid asimétrico por defecto. Bann 3-column cards iguales.
- Espaciado: secciones `py-24 md:py-32`. Aire generoso.
- Esquinas: `rounded-sm` (4px) para paneles. Botones: `rounded-none` o `rounded-full` deliberado.
- Bordes: 1px `line`, con transición a `line-strong` en hover.

## Background

- Base `#08080C`.
- Mesh gradient sutil fijo: dos blobs grandes de acento a ~3% opacity, uno arriba-izquierda, otro abajo-derecha.
- Ruido SVG fijo a `opacity-5`.
- Scanlines opcionales en secciones de datos: `repeating-linear-gradient` a 2% opacity.

## Componentes

### Botones
- Primary: fondo `accent`, texto `bg`, peso 500, padding `px-6 py-3`, esquina 0 o full. Hover: brillo sutil con `box-shadow: 0 0 20px accent-glow`.
- Secondary: borde 1px `line`, texto `text`, hover `line-strong` + texto `accent`.
- Ghost: texto `text-muted`, hover `text`.

### Paneles
- Fondo `panel`, borde 1px `line`, padding `p-6 md:p-8`.
- Hover: borde `line-strong`, transform `translateY(-2px)`.
- No sombras genéricas. Sí reflejo de borde sutil en hover.

### Labels / Tags
- Mono uppercase, tracking `0.14em`, tamaño `0.7rem`.
- Formato: `[ TAG ]` o `UNIT / 01`.

## Animaciones

- Transiciones: `cubic-bezier(0.16, 1, 0.3, 1)` duración 400ms.
- Scroll reveal: `opacity` + `translateY(24px)`, easing personalizado.
- Glitch text: solo en hero principal, implementado con CSS clip-path / text-shadow, no en todo el sitio.
- Contadores: animación numérica con `requestAnimationFrame`.
- Nada de `linear` o `ease-in-out` por defecto.

## Anti-patterns prohibidas

- No Inter, no Roboto, no Arial.
- No emojis.
- No gradientes masivos en texto.
- No glows de neón por todos lados.
- No cards redondeadas uniformes.
- No layouts simétricos de 3 cards.
- No copy con "eleva", "impulsa", "revoluciona", "sin fisuras".
- No afirmaciones huecas sin dato concreto.
- No emdashes.

## Voz

Directa, técnica, sin adornos. Cada oración termina en un hecho verificable. Los héroes son perfiles operativos, no dioses. Hermes es la empresa. El Partenón es el lugar de trabajo compartido.
