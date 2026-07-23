# Config

**Script:** [Config (script)](config.py)

## Purpose
Single source of truth for every path and tunable (root Rule #4). Machine paths
are derived from the environment so nothing user-specific is baked into code.

## Key values

- `PROJECT_DIR`, `MONOREPO_ROOT`, `LOGOS_DIR` — derived from this file's
  location (the tool follows the repo wherever it lives).
- `ICO_DIR`, `SOURCES_DIR`, `SOURCES_LOCAL_DIR` — output and source roots.
- `DESKTOP_DIR` — the `VSCode Projects` shortcut folder. Defaults to
  `%USERPROFILE%\OneDrive\Desktop\VSCode Projects`; override with the
  `ICON_FORGE_DESKTOP` env var.
- `VSCODE_EXE` — VS Code executable. Defaults under `%LOCALAPPDATA%`; override
  with `ICON_FORGE_VSCODE`.
- `ICO_SIZES = [16,32,48,64,128,256]` — ICO frames (256 = Windows shell cap).
- `MAX_PNG = 512` — largest standalone PNG export.
- `supersample_factor(size)` — 4× ≤64px, 2× ≤128px, else 1×.

## Used by
- [Core (folder)](core/___core.md), [GUI (folder)](gui/___gui.md),
  [CLI Runner](run.md)
