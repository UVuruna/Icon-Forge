# CLAUDE.md — Icon Forge

The monorepo constitution governs: read the root `CLAUDE.md` first, then
load ONLY the rulebook your job needs via its Router. Nothing universal is
restated here — this file carries project FACTS and project DELTAS, and may
only tighten root rules, never loosen them.

| Your job this session | Read (monorepo root) |
|-----------------------|----------------------|
| Implement / fix | `rules/CODE.md` + the folder's `___folder.md` |
| Any GUI work | `rules/GUI.md` + `DESIGN.md` |
| Write documentation | `rules/DOCS.md` |
| Migrate docs / enforcement | `MIGRATE-DOCS.md` + `rules/DOCS.md` |
| Plan / brainstorm | `rules/PLAN.md` |

Start here for the code itself: [README](README.md) →
[Core (folder)](core/___core.md) / [GUI (folder)](gui/___gui.md). Open
decisions live in [Open Questions](OPEN-QUESTIONS.md).

---

## Project Facts

- **Purpose:** SVG/PNG → ICO converter + manager of the desktop
  `VSCode Projects/` `.lnk` shortcuts (custom icon per project and per
  category ROOT folder, for fast opening in VS Code).
- **Stack:** Python 3.13, PySide6 (`QSvgRenderer` render), Pillow (ICO/PNG
  save), PowerShell `WScript.Shell` for `.lnk` writing. **No installer, no
  build pipeline, no GIT RELEASE** (owner decision 2026-07-23) — this is an
  internal dev utility; `rules/SHIP.md` does not apply here.
- **Language choice (root `rules/START.md` → Technology Selection):**
  Python — reuses the exact proven SVG→ICO render already used by every
  build pipeline's `svg_to_ico.py` (no duplicate code), and PySide6 is
  already the house GUI toolkit for this kind of tool. No lighter tool
  would avoid the Qt SVG dependency the render quality needs. Alternative
  considered: a pure-Pillow/`cairosvg` renderer — rejected, its SVG
  fidelity is weaker than Qt's for the gradients/filters some project logos
  use.

## Design Decisions

- **Sources are not duplicated.** Project logos are read from the monorepo
  `logos/` folder; `core/paths.resolve_svg` tries the project dir first,
  then `logos/`. Only the category ROOT icons (`sources/roots/`) and hidden
  entries (`sources_local/`) are owned here.
- **ICO output is computed, never stored** (root `rules/CODE.md` → Compute,
  Don't Generate). `ico/` is gitignored and regenerated from SVG on demand.
- **Hidden projects (see root `CLAUDE.md` → Project Visibility):** entries
  live in `manifest.local.json` and `sources_local/`, both gitignored.
  Owner decision 2026-07-23: a hidden project's **name and icon may
  appear** in the tool and on the desktop, but **no description** of what
  it is or does — anywhere. Nothing hidden is ever pushed.
- **ICO caps at 256px** (Windows Explorer's real cap for a shortcut icon);
  the 512px size the owner wanted is exposed as a separate PNG export.
- **Shortcut writing is delegated to PowerShell**
  (`write_shortcuts.ps1`) — the dependency-free, reliable way to author
  `.lnk` files. `shortcuts.py` only builds the specs; it never edits binary
  `.lnk` bytes itself.

## Enforcement — Project Deltas

- **Guard-test ratchet policy:** `RATCHET` in `tests/test_structure_law.py`
  is EMPTY — the 2026-08-02 migration inventory found no file over ~201
  lines (`gui/app.py`, the largest) anywhere in this project. Adding an
  entry requires the owner's explicit approval in the same session that
  needs it (root `rules/CODE.md` → Enforcement).
- **`CONFIG_FILES`** in `tests/test_config_sections.py` is seeded narrowly
  with `config.py` only — see [Open Questions](OPEN-QUESTIONS.md) #2 for
  the `gui/theme.py` judgment call.
- **`test_structure_law.py`'s `SUFFIXES`** includes `.ps1` (not just `.py`)
  — this project's one PowerShell helper is a real source file and the
  god-file check costs nothing extra to widen; the docs-coverage and
  config-sections guards stay `.py`-only per the monorepo's reference
  implementation.

## Config, not hardcode

All paths and tunables live in `config.py`; the entry list lives in
`manifest.json`. Machine-specific locations (desktop folder, VS Code exe)
are derived from environment variables with overrides — nothing
user-specific is baked into code.

## Communication

Serbian (Latin) with the owner; everything in files stays English.
