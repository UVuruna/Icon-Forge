# Worker

**Script:** [Worker (script)](../worker.py)

## Purpose
Run batch work off the UI thread so the window stays responsive, streaming
progress lines back (root `rules/CODE.md` → Progress Logging for Long
Tasks).

## Classes

### TaskWorker(QThread)
Runs one task: `"icons"`, `"shortcuts"`, or `"all"`.

#### Signals
- `progress(str)` — one log line
- `finished_ok()` — task complete

#### Methods
- `run()` — loads entries once; for `"icons"`/`"all"` converts every entry
  with an existing source (emitting a line per entry, and a missing-source
  line for the rest); for `"shortcuts"`/`"all"` calls `sync_shortcuts` and
  re-emits its log line by line; always ends by emitting `finished_ok`.

## Connections
### Uses
- [Manifest](../../core/__about/manifest.md),
  [Converter](../../core/__about/converter.md),
  [Shortcuts](../../core/__about/shortcuts.md)
### Used by
- [App](app.md)
