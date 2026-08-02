# CLI Runner

**Script:** [CLI Runner (script)](../run.py)

## Purpose
Command-line entry point. Orchestrates ICO generation and shortcut sync,
prints a status table, converts one-off files, and launches the GUI.

## Commands
- `all` (default) — generate ICOs, then sync shortcuts
- `icons` — generate ICOs only
- `shortcuts` — create/update desktop shortcuts only
- `status` — per-entry SVG / ICO / LNK / target status
- `convert SRC [--out DIR] [--png]` — one-off SVG/PNG → ICO (+512px PNG)
- `gui` — launch the control panel

## Functions
- `main()` — argument parsing + command dispatch (a dict maps
  `all`/`icons`/`shortcuts`/`status` to their handler; `convert`/`gui` are
  handled before entries are even loaded, since they don't need the
  manifest)
- `generate_icons(entries)`, `cmd_icons`, `cmd_shortcuts`, `cmd_all`,
  `cmd_status`, `cmd_convert`, `cmd_gui` — one handler per command, each a
  thin wrapper printing to stdout over the `core/` functions

## Connections
### Uses
- [Manifest](../core/__about/manifest.md),
  [Converter](../core/__about/converter.md),
  [Shortcuts](../core/__about/shortcuts.md), [App](../gui/__about/app.md)
