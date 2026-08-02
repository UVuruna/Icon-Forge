# tests/

Icon Forge's enforcement layer (root CODE.md → Enforcement): four guard
tests plus a fast runner wired into Claude Code hooks. `tests/` tier per
root DOCS.md — test modules get NO per-file `__about/`/`__flow/` docs, only
this folder doc.

This project has no separate behavioral test suite (small utility, no prior
automated tests) — these four guards ARE the project's `tests/` folder.

## Files

- **`test_structure_law.py`** — THE STRUCTURE LAW's guard. Fails the build
  if any `.py`/`.ps1` source file exceeds ~1,000 lines and is not in the
  `RATCHET` allowlist. `RATCHET` is empty: the largest file in this project
  is `gui/app.py` at 201 lines.
- **`test_config_sections.py`** — THE CONFIG SECTION LAW's guard. Checks
  only the files named in `CONFIG_FILES` (seeded with `config.py` — see
  [Open Questions](../OPEN-QUESTIONS.md) for the `gui/theme.py` judgment
  call) for definitions before the first section banner, duplicate dict
  keys, and post-definition table patching.
- **`test_docs_coverage.py`** — DOCS.md's tier guard. Encodes every source
  file's tier (`TIERS` dict) and asserts it has exactly the `__about/`/
  `__flow/` docs its tier requires — no more, no less.
- **`test_doc_links.py`** — DOCS.md's navigation-chain guard. Every project
  `.md` must be reachable from `README.md`, and no relative link may point
  at a file that does not exist.
- **`run_guards.py`** — fast wrapper for Claude Code hooks. `--fast` runs
  structure + config-sections only (PostToolUse, on every `Edit`/`Write`);
  no flag runs all four (Stop, before a session can end). Exits **2** on any
  failure — the exit code that makes a hook BLOCKING. Reads the PostToolUse
  hook JSON on stdin and exits 0 immediately for a non-`.py` file in
  `--fast` mode, so a docs-only session pays no guard cost per edit.

## Connections

### Used by
- `.claude/settings.json` — PostToolUse (`--fast`) and Stop (full) hooks

### Uses
- Every source file in the project (structure + config-section scan);
  every `.md` file in the project (docs coverage + link scan)
