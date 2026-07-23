# gui/

The PySide6 control panel. Dark-first, single indigo accent, per the monorepo
design system (root Rule #16, [DESIGN.md](../../../DESIGN.md)). Thin layer over
`core/` — it renders status and streams progress; all real work lives in the
engine.

## Files

### `app.py` — main window
One window: header card, action bar (Generate + Sync / Generate ICOs / Sync
Shortcuts / Convert File…), an entries table (thumbnail + kind + SVG/ICO/LNK
status dots), and a live log. Launch with `python run.py gui`. See
[App](app.md).

### `theme.py` — tokens + QSS
Color tokens and the QSS stylesheet, plus `apply_shadow` for soft depth. All
colors are tokens (root Rule #4). See [Theme](theme.md).

### `worker.py` — background task thread
A `QThread` that runs `icons` / `shortcuts` / `all` and streams progress lines,
keeping the UI responsive (root Rule #10). See [Worker](worker.md).

## Connections

### Uses
- [Core (folder)](../core/___core.md) — converter, manifest, shortcuts
- [Config](../config.md) — output dirs, PNG size

### Used by
- [CLI Runner](../run.md) — `python run.py gui`
