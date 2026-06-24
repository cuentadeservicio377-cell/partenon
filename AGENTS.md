# AGENTS.md — Partenon

## Reglas de Oro
1. **Siempre commitear** al cerrar sesión: `git add -A && git commit -m "tipo: descripción"`
2. **Siempre actualizar TODOS.md** antes de terminar
3. **Siempre verificar visualmente** las páginas HTML después de cambios importantes
4. **Foco en resultados funcionales**, no solo código
5. **No romper el build** — verificar antes de commit
6. **Mantener coherencia narrativa** entre `index.html` (marketing) y `developers.html` (técnico)

## Stack
- **Páginas web**: HTML estático + Tailwind CSS CDN + JavaScript vanilla
- **Tipografía**: Space Grotesk (display), Geist (body), JetBrains Mono (mono/data y hero técnico)
- **Estética**: Nous Research / manual técnico open source con anti-slop. Fondo `#050505` / `#08080C`, acento cian `#00D4FF` (saturación <80%), ámbar `#FFB800` quirúrgico, cards con doble-bisel, nav flotante fluid island, bordes hairline 1px, layouts asimétricos/bento. Sin gradientes masivos ni glows genéricos.
- **Agentes**: Hermes Agent (Nous Research) + Python skills
- **Dashboard futuro**: Next.js 15 + React 19 + TypeScript + Tailwind
- **Datos / workspace**: Google Workspace (Sheets, Docs, Slides, Drive, Calendar, Gmail)
- **Pagos**: Stripe API
- **Memoria**: G-Brain de Garitán vía MCP
- **Deploy local**: Docker / Docker Compose

## Convenciones
- Usar clases de Tailwind extendidas en `tailwind.config` inline en cada HTML.
- No usar fuentes baneadas: Inter, Roboto, Arial, Open Sans, Helvetica.
- No usar iconos gruesos; preferir Material Symbols Sharp peso 300.
- Animaciones solo con `transform` y `opacity`; nunca animar `width`, `height`, `top`, `left`.
- `backdrop-blur` solo en navbar fijo u overlays, nunca en contenedores con scroll.
- Mobile-first: todo layout asimétrico debe colapsar a `w-full` + `px-4` bajo 768px.
- Diagramas Mermaid con tema `base` y colores Partenon planos (fondos oscuros, bordes finos).
- Copy sin emdashes, intensificadores, filler phrases ni clichés de IA.

## Qué NO tocar sin consultar
- La estructura de los 6 héroes (Tesorero, Mensajero, Cobrador, Guardián, Estratega, Diplomático).
- La relación "Hermes = empresa" (no CEO).
- La dirección estética Nous-style y la paleta cian `#00D4FF` / ámbar `#FFB800`.
- El contador 10 → 1M y sus métricas de impacto.

## Checklist de Cierre
- [ ] Páginas se ven bien en desktop (1440px) y mobile (390px)
- [ ] No hay fuentes ni iconos baneados
- [ ] Mermaid renderiza sin errores
- [ ] Commit realizado
- [ ] TODOS.md actualizado
- [ ] README.md actualizado si cambia el scope
