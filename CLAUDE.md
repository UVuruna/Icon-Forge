# CLAUDE.md — Icon Forge

Project-specific guidance. **Inherits ALL rules from the monorepo root
[CLAUDE.md](../../CLAUDE.md)** (mandatory workflow, Priorities, Rules #1–#24,
markdown guidelines, MD-first docs). Read that first; only project facts and
deltas live here.

---

## Project Facts

- **Purpose:** SVG/PNG → ICO converter + manager of the desktop
  `VSCode Projects/` `.lnk` shortcuts (custom icon per project and per category
  ROOT folder, for fast opening in VS Code).
- **Stack:** Python 3.13, PySide6 (`QSvgRenderer` render), Pillow (ICO/PNG
  save), PowerShell `WScript.Shell` for `.lnk` writing. No installer, no build
  pipeline, no GIT RELEASE — this is an internal dev utility (owner decision
  2026-07-23).
- **Language choice (root Rule #21):** Python — reuses the exact proven SVG→ICO
  render already used by every build pipeline's `svg_to_ico.py` (root Rule #5),
  and PySide6 is already the house GUI toolkit. No lighter tool would avoid the
  Qt SVG dependency the render quality needs.

## Design Decisions

- **Sources are not duplicated (root Rule #5).** Project logos are read from the
  monorepo `logos/` folder; `paths.resolve_svg` tries the project dir first,
  then `logos/`. Only the category ROOT icons (`sources/roots/`) and hidden
  entries (`sources_local/`) are owned here.
- **ICO output is computed, never stored (root Rule #19).** `ico/` is
  gitignored and regenerated from SVG on demand.
- **Hidden projects (root Rule #23 / visibility):** entries live in
  `manifest.local.json` and `sources_local/`, both gitignored. Owner decision
  2026-07-23: a hidden project's **name and icon may appear** in the tool and on
  the desktop, but **no description** of what it is or does — anywhere. Nothing
  hidden is ever pushed.
- **ICO caps at 256px** (Windows Explorer's real cap for a shortcut icon); the
  512px size the owner wanted is exposed as a separate PNG export.
- **Shortcut writing is delegated to PowerShell** (`write_shortcuts.ps1`) — the
  dependency-free, reliable way to author `.lnk` files. `shortcuts.py` only
  builds the specs; it never edits binary `.lnk` bytes itself.

## Config, not hardcode (root Rule #4)

All paths and tunables live in [config.py](config.py); the entry list lives in
`manifest.json`. Machine-specific locations (desktop folder, VS Code exe) are
derived from environment variables with overrides — nothing user-specific is
baked into code.

## Communication

Serbian (Latin) with the owner; everything in files stays English (root
Rules #12 / #13).
