# CLI Runner

**Script:** [CLI Runner (script)](run.py)

## Purpose
Command-line entry point. Orchestrates ICO generation and shortcut sync, prints
a status table, converts one-off files, and launches the GUI.

## Commands
- `all` (default) — generate ICOs, then sync shortcuts
- `icons` — generate ICOs only
- `shortcuts` — create/update desktop shortcuts only
- `status` — per-entry SVG / ICO / LNK / target status
- `convert SRC [--out DIR] [--png]` — one-off SVG/PNG → ICO (+512px PNG)
- `gui` — launch the control panel

## Connections
### Uses
- [Manifest](core/manifest.md), [Converter](core/converter.md),
  [Shortcuts](core/shortcuts.md), [App](gui/app.md)
