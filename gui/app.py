"""Icon Forge — GUI control panel.

A single window: header, action bar, an entries table (thumbnail + status),
and a live log. Launch with `python run.py gui` or `python -m gui.app`.
"""

import sys
from pathlib import Path

# Allow `python -m gui.app` and direct execution to find `config`/`core`.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QImage, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QApplication, QFileDialog, QHBoxLayout, QHeaderView, QLabel,
    QPlainTextEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget,
)

from config import ICO_DIR, MAX_PNG, PROJECT_DIR
from core.converter import convert_to_ico, export_png
from core.manifest import Entry, load_entries
from gui.theme import TOKENS, apply_shadow, stylesheet
from gui.worker import TaskWorker

LOGO = PROJECT_DIR / "assets" / "logo.svg"
THUMB = 34


def svg_pixmap(path: Path, size: int) -> QPixmap:
    """Render an SVG (or ICO) to a transparent QPixmap."""
    if path.suffix.lower() == ".svg" and path.is_file():
        renderer = QSvgRenderer(str(path))
        image = QImage(size, size, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.transparent)
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        renderer.render(painter)
        painter.end()
        return QPixmap.fromImage(image)
    if path.is_file():
        return QIcon(str(path)).pixmap(size, size)
    return QPixmap(size, size)


def dot(ok: bool) -> QTableWidgetItem:
    item = QTableWidgetItem("●" if ok else "—")
    item.setForeground(Qt.GlobalColor.transparent)  # replaced below
    from PySide6.QtGui import QColor
    item.setForeground(QColor(TOKENS["success"] if ok else TOKENS["text-2"]))
    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    item.setFlags(Qt.ItemFlag.ItemIsEnabled)
    return item


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Icon Forge")
        self.setWindowIcon(QIcon(str(LOGO)))
        self.resize(760, 620)
        self.worker: TaskWorker | None = None

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(16)

        root.addWidget(self._header())
        root.addWidget(self._action_bar())
        self.table = self._build_table()
        root.addWidget(self.table, 1)
        self.log = QPlainTextEdit(readOnly=True)
        self.log.setFixedHeight(150)
        root.addWidget(self.log)

        self.refresh_table()

    # --- sections ----------------------------------------------------------

    def _header(self) -> QWidget:
        card = QWidget(objectName="Card")
        apply_shadow(card)
        row = QHBoxLayout(card)
        row.setContentsMargins(18, 14, 18, 14)

        logo = QLabel()
        logo.setPixmap(svg_pixmap(LOGO, 44))
        row.addWidget(logo)

        text = QVBoxLayout()
        text.setSpacing(2)
        text.addWidget(QLabel("Icon Forge", objectName="Title"))
        text.addWidget(QLabel(
            "SVG / PNG → ICO · VSCode quick-open shortcut icons", objectName="Subtitle"))
        row.addLayout(text)
        row.addStretch(1)
        return card

    def _action_bar(self) -> QWidget:
        bar = QWidget()
        row = QHBoxLayout(bar)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(10)

        self.btn_all = QPushButton("Generate + Sync", objectName="Primary")
        self.btn_all.clicked.connect(lambda: self.run_task("all"))
        apply_shadow(self.btn_all, blur=22, alpha=90, dy=4, color=TOKENS["accent"])

        self.btn_icons = QPushButton("Generate ICOs")
        self.btn_icons.clicked.connect(lambda: self.run_task("icons"))

        self.btn_shortcuts = QPushButton("Sync Shortcuts")
        self.btn_shortcuts.clicked.connect(lambda: self.run_task("shortcuts"))

        self.btn_convert = QPushButton("Convert File…")
        self.btn_convert.clicked.connect(self.convert_file)

        for b in (self.btn_all, self.btn_icons, self.btn_shortcuts, self.btn_convert):
            row.addWidget(b)
        row.addStretch(1)
        return bar

    def _build_table(self) -> QTableWidget:
        table = QTableWidget(0, 5)
        table.setHorizontalHeaderLabels(["Entry", "Kind", "SVG", "ICO", "LNK"])
        table.verticalHeader().setVisible(False)
        table.setIconSize(QSize(THUMB, THUMB))
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setShowGrid(False)
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for c in range(1, 5):
            header.setSectionResizeMode(c, QHeaderView.ResizeMode.ResizeToContents)
        table.verticalHeader().setDefaultSectionSize(THUMB + 12)
        return table

    # --- data --------------------------------------------------------------

    def refresh_table(self) -> None:
        entries = load_entries()
        self.table.setRowCount(len(entries))
        for r, e in enumerate(entries):
            name = QTableWidgetItem(e.name + ("  ·hidden" if e.local else ""))
            name.setIcon(QIcon(svg_pixmap(e.svg, THUMB)))
            self.table.setItem(r, 0, name)
            kind = QTableWidgetItem(e.kind)
            kind.setForeground(Qt.GlobalColor.gray)
            self.table.setItem(r, 1, kind)
            self.table.setItem(r, 2, dot(e.svg_exists))
            self.table.setItem(r, 3, dot(e.ico_exists))
            self.table.setItem(r, 4, dot(e.shortcut_exists))

    # --- actions -----------------------------------------------------------

    def _set_busy(self, busy: bool) -> None:
        for b in (self.btn_all, self.btn_icons, self.btn_shortcuts, self.btn_convert):
            b.setEnabled(not busy)

    def run_task(self, task: str) -> None:
        if self.worker and self.worker.isRunning():
            return
        self._set_busy(True)
        self.log.clear()
        self.worker = TaskWorker(task)
        self.worker.progress.connect(self.log.appendPlainText)
        self.worker.finished_ok.connect(self._task_done)
        self.worker.start()

    def _task_done(self) -> None:
        self._set_busy(False)
        self.refresh_table()
        self.log.appendPlainText("\nDone.")

    def convert_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Choose an SVG or PNG", "",
            "Images (*.svg *.png *.jpg *.jpeg *.bmp *.webp)")
        if not path:
            return
        src = Path(path)
        ICO_DIR.mkdir(parents=True, exist_ok=True)
        ico = convert_to_ico(src, ICO_DIR / f"{src.stem}.ico")
        png = export_png(src, ICO_DIR / f"{src.stem}_{MAX_PNG}.png")
        self.log.clear()
        self.log.appendPlainText(f"ICO → {ico}")
        self.log.appendPlainText(f"PNG → {png}")


def main() -> None:
    app = QApplication.instance() or QApplication(sys.argv)
    app.setStyleSheet(stylesheet())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
