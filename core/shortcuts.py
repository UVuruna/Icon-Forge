"""Create/update the VSCode quick-open .lnk shortcuts on the desktop.

Delegates the actual .lnk write to `write_shortcuts.ps1` via PowerShell's
`WScript.Shell` COM object — the reliable, dependency-free way to author
Windows shortcuts. This module only builds the specs and reports the result.
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path

from config import VSCODE_EXE, SHORTCUT_SCRIPT, DESKTOP_DIR
from core.manifest import Entry


def _spec(entry: Entry) -> dict:
    return {
        "path": str(entry.shortcut),
        "target": str(VSCODE_EXE),
        "args": f'"{entry.target}"',
        "workdir": str(entry.target),
        "icon": f"{entry.ico},0",
        "existed": entry.shortcut_exists,
    }


def sync_shortcuts(entries: list[Entry]) -> dict:
    """Write/update a .lnk for every entry whose ICO exists. Entries missing
    their ICO are skipped and reported (their icon cannot be set yet)."""
    ready = [e for e in entries if e.ico_exists]
    skipped = [e.name for e in entries if not e.ico_exists]

    if not ready:
        return {"written": 0, "skipped": skipped, "log": ""}

    DESKTOP_DIR.mkdir(parents=True, exist_ok=True)
    specs = [_spec(e) for e in ready]

    fd, tmp = tempfile.mkstemp(suffix=".json", prefix="iconforge_")
    os.close(fd)
    tmp_path = Path(tmp)
    try:
        tmp_path.write_text(json.dumps(specs, ensure_ascii=False), encoding="utf-8")
        proc = subprocess.run(
            [
                "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                "-File", str(SHORTCUT_SCRIPT), "-Json", str(tmp_path),
            ],
            capture_output=True, text=True,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"Shortcut writer failed:\n{proc.stderr.strip()}")
        return {"written": len(ready), "skipped": skipped, "log": proc.stdout.strip()}
    finally:
        tmp_path.unlink(missing_ok=True)
