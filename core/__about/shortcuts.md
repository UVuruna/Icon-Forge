# Shortcuts

**Script:** [Shortcuts (script)](../shortcuts.py) ·
**Flow:** [diagram](../__flow/shortcuts.md)

## Purpose
Create/update the desktop `.lnk` shortcuts so each opens its folder in VS
Code with its own generated ICO. Never edits `.lnk` binary bytes itself —
delegates the actual write to `write_shortcuts.ps1` (WScript.Shell), the
dependency-free, reliable way to author Windows shortcuts.

## Functions
- `sync_shortcuts(entries)` — filters entries to those with an existing ICO
  (`ready`) vs not (`skipped`), writes one JSON spec per ready entry to a
  temp file, invokes `write_shortcuts.ps1` over it via `subprocess.run`, and
  returns `{written, skipped, log}`. Raises `RuntimeError` if the PowerShell
  process exits non-zero.
- `_spec(entry)` — internal: builds one shortcut spec dict (`path`, `target`
  = `VSCODE_EXE`, `args` = the quoted target folder, `workdir`, `icon` =
  `"{ico},0"`, `existed`).

## Connections
### Uses
- [Config](../../__about/config.md) — `VSCODE_EXE`, `DESKTOP_DIR`,
  `SHORTCUT_SCRIPT`
- `write_shortcuts.ps1` — the actual `.lnk` writer (a PowerShell helper
  called only from here; described in [Core (folder)](../___core.md) —
  Trivial tier, no own doc)
### Used by
- [CLI Runner](../../__about/run.md), [Worker](../../gui/__about/worker.md)
