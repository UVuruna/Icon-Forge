# Converter — Flow

**About:** [description](../__about/converter.md)

Earns its flow doc (root DOCS.md tier signal: "nontrivial geometry/math") —
the supersample-factor-per-size selection and the largest-first multi-frame
ICO assembly are not obvious from a single read of the code.

## Algorithm

```mermaid
%%{init: {'flowchart': {'subGraphTitleMargin': {'top': 0, 'bottom': 35}}}}%%
flowchart TB
    A[source file] --> B{suffix}
    B -- .svg --> C[QSvgRenderer]
    B -- raster --> D[Pillow.Image.open]
    C --> E[for each target size]
    D --> E
    E --> F{factor = supersample_factor size}
    F -- svg --> G[render at size × factor, AA + smooth transform]
    G --> H[Lanczos downscale to size]
    F -- raster --> I[Lanczos resize base image to size]
    H --> J{frame fully transparent?}
    I --> J
    J -- yes --> K[print WARNING]
    J -- no --> L[collect frame]
    K --> L
    L --> M{more sizes?}
    M -- yes --> E
    M -- no --> N[reverse frames — largest first]
    N --> O[(save one multi-frame .ico)]
```

Pseudocode (language-neutral):

    build a size -> image renderer for the source:
        IF suffix == .svg  -> QSvgRenderer (needs a live QGuiApplication)
        IF suffix in raster set -> open once with Pillow

    FOR each size in ICO_SIZES (config.py):
        factor = supersample_factor(size)   # 4x <=64px, 2x <=128px, else 1x
        IF svg:
            render at (size * factor), antialiased, smooth transform
            IF factor > 1: Lanczos-downscale render to (size, size)
        ELSE (raster):
            Lanczos-resize the already-open base image to (size, size)
        IF the frame's alpha extrema == (0, 0): warn "fully transparent"
        append frame

    reverse frame list (largest size first -- Windows shows it as primary)
    save all frames together as one multi-resolution .ico

`export_png` follows the same renderer-selection branch but stops after one
frame at `MAX_PNG` (512px, config.py) and saves it as a standalone PNG.
