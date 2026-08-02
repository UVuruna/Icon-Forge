# Converter

**Script:** [Converter (script)](../converter.py) ·
**Flow:** [diagram](../__flow/converter.md)

## Purpose
Render a source image (SVG or raster) into a multi-resolution ICO, or a
single high-resolution PNG. Same proven supersample-and-Lanczos render as
the monorepo build pipelines' `svg_to_ico.py` (root `rules/CODE.md` → No
Duplicate Code).

## Functions
- `convert_to_ico(src, ico, sizes=ICO_SIZES)` — renders every size in
  `sizes`, warns on a fully-transparent frame, saves one multi-frame `.ico`
  (largest frame first — the frame Windows shows as the primary). Returns
  the ICO path.
- `export_png(src, png, size=MAX_PNG)` — renders a single frame at `size`
  and saves it as PNG. Returns the PNG path.
- `_master_renderer(src)` — internal: returns a `size -> RGBA Image`
  callable for `src` (SVG via `QSvgRenderer`, raster via `Pillow.Image`).
- `_render_svg(renderer, size)` — internal: renders one SVG frame at a
  supersampled size, then Lanczos-downscales to `size`.
- `_ensure_qt_app()` — internal: `QSvgRenderer` needs a live
  `QGuiApplication`; creates a headless one if none exists yet.

## Connections
### Uses
- [Config](../../__about/config.md) — `ICO_SIZES`, `MAX_PNG`,
  `supersample_factor`
### Used by
- [CLI Runner](../../__about/run.md), [Worker](../../gui/__about/worker.md),
  [App](../../gui/__about/app.md)
