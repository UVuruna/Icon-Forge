# App

**Script:** [App (script)](../app.py) ·
**Flow:** [layout](../__flow/app.md)

## Purpose
The main GUI window: status overview + one-click actions over the whole
manifest, plus a single-file converter. Launch with `python run.py gui` or
`python -m gui.app`.

## Classes

### MainWindow(QWidget)
#### Methods
- `_header()` — logo + title/subtitle card
- `_action_bar()` — the four action buttons
- `_build_table()` — the 5-column entries table (Entry/Kind/SVG/ICO/LNK)
- `refresh_table()` — reloads entries via `load_entries()` and repaints
  every row's thumbnail + status dots
- `run_task(task)` — starts a `TaskWorker` for `"all"`/`"icons"`/
  `"shortcuts"`, disables the buttons, streams its `progress` signal into
  the log
- `_task_done()` — re-enables buttons, refreshes the table, appends "Done."
- `convert_file()` — file picker → `convert_to_ico` + `export_png` for one
  arbitrary file (not manifest-driven)
- `_set_busy(busy)` — enable/disable the four action buttons

## Helpers
- `svg_pixmap(path, size)` — renders an SVG (or loads an ICO) into a
  transparent `QPixmap`
- `dot(ok)` — a colored `●`/`—` status cell (`TOKENS["success"]` /
  `TOKENS["text-2"]`)

## Connections
### Uses
- [Worker](worker.md), [Theme](theme.md),
  [Converter](../../core/__about/converter.md),
  [Manifest](../../core/__about/manifest.md),
  [Config](../../__about/config.md)
### Used by
- [CLI Runner](../../__about/run.md) — `python run.py gui`
