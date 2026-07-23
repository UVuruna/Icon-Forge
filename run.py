"""Icon Forge — command-line entry point.

Usage:
    python run.py              # generate all ICOs, then sync shortcuts (default)
    python run.py icons        # only (re)generate ICOs from sources
    python run.py shortcuts    # only create/update desktop shortcuts
    python run.py status       # show source/ICO/shortcut status per entry
    python run.py convert SRC [--out DIR] [--png]   # one-off SVG/PNG -> ICO
    python run.py gui          # launch the GUI
"""

import argparse
import sys
from pathlib import Path

from config import ICO_DIR, MAX_PNG
from core.converter import convert_to_ico, export_png
from core.manifest import Entry, load_entries
from core.shortcuts import sync_shortcuts


def generate_icons(entries: list[Entry]) -> tuple[int, list[str]]:
    """Render an ICO for every entry with an existing source. Returns
    (generated_count, list of names whose source SVG is missing)."""
    generated = 0
    missing = []
    for e in entries:
        if not e.svg_exists:
            missing.append(e.name)
            print(f"  MISSING source  {e.name}  ->  {e.svg}")
            continue
        convert_to_ico(e.svg, e.ico)
        generated += 1
        print(f"  ok  {e.ico.name:<26} <- {e.svg.name}")
    return generated, missing


def cmd_icons(entries: list[Entry]) -> None:
    print(f"Generating ICOs into {ICO_DIR}")
    generated, missing = generate_icons(entries)
    print(f"\nGenerated {generated} ICO(s); {len(missing)} missing source(s).")


def cmd_shortcuts(entries: list[Entry]) -> None:
    print("Syncing desktop shortcuts")
    result = sync_shortcuts(entries)
    if result["log"]:
        print(result["log"])
    print(f"\nWrote {result['written']} shortcut(s).")
    if result["skipped"]:
        print(f"Skipped (no ICO yet): {', '.join(result['skipped'])}")


def cmd_all(entries: list[Entry]) -> None:
    cmd_icons(entries)
    print()
    cmd_shortcuts(entries)


def cmd_status(entries: list[Entry]) -> None:
    def mark(ok: bool) -> str:
        return "OK " if ok else " - "

    print(f"{'ENTRY':<24} {'KIND':<8} SVG ICO LNK TARGET")
    print("-" * 60)
    for e in entries:
        tag = e.name + (" *" if e.local else "")
        print(
            f"{tag:<24} {e.kind:<8} "
            f"{mark(e.svg_exists)} {mark(e.ico_exists)} "
            f"{mark(e.shortcut_exists)} {mark(e.target_exists)}"
        )
    print("\n* = local-only (hidden) entry")


def cmd_convert(args: argparse.Namespace) -> None:
    src = Path(args.src).resolve()
    out_dir = Path(args.out).resolve() if args.out else ICO_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    ico = out_dir / f"{src.stem}.ico"
    convert_to_ico(src, ico)
    print(f"ICO  -> {ico}")

    if args.png:
        png = out_dir / f"{src.stem}_{MAX_PNG}.png"
        export_png(src, png)
        print(f"PNG  -> {png}")


def cmd_gui() -> None:
    from gui.app import main as gui_main
    gui_main()


def main() -> None:
    parser = argparse.ArgumentParser(description="Icon Forge")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("all", help="generate ICOs then sync shortcuts (default)")
    sub.add_parser("icons", help="generate ICOs only")
    sub.add_parser("shortcuts", help="sync desktop shortcuts only")
    sub.add_parser("status", help="show status per entry")
    sub.add_parser("gui", help="launch the GUI")

    p_conv = sub.add_parser("convert", help="one-off SVG/PNG -> ICO")
    p_conv.add_argument("src")
    p_conv.add_argument("--out", help="output directory (default: ico/)")
    p_conv.add_argument("--png", action="store_true", help=f"also export {MAX_PNG}px PNG")

    args = parser.parse_args()
    command = args.command or "all"

    if command == "convert":
        cmd_convert(args)
        return
    if command == "gui":
        cmd_gui()
        return

    entries = load_entries()
    {
        "all": cmd_all,
        "icons": cmd_icons,
        "shortcuts": cmd_shortcuts,
        "status": cmd_status,
    }[command](entries)


if __name__ == "__main__":
    sys.exit(main())
