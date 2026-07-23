# Paths

**Script:** [Paths (script)](paths.py)

## Purpose
Resolve manifest paths against the right roots — so project logos are shared
from `logos/` and never duplicated (root Rule #5).

## Functions
- `resolve_svg(rel)` — tries the project dir first (own `sources/`), then the
  monorepo `logos/`. Returns the project-dir candidate if neither exists so the
  caller can report it missing.
- `resolve_target(rel)` — resolves a folder path against the monorepo root;
  `"."` means the monorepo root itself (the UVuruna ROOT shortcut).

## Connections
### Uses
- [Config](../config.md) — `PROJECT_DIR`, `MONOREPO_ROOT`
### Used by
- [Manifest](manifest.md)
