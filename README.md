# Icon Forge

Icon Forge is a Windows developer utility that turns project logo SVGs (or PNGs) into multi-resolution ICO files and stamps them onto the VSCode quick-open shortcuts on the desktop, so every project and every category folder opens from a distinct, recognizable icon.

It exists for one concrete job: the `Desktop/VSCode Projects` folder full of
`.lnk` shortcuts that open each UVuruna project in VS Code. Left alone they all
share Windows' default icon (or random reused ones) and become impossible to
tell apart. Icon Forge renders each project's logo into a crisp ICO and points
its shortcut at it — and creates any shortcut that is missing.

---

## Table of Contents

- [What it does](#what-it-does)
- [Structure](#structure)
- [Usage](#usage)
- [How it works](#how-it-works)
- [Documentation map](#docs)

---

<a id="what-it-does"></a>

## What it does

- **Convert** — SVG or PNG → multi-resolution ICO (16–256px, supersampled +
  Lanczos for sharpness), plus an optional 512px PNG export.
- **Batch** — reads `manifest.json` and generates one ICO per project and per
  category ROOT folder.
- **Shortcuts** — creates/updates the desktop `.lnk` files: sets each one to
  open its folder in VS Code with its own generated icon. Missing shortcuts
  (projects and ROOTs) are created; existing ones are re-pointed.

The old shortcuts pointed their icons at an external `M:\` drive and several
reused the same file (Colorize SVG and Ultra Vivid were identical). Icon Forge
gives every entry a distinct icon on the always-present `U:\` drive.

<a id="structure"></a>

## Structure

```
📁 Icon Forge/
  📝 README.md              ← this file (plays the ___folder.md role for the loose root scripts below)
  📝 CLAUDE.md              ← project rules (inherits monorepo root)
  📝 OPEN-QUESTIONS.md      ← judgment calls made in autonomous sessions, for owner review
  ⚙️ config.py              ← paths + tunables (single source of truth) — [about](__about/config.md)
  ⚙️ manifest.json          ← entry map (roots + projects) — tracked
  ⚙️ manifest.local.json    ← hidden entries — gitignored
  🐍 run.py                 ← CLI entry point — [about](__about/run.md)
  📁 __about/                 ← WHAT: root loose-script docs
  📁 assets/
    🖼️ logo.svg             ← Icon Forge's own logo
  📁 core/
    📝 ___core.md
    📁 __about/                ← WHAT: per-file description & connections
    📁 __flow/                 ← HOW: per-file algorithm diagrams
    🐍 converter.py         ← SVG/PNG → ICO/PNG engine
    🐍 manifest.py          ← load + resolve entries
    🐍 paths.py             ← path resolution
    🐍 shortcuts.py         ← .lnk writer (drives PowerShell)
    🔧 write_shortcuts.ps1  ← WScript.Shell shortcut creator
  📁 gui/
    📝 ___gui.md
    📁 __about/
    📁 __flow/
    🐍 app.py               ← main window
    🐍 theme.py             ← dark theme tokens + QSS
    🐍 worker.py            ← background task thread
  📁 tests/
    📝 ___tests.md
    🐍 test_structure_law.py, test_config_sections.py, test_docs_coverage.py, test_doc_links.py, run_guards.py
  📁 .claude/
    ⚙️ settings.json        ← PostToolUse + Stop guard hooks
  📁 sources/roots/         ← category ROOT icons (SVG)
  📁 sources_local/         ← hidden-project SVGs — gitignored
  📁 ico/                   ← generated ICO output — gitignored
```

<a id="usage"></a>

## Usage

```bash
pip install -r requirements.txt

python run.py            # generate all ICOs, then sync shortcuts (default)
python run.py icons      # generate ICOs only
python run.py shortcuts  # create/update desktop shortcuts only
python run.py status     # show source / ICO / shortcut status per entry
python run.py gui        # open the GUI control panel
python run.py convert path/to/art.svg --png   # one-off convert (+512px PNG)
```

The desktop folder and VS Code path are derived from the environment; override
with the `ICON_FORGE_DESKTOP` and `ICON_FORGE_VSCODE` environment variables if
they differ on this machine (see [Config](__about/config.md)).

<a id="how-it-works"></a>

## How it works

```mermaid
%%{init: {'flowchart': {'subGraphTitleMargin': {'top': 0, 'bottom': 35}}}}%%
flowchart LR
    M[manifest.json] --> L[manifest.py]
    S[logos/*.svg + sources/*] --> C[converter.py]
    L --> C
    C --> I[(ico/*.ico)]
    L --> H[shortcuts.py]
    I --> H
    H --> P[write_shortcuts.ps1]
    P --> K[Desktop *.lnk]
```

Sources are never duplicated: project logos are read straight from the monorepo
`logos/` folder (the single source of truth); only the category ROOT icons and
hidden-project icons live inside this tool. ICO output is computed on demand and
gitignored (root `rules/CODE.md` → Compute, Don't Generate).

<a id="docs"></a>

## Documentation map

This README plays the `___folder.md` role for the two loose root scripts
(root DOCS.md, "flat, root-level-only projects" provision):

- [Config](__about/config.md) — paths and tunables
- [CLI Runner](__about/run.md) — command entry point
- [Core (folder)](core/___core.md) — converter, manifest, paths, shortcuts
- [GUI (folder)](gui/___gui.md) — window, theme, worker
- [Tests (folder)](tests/___tests.md) — the four enforcement guards
- [Open Questions](OPEN-QUESTIONS.md) — judgment calls flagged for owner review

Project rules and facts: [CLAUDE.md](CLAUDE.md). Universal rules for every
project in this monorepo live at the root: `CLAUDE.md`, `rules/CODE.md`,
`rules/DOCS.md`.
