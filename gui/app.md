# App

**Script:** [App (script)](app.py)

## Purpose
The main GUI window: status overview + one-click actions over the whole
manifest, plus a single-file converter.

## Classes

### MainWindow
#### Sections
- Header card — logo, title, subtitle
- Action bar — Generate + Sync (primary), Generate ICOs, Sync Shortcuts,
  Convert File…
- Table — one row per entry: thumbnail, name, kind, SVG/ICO/LNK status dots
- Log — live progress stream

#### Methods
- `refresh_table()` — reload entries and repaint status
- `run_task(task)` — start a `TaskWorker`, disable buttons, stream the log
- `convert_file()` — file picker → ICO (+512px PNG)

## Helpers
- `svg_pixmap(path, size)` — render an SVG/ICO to a transparent pixmap
- `dot(ok)` — colored status cell

## Connections
### Uses
- [Worker](worker.md), [Theme](theme.md), [Converter](../core/converter.md),
  [Manifest](../core/manifest.md), [Config](../config.md)
