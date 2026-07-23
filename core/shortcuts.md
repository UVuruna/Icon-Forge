# Shortcuts

**Script:** [Shortcuts (script)](shortcuts.py)

## Purpose
Create/update the desktop `.lnk` shortcuts so each opens its folder in VS Code
with its own generated ICO.

## Flow (pseudocode)
```
ready   = entries whose ICO exists
skipped = entries whose ICO is missing
FOR each ready entry → build spec {path, target=VSCode, args="folder",
                                   workdir, icon="ico,0", existed?}
write specs to a temp JSON
run write_shortcuts.ps1 (PowerShell WScript.Shell) over the JSON
return {written, skipped, log}
```
Entries without an ICO are skipped and reported — their icon can't be set yet.

## Functions
- `sync_shortcuts(entries)` → `{written, skipped, log}`

## Connections
### Uses
- [Config](../config.md) — `VSCODE_EXE`, `DESKTOP_DIR`, `SHORTCUT_SCRIPT`
- `write_shortcuts.ps1` — the actual `.lnk` writer (see [Core](___core.md))
### Used by
- [CLI Runner](../run.md), [GUI Worker](../gui/worker.md)
