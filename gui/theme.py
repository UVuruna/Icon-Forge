"""Icon Forge theme — dark-first, single indigo accent (root Rule #16, DESIGN.md).

All colors are tokens here, never literals in the widgets (root Rule #4).
"""

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QWidget

# --- Tokens ----------------------------------------------------------------

TOKENS = {
    "surface-0": "#16161f",
    "surface-1": "#1e1e28",
    "surface-2": "#262633",
    "surface-3": "#2f2f3d",
    "border": "rgba(255, 255, 255, 0.10)",
    "text": "#f5f5f5",
    "text-2": "#a0a0b5",
    "accent": "#6366f1",
    "accent-dark": "#4f46e5",
    "accent-light": "#818cf8",
    "success": "#22c55e",
    "warning": "#f59e0b",
    "error": "#ef4444",
}

QSS = """
QWidget {{
    background: {surface-0};
    color: {text};
    font-family: 'Inter', 'Segoe UI', sans-serif;
    font-size: 14px;
}}
#Card {{
    background: {surface-1};
    border: 1px solid {border};
    border-radius: 16px;
}}
#Title {{ font-size: 22px; font-weight: 700; }}
#Subtitle {{ color: {text-2}; font-size: 13px; }}

QPushButton {{
    background: {surface-2};
    border: 1px solid {border};
    border-radius: 8px;
    padding: 9px 16px;
    color: {text};
    font-weight: 600;
}}
QPushButton:hover {{ background: {surface-3}; }}
QPushButton:pressed {{ background: {surface-1}; }}

QPushButton#Primary {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
               stop:0 {accent-light}, stop:1 {accent-dark});
    border: none;
}}
QPushButton#Primary:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
               stop:0 {accent}, stop:1 {accent-dark});
}}
QPushButton#Primary:pressed {{ background: {accent-dark}; }}

QTableWidget {{
    background: {surface-1};
    border: none;
    gridline-color: transparent;
    outline: none;
}}
QTableWidget::item {{
    padding: 4px 8px;
    border-bottom: 1px solid {border};
}}
QTableWidget::item:selected {{ background: {surface-3}; color: {text}; }}
QHeaderView::section {{
    background: {surface-1};
    color: {text-2};
    border: none;
    border-bottom: 1px solid {border};
    padding: 8px;
    font-weight: 600;
    text-align: left;
}}
QTableCornerButton::section {{ background: {surface-1}; border: none; }}

QPlainTextEdit {{
    background: {surface-0};
    border: 1px solid {border};
    border-radius: 12px;
    padding: 10px;
    color: {text-2};
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 12px;
}}
QScrollBar:vertical {{ background: transparent; width: 10px; margin: 2px; }}
QScrollBar::handle:vertical {{ background: {surface-3}; border-radius: 5px; min-height: 30px; }}
QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; }}
"""


def stylesheet() -> str:
    return QSS.format(**TOKENS)


def apply_shadow(widget: QWidget, blur: int = 28, alpha: int = 60,
                 dy: int = 8, color: str | None = None) -> None:
    """Soft ambient shadow (DESIGN.md depth spec). Glow = color + dy 0."""
    effect = QGraphicsDropShadowEffect(widget)
    effect.setBlurRadius(blur)
    effect.setOffset(0, dy)
    qc = QColor(color) if color else QColor(0, 0, 0)
    qc.setAlpha(alpha)
    effect.setColor(qc)
    widget.setGraphicsEffect(effect)
