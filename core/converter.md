# Converter

**Script:** [Converter (script)](converter.py)

## Purpose
Render a source image into a multi-resolution ICO, or a single high-res PNG.

## Algorithm (pseudocode)
```
build a size→image renderer for the source:
    IF .svg → QSvgRenderer; render at size×factor, Lanczos-downscale to size
    IF raster → open once, resize to each size with Lanczos
FOR each size in ICO_SIZES:
    render frame; warn if fully transparent
save frames (largest first) as one .ico
```

## Functions
- `convert_to_ico(src, ico, sizes=ICO_SIZES)` → writes the ICO, returns its path
- `export_png(src, png, size=MAX_PNG)` → writes a single PNG
- `_master_renderer(src)` → the size→image callable (SVG or raster)

## Connections
### Uses
- [Config](../config.md) — `ICO_SIZES`, `MAX_PNG`, `supersample_factor`
### Used by
- [CLI Runner](../run.md), [GUI Worker](../gui/worker.md), [App](../gui/app.md)
