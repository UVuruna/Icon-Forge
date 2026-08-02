# Open Questions

Judgment calls made during the 2026-08-02 overnight docs-migration +
enforcement session (root `MIGRATE-DOCS.md`). None blocked the session —
each was resolved with a stated rationale — but per the autonomous-session
protocol (root `rules/CODE.md` → Enforcement) they are surfaced here for the
owner to ratify or overrule. Linked from [README.md](README.md).

## 1. Tier calls: converter.py, shortcuts.py, gui/app.py as Algorithmic

Root `rules/DOCS.md` narrows the Algorithmic tier hard ("reading turns ~80%
of files 'Algorithmic'" was the lesson of the first pilots) — a flow doc
must EARN its place. Three files were judged to earn it:

- **`core/converter.py`** — the explicit example named in this session's
  brief: supersample-factor selection + Lanczos downscale + largest-first
  multi-frame ICO assembly is real geometry/math a diagram tells better
  than a straight read.
- **`core/shortcuts.py`** — matches two DOCS.md signals directly: "a
  background-thread or process handoff" (Python → temp JSON → PowerShell →
  COM) and "a protocol with ordered steps" (skip entries with no ICO yet,
  always clean up the temp file even on failure).
- **`gui/app.py`** — a genuinely multi-zone window (header/action-bar/
  table/log) PLUS a real background-thread handoff (`run_task` →
  `TaskWorker` → Qt signals back to the main thread); DOCS.md's own worked
  example ("an 86-line Qt widget is still Algorithmic") supports nature
  over line count here.

Everything else (`config.py`, `run.py`, `core/manifest.py`, `core/paths.py`,
`gui/theme.py`, `gui/worker.py`) was judged Standard — each is either
mostly linear/declarative or short enough that a diagram would only restate
the code. Full counts in the session's final report.

**Ask:** does the owner agree `shortcuts.py` and `gui/app.py` earn
Algorithmic, or should one/both be downgraded to Standard (delete the flow
doc, update `test_docs_coverage.py`'s `TIERS`)?

## 2. CONFIG_FILES scope: config.py only

`config.py` is seeded into `test_config_sections.py`'s `CONFIG_FILES` — it
is explicitly the project's single-source-of-truth config module (its own
docstring says so), with two clear sections (`LOCATIONS`, `RENDERING`).

`gui/theme.py`'s `TOKENS` dict was considered and left OUT: it is one flat,
already-atomic 14-key dict with no history of being patched from elsewhere
in the file, and root `rules/CODE.md` explicitly says to keep the seed
narrow ("a file that is mostly algorithm with one small table stays out").
`theme.py` is arguably the *opposite* case — mostly data, not algorithm —
but its data is a single unpatchable literal, so there is no post-definition
patching failure mode to guard against yet.

**Ask:** does the owner want `gui/theme.py` seeded into `CONFIG_FILES`
pre-emptively, or left out until (if ever) it grows a second table?

## 3. config.py banner style: dash comments converted to canonical form

`config.py` already had two section comments (`# --- Locations ---...`,
`# --- Rendering ---...`) using dashes. Root `rules/CODE.md`'s Config
Section Law canonical banner requires a run of **8+ `=`/box-drawing**
characters specifically — a dash-only banner is invisible to the guard's
regex (`(=|═){8,}`). Both comments were rewritten to the canonical
`# ═══ SECTION ═══` form as part of installing the guard — a comment-only
edit, explicitly allowed by `MIGRATE-DOCS.md`'s Hard Constraint #1, zero
behavior change (verified: compile + import baseline unchanged before and
after).

**Ask:** none — flagged for visibility only, since it is a source-file edit
even though it changes no behavior.

## 4. write_shortcuts.ps1 stays Trivial tier, outside the .py-scoped guards

`write_shortcuts.ps1` (26 lines) is a real source file but the project's
guard tests scope `SUFFIXES` to `.py` for the docs-coverage and
config-sections guards, matching the monorepo's existing reference
implementation (`Gadgets/Ultra Vivid/tests/`) — DOCS.md's tier system and
templates are written for a single-language project's dominant stack. It
IS included in `test_structure_law.py`'s scan (added `.ps1` to that guard's
`SUFFIXES`, since god-files are a cross-language risk and the check costs
nothing). Its logic stays described inside `core/___core.md` and
`core/__about/shortcuts.md`/`__flow/shortcuts.md` (its only caller) rather
than getting its own `__about/write_shortcuts.md` — this matches the
project's pre-existing convention (the legacy `core/___core.md` already
said "No individual `.md` — a generated helper described here").

**Ask:** none — flagged for visibility; revisit if the script grows real
branching logic of its own.

## 5. Stale `root Rule #N` references left untouched in source comments

Five source files still cite the OLD numbered-rule scheme in comments/
docstrings: `config.py` ("root Rule #4"), `gui/worker.py` ("root Rule
#10"), `gui/theme.py` ("root Rule #16"), `core/converter.py` ("root Rule
#5"), and `.gitignore` ("root Rule #18"). The root constitution moved rules
out of `CLAUDE.md` into named laws inside `rules/*.md` — these numbers no
longer resolve to anything. All `.md` documentation written or touched this
session was updated to the new named-reference form (e.g. `root
rules/CODE.md → No Hardcoded Values`); these five source-file comments were
deliberately left AS-IS, since `MIGRATE-DOCS.md`'s Hard Constraint #1 only
authorizes two categories of source edit this session (config-law section
banners; `.md` path references broken by the migration) and a stale
rule-number citation is neither.

**Ask:** should a follow-up pass update these five comments to the named-law
form too (comment-only, zero behavior change), or leave them since they
still convey the right idea even with a dead number?
