"""Background task worker — keeps the UI responsive during batch work
(root Rule #10: progress visibility for long operations)."""

from PySide6.QtCore import QThread, Signal

from core.converter import convert_to_ico
from core.manifest import load_entries
from core.shortcuts import sync_shortcuts


class TaskWorker(QThread):
    """Runs one of: 'icons', 'shortcuts', 'all'. Streams progress lines."""

    progress = Signal(str)
    finished_ok = Signal()

    def __init__(self, task: str):
        super().__init__()
        self.task = task

    def run(self) -> None:
        entries = load_entries()

        if self.task in ("icons", "all"):
            self.progress.emit("Generating ICOs …")
            generated, missing = 0, 0
            for e in entries:
                if not e.svg_exists:
                    missing += 1
                    self.progress.emit(f"  MISSING source  {e.name}")
                    continue
                convert_to_ico(e.svg, e.ico)
                generated += 1
                self.progress.emit(f"  ok  {e.ico.name} ← {e.svg.name}")
            self.progress.emit(f"→ {generated} ICO(s), {missing} missing source(s).\n")

        if self.task in ("shortcuts", "all"):
            self.progress.emit("Syncing desktop shortcuts …")
            result = sync_shortcuts(entries)
            for line in result["log"].splitlines():
                self.progress.emit(line)
            self.progress.emit(f"→ {result['written']} shortcut(s) written.")
            if result["skipped"]:
                self.progress.emit(f"  skipped (no ICO): {', '.join(result['skipped'])}")

        self.finished_ok.emit()
