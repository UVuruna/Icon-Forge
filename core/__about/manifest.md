# Manifest

**Script:** [Manifest (script)](../manifest.py)

## Purpose
Load the entry map (`manifest.json` + optional `manifest.local.json`) and
resolve each raw row into an absolute-path `Entry`.

## Classes

### Entry
One shortcut/icon target (a category ROOT folder or a project).

#### Attributes
- `name` — display name
- `kind` — `"root"` or `"project"`
- `local` — `True` when it came from `manifest.local.json` (hidden project)
- `svg`, `ico`, `target`, `shortcut` — resolved absolute `Path`s

#### Properties
- `svg_exists`, `ico_exists`, `shortcut_exists`, `target_exists` — live
  filesystem checks, used by `status`/the GUI table to render OK/missing.

## Functions
- `load_entries()` — reads `manifest.json` (roots then projects), then
  `manifest.local.json` if present (merged in as local projects). Returns
  the combined `list[Entry]`.
- `_build(raw, kind, local)` — internal: one raw manifest row -> `Entry`,
  resolving `svg`/`target` via [Paths](paths.md) and `ico`/`shortcut`
  against `config.py`'s output/desktop directories.

## Connections
### Uses
- [Paths](paths.md), [Config](../../__about/config.md)
### Used by
- [CLI Runner](../../__about/run.md), [Worker](../../gui/__about/worker.md),
  [App](../../gui/__about/app.md)
