# Config

**Script:** [Config (script)](../config.py)

## Purpose
Single source of truth for every path and tunable (root `rules/CODE.md` →
No Hardcoded Values). Machine
paths are derived from the environment so nothing user-specific is baked
into code. Config-law guarded — see [Design Decisions](#design-decisions).

## Key values

- `PROJECT_DIR`, `MONOREPO_ROOT`, `LOGOS_DIR` — derived from this file's own
  location (the tool follows the repo wherever it is cloned).
- `ICO_DIR`, `SOURCES_DIR`, `SOURCES_LOCAL_DIR` — output and source roots.
- `DESKTOP_DIR` — the `VSCode Projects` shortcut folder. Defaults to
  `%USERPROFILE%\OneDrive\Desktop\VSCode Projects`; override with the
  `ICON_FORGE_DESKTOP` env var.
- `VSCODE_EXE` — VS Code executable. Defaults under `%LOCALAPPDATA%`;
  override with `ICON_FORGE_VSCODE`.
- `MANIFEST`, `MANIFEST_LOCAL`, `SHORTCUT_SCRIPT` — data/helper file paths.
- `ICO_SIZES = [16, 32, 48, 64, 128, 256]` — ICO frames (256 = Windows shell
  cap for a `.lnk` icon).
- `MAX_PNG = 512` — largest standalone PNG export.
- `supersample_factor(size)` — 4× at ≤64px, 2× at ≤128px, else 1×.

## Connections
### Used by
- [Core (folder)](../core/___core.md), [GUI (folder)](../gui/___gui.md),
  [CLI Runner](run.md)

<a id="design-decisions"></a>
## Design Decisions
This file is seeded in `tests/test_config_sections.py`'s `CONFIG_FILES` —
its two sections (`LOCATIONS`, `RENDERING`) are organized under canonical
banners so a future addition lands inside the right table instead of being
appended at file end. `gui/theme.py`'s `TOKENS` dict was considered for the
same seeding and left out: it is one flat, already-atomic dict with no
history of scattered patches — adding it would widen `CONFIG_FILES` beyond
"narrow" (root CODE.md → Enforcement) without a concrete failure mode to
guard against. Recorded for owner review in [Open Questions](../OPEN-QUESTIONS.md).
