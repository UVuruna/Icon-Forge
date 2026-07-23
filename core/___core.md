# core/

The engine of Icon Forge: turn sources into ICOs, resolve the manifest, and
write the desktop shortcuts. No GUI, no CLI — pure logic, importable in
isolation.

## Files

### `converter.py` — SVG/PNG → ICO/PNG
Renders a source into a multi-resolution ICO (and optional 512px PNG). SVG is
rendered with an anti-aliased `QPainter` at a supersampled size then Lanczos
downscaled; raster input is resized directly. Same proven render as the build
pipelines' `svg_to_ico.py` (root Rule #5). See [Converter](converter.md).

### `manifest.py` — entry model
Loads `manifest.json` (+ optional `manifest.local.json`) and resolves every raw
row into an `Entry` with absolute SVG / ICO / target / shortcut paths and
status properties. See [Manifest](manifest.md).

### `paths.py` — path resolution
`resolve_svg` (project dir → monorepo `logos/`) and `resolve_target` (against
the monorepo root). See [Paths](paths.md).

### `shortcuts.py` — shortcut writer
Builds a spec per entry and delegates the actual `.lnk` creation to
`write_shortcuts.ps1`. See [Shortcuts](shortcuts.md).

### `write_shortcuts.ps1` — WScript.Shell creator
Reads a JSON spec list and creates/updates each `.lnk` via the
`WScript.Shell` COM object (TargetPath = VS Code, Arguments = the folder,
IconLocation = the generated ICO). Called only by `shortcuts.py`; never run by
hand. No individual `.md` — a generated helper described here.

## Connections

### Used by
- [CLI Runner](../run.md) — orchestrates convert + sync
- [GUI Worker](../gui/worker.md) — runs the same batch off the UI thread

### Uses
- [Config](../config.md) — paths, ICO sizes, supersample factors
