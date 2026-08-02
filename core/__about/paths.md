# Paths

**Script:** [Paths (script)](../paths.py)

## Purpose
Resolve manifest-relative paths against the right root, so project logos
are shared from the monorepo `logos/` folder and never duplicated (root
`rules/CODE.md` → No Duplicate Code).

## Functions
- `resolve_svg(rel)` — tries the project dir first (this tool's own
  `sources/`), then the monorepo root (shared `logos/`). Returns the
  project-dir candidate if neither exists, so the caller (`Entry.svg_exists`)
  can report it as missing rather than raise.
- `resolve_target(rel)` — resolves a folder path against the monorepo root;
  `"."` (or `""`) means the monorepo root itself (the `UVuruna` ROOT
  shortcut's target).

## Connections
### Uses
- [Config](../../__about/config.md) — `PROJECT_DIR`, `MONOREPO_ROOT`
### Used by
- [Manifest](manifest.md)
