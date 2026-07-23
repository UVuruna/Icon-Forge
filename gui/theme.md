# Theme

**Script:** [Theme (script)](theme.py)

## Purpose
Dark-first theme, single indigo accent, per the monorepo design system (root
Rule #16, [DESIGN.md](../../../DESIGN.md)). All colors are tokens (root Rule #4).

## Contents
- `TOKENS` — surfaces, border, text, accent, semantic colors
- `QSS` / `stylesheet()` — the stylesheet, tokens interpolated in
- `apply_shadow(widget, blur, alpha, dy, color)` — soft ambient shadow / glow
  (`QGraphicsDropShadowEffect` tuned to the DESIGN.md depth spec)

## Connections
### Used by
- [App](app.md)
