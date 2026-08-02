"""
Icon Forge — configuration (single source of truth for paths and tunables).

Machine-specific locations are DERIVED from the environment where possible
(root Rule #4: no hardcoded values). Anything the owner may want to change
lives here, never inline in the modules.
"""

import os
from pathlib import Path

# ═══════════════════════════ LOCATIONS ═══════════════════════════

# This project's own folder: .../UVuruna/Gadgets/Icon Forge
PROJECT_DIR = Path(__file__).resolve().parent

# The monorepo root: two levels up (Gadgets/Icon Forge -> UVuruna). Derived,
# not hardcoded, so the tool follows the repo wherever it is cloned.
MONOREPO_ROOT = PROJECT_DIR.parents[1]

# Where the project logo SVGs live (single source of truth for logos).
LOGOS_DIR = MONOREPO_ROOT / "logos"

# Generated ICO output (gitignored — computed, never stored; root Rule #19).
ICO_DIR = PROJECT_DIR / "ico"

# Source SVGs owned by this tool (root-category icons, etc).
SOURCES_DIR = PROJECT_DIR / "sources"

# Local-only sources (hidden projects) — gitignored, never pushed.
SOURCES_LOCAL_DIR = PROJECT_DIR / "sources_local"

# The desktop folder of VSCode quick-open shortcuts this tool maintains.
# Default derives from the user profile; override with the ICON_FORGE_DESKTOP
# environment variable if OneDrive is not in the path.
_default_desktop = Path(
    os.environ.get("USERPROFILE", str(Path.home()))
) / "OneDrive" / "Desktop" / "VSCode Projects"
DESKTOP_DIR = Path(os.environ.get("ICON_FORGE_DESKTOP", str(_default_desktop)))

# The editor each shortcut launches. Derived from LOCALAPPDATA; override with
# ICON_FORGE_VSCODE if VS Code is installed elsewhere.
_default_vscode = Path(
    os.environ.get("LOCALAPPDATA", "")
) / "Programs" / "Microsoft VS Code" / "Code.exe"
VSCODE_EXE = Path(os.environ.get("ICON_FORGE_VSCODE", str(_default_vscode)))

# Manifests (data — the entry list; separate from this code config).
MANIFEST = PROJECT_DIR / "manifest.json"
MANIFEST_LOCAL = PROJECT_DIR / "manifest.local.json"  # hidden projects; optional

# PowerShell helper that actually writes the .lnk files.
SHORTCUT_SCRIPT = PROJECT_DIR / "core" / "write_shortcuts.ps1"

# ═══════════════════════════ RENDERING ═══════════════════════════

# ICO frames. Windows Explorer uses up to 256 for shell icons — that is the
# real cap for a .lnk icon, so the ICO tops out at 256. Larger raster is
# exported separately as PNG (see MAX_PNG).
ICO_SIZES = [16, 32, 48, 64, 128, 256]

# Largest raster the converter will emit as a standalone PNG (owner: max 512).
MAX_PNG = 512

# Supersample factor per target size — higher for small icons where the
# Lanczos downscale buys the most sharpness.
def supersample_factor(size: int) -> int:
    if size <= 64:
        return 4
    if size <= 128:
        return 2
    return 1
