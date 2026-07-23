"""Load and merge the entry manifests into resolved `Entry` objects.

`manifest.json` is tracked; `manifest.local.json` (hidden projects) is
gitignored and merged in only if present.
"""

import json
from dataclasses import dataclass
from pathlib import Path

from config import MANIFEST, MANIFEST_LOCAL, DESKTOP_DIR, ICO_DIR
from core.paths import resolve_svg, resolve_target


@dataclass
class Entry:
    name: str
    kind: str            # "root" | "project"
    svg: Path            # resolved source SVG/PNG (may not exist yet)
    ico: Path            # output ICO path
    target: Path         # folder the shortcut opens
    shortcut: Path       # .lnk path under the desktop folder
    local: bool = False  # from manifest.local.json (hidden)

    @property
    def svg_exists(self) -> bool:
        return self.svg.is_file()

    @property
    def ico_exists(self) -> bool:
        return self.ico.is_file()

    @property
    def shortcut_exists(self) -> bool:
        return self.shortcut.is_file()

    @property
    def target_exists(self) -> bool:
        return self.target.is_dir()


def _build(raw: dict, kind: str, local: bool) -> Entry:
    return Entry(
        name=raw["name"],
        kind=kind,
        local=local,
        svg=resolve_svg(raw["svg"]),
        ico=ICO_DIR / f'{raw["ico"]}.ico',
        target=resolve_target(raw["target"]),
        shortcut=DESKTOP_DIR / raw["shortcut"],
    )


def load_entries() -> list[Entry]:
    """All entries: tracked roots + projects, then local (hidden) projects."""
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = [_build(r, "root", False) for r in data.get("roots", [])]
    entries += [_build(r, "project", False) for r in data.get("projects", [])]

    if MANIFEST_LOCAL.is_file():
        local = json.loads(MANIFEST_LOCAL.read_text(encoding="utf-8"))
        entries += [_build(r, "project", True) for r in local.get("projects", [])]

    return entries
