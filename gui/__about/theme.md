# Theme

**Script:** [Theme (script)](../theme.py)

## Purpose
Dark-first theme, single indigo accent, per the monorepo design system
(root `rules/GUI.md` → Modern UI, `DESIGN.md`). All colors are tokens (root
`rules/CODE.md` → No Hardcoded Values) — never literals inside `app.py`.

## Contents
- `TOKENS` — flat dict: surfaces (0–3), border, text (+secondary), accent
  (+dark/light), semantic (success/warning/error)
- `QSS` — the stylesheet template string, `{token}` placeholders
- `stylesheet()` — `QSS.format(**TOKENS)`, applied once to the `QApplication`
- `apply_shadow(widget, blur=28, alpha=60, dy=8, color=None)` — soft ambient
  shadow / glow via `QGraphicsDropShadowEffect` (DESIGN.md depth spec)

## Connections
### Used by
- [App](app.md)
