# core/

The engine of Icon Forge: turn sources into ICOs, resolve the manifest, and
write the desktop shortcuts. No GUI, no CLI — pure logic, importable in
isolation.

## Files

| File | Tier | One line |
|------|------|----------|
| `converter.py` | Algorithmic | SVG/PNG → ICO/PNG render engine — [about](__about/converter.md) · [flow](__flow/converter.md) |
| `manifest.py` | Standard | loads `manifest.json` (+local) into `Entry` objects — [about](__about/manifest.md) |
| `paths.py` | Standard | resolves manifest paths against project dir / monorepo root — [about](__about/paths.md) |
| `shortcuts.py` | Algorithmic | builds specs, hands off to `write_shortcuts.ps1` — [about](__about/shortcuts.md) · [flow](__flow/shortcuts.md) |
| `write_shortcuts.ps1` | Trivial | PowerShell `WScript.Shell` `.lnk` writer, called only by `shortcuts.py`; never run by hand |
| `__init__.py` | Trivial | empty package marker |

## Connections

### Used by
- [CLI Runner](../__about/run.md) — orchestrates convert + sync
- [GUI Worker](../gui/__about/worker.md) — runs the same batch off the UI
  thread
- [App](../gui/__about/app.md) — one-off `convert_file()`

### Uses
- [Config](../__about/config.md) — paths, ICO sizes, supersample factors

## Design Decisions
`write_shortcuts.ps1` stays Trivial tier deliberately (root DOCS.md tier
table: glue/wiring under ~60 lines with no branching logic of its own beyond
"create the dir if missing, then set the four shortcut properties") — its
protocol is described inside `shortcuts.py`'s own flow doc, since that is
where the caller-side decisions (skip vs write, cleanup) actually live.
