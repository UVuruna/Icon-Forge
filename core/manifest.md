# Manifest

**Script:** [Manifest (script)](manifest.py)

## Purpose
Load the entry map and resolve each row into an absolute-path `Entry`.

## Classes

### Entry
One shortcut/icon target.

#### Attributes
- `name`, `kind` (`root` | `project`), `local` (from the hidden manifest)
- `svg`, `ico`, `target`, `shortcut` — resolved absolute paths

#### Properties
- `svg_exists`, `ico_exists`, `shortcut_exists`, `target_exists`

## Functions
- `load_entries()` → roots + projects from `manifest.json`, then any
  `manifest.local.json` (hidden) entries.

## Connections
### Uses
- [Paths](paths.md), [Config](../config.md)
### Used by
- [CLI Runner](../run.md), [GUI Worker](../gui/worker.md), [App](../gui/app.md)
