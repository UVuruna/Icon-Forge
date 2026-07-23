# Worker

**Script:** [Worker (script)](worker.py)

## Purpose
Run batch work off the UI thread so the window stays responsive and streams
progress (root Rule #10).

## Classes

### TaskWorker(QThread)
Runs one task: `icons`, `shortcuts`, or `all`.

#### Signals
- `progress(str)` — one log line
- `finished_ok()` — task complete

#### run()
Loads entries, generates ICOs (for `icons`/`all`), syncs shortcuts (for
`shortcuts`/`all`), emitting progress throughout.

## Connections
### Uses
- [Manifest](../core/manifest.md), [Converter](../core/converter.md),
  [Shortcuts](../core/shortcuts.md)
### Used by
- [App](app.md)
