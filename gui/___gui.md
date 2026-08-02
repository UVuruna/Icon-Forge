# gui/

The PySide6 control panel. Dark-first, single indigo accent, per the
monorepo design system (root `rules/GUI.md` → Modern UI, `DESIGN.md`). Thin
layer over
`core/` — it renders status and streams progress; all real work lives in
the engine.

## Files

| File | Tier | One line |
|------|------|----------|
| `app.py` | Algorithmic | main window — header, action bar, entries table, log — [about](__about/app.md) · [flow](__flow/app.md) |
| `theme.py` | Standard | color tokens + QSS stylesheet + shadow helper — [about](__about/theme.md) |
| `worker.py` | Standard | background `QThread` running icons/shortcuts, streams progress — [about](__about/worker.md) |
| `__init__.py` | Trivial | empty package marker |

## Connections

### Uses
- [Core (folder)](../core/___core.md) — converter, manifest, shortcuts
- [Config](../__about/config.md) — output dirs, PNG size

### Used by
- [CLI Runner](../__about/run.md) — `python run.py gui`
