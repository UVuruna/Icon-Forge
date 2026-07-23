"""Path resolution for manifest entries.

SVG sources come from two roots: the project's own `sources/` and the monorepo
`logos/`. Targets are always relative to the monorepo root.
"""

from pathlib import Path

from config import PROJECT_DIR, MONOREPO_ROOT


def resolve_svg(rel: str) -> Path:
    """Resolve a manifest 'svg' path. Tries the project dir first (own
    sources), then the monorepo root (shared logos). Returns the project-dir
    candidate if neither exists, so the caller can report it as missing."""
    for base in (PROJECT_DIR, MONOREPO_ROOT):
        candidate = base / rel
        if candidate.exists():
            return candidate
    return PROJECT_DIR / rel


def resolve_target(rel: str) -> Path:
    """Resolve a manifest 'target' (folder the shortcut opens) against the
    monorepo root. '.' means the monorepo root itself."""
    if rel in (".", ""):
        return MONOREPO_ROOT
    return MONOREPO_ROOT / rel
