"""SVG/PNG -> ICO (and PNG) conversion engine.

SVG is rendered with an anti-aliased QPainter and a supersampled Lanczos
downscale for crisp results at every size (same proven approach as the build
pipelines' `svg_to_ico.py` — root Rule #5). Raster input (PNG/JPG) is resized
directly with Lanczos.
"""

import sys
from collections.abc import Callable
from pathlib import Path

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QGuiApplication, QImage, QPainter
from PySide6.QtSvg import QSvgRenderer
from PIL import Image

from config import ICO_SIZES, MAX_PNG, supersample_factor

_app: QGuiApplication | None = None

RASTER_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"}


def _ensure_qt_app() -> None:
    """QSvgRenderer needs a QGuiApplication instance to exist."""
    global _app
    if QGuiApplication.instance() is None:
        _app = QGuiApplication(sys.argv[:1])


def _render_svg(renderer: QSvgRenderer, size: int) -> Image.Image:
    factor = supersample_factor(size)
    render_size = size * factor

    qimage = QImage(QSize(render_size, render_size), QImage.Format.Format_ARGB32)
    qimage.fill(Qt.GlobalColor.transparent)

    painter = QPainter(qimage)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    renderer.render(painter)
    painter.end()

    img = Image.frombytes(
        "RGBA", (render_size, render_size), qimage.bits().tobytes(), "raw", "BGRA"
    )
    if factor > 1:
        img = img.resize((size, size), Image.Resampling.LANCZOS)
    return img


def _master_renderer(src: Path) -> Callable[[int], Image.Image]:
    """Return a `size -> RGBA Image` renderer for the source file."""
    suffix = src.suffix.lower()

    if suffix == ".svg":
        _ensure_qt_app()
        renderer = QSvgRenderer(str(src))
        if not renderer.isValid():
            raise RuntimeError(f"Invalid SVG: {src}")
        return lambda size: _render_svg(renderer, size)

    if suffix in RASTER_SUFFIXES:
        base = Image.open(src).convert("RGBA")
        return lambda size: base.resize((size, size), Image.Resampling.LANCZOS)

    raise ValueError(f"Unsupported source type '{suffix}': {src}")


def convert_to_ico(src: Path, ico: Path, sizes: list[int] | None = None) -> Path:
    """Render `src` into a multi-resolution ICO at `ico`. Returns the ICO path."""
    if not src.is_file():
        raise FileNotFoundError(f"Source not found: {src}")

    sizes = sizes or ICO_SIZES
    render = _master_renderer(src)

    frames = []
    for size in sizes:
        frame = render(size)
        if frame.getextrema()[3] == (0, 0):
            print(f"  WARNING: {src.name} {size}x{size} frame is fully transparent")
        frames.append(frame)

    frames.reverse()  # largest first — Windows uses it as the primary
    ico.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(str(ico), format="ICO", append_images=frames[1:])
    return ico


def export_png(src: Path, png: Path, size: int = MAX_PNG) -> Path:
    """Render `src` to a single high-resolution PNG (owner: up to 512x512)."""
    if not src.is_file():
        raise FileNotFoundError(f"Source not found: {src}")
    render = _master_renderer(src)
    png.parent.mkdir(parents=True, exist_ok=True)
    render(size).save(str(png), format="PNG")
    return png
