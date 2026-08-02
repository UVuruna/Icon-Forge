# Shortcuts — Flow

**About:** [description](../__about/shortcuts.md)

Earns its flow doc (root DOCS.md tier signals: "a process handoff" and "a
protocol with ordered steps") — the work crosses a process boundary
(Python -> temp JSON file -> PowerShell -> COM) and the ordering (skip
entries with no ICO yet, always clean up the temp file) is easy to get
wrong by re-reading only the code.

## Algorithm

```mermaid
%%{init: {'flowchart': {'subGraphTitleMargin': {'top': 0, 'bottom': 35}}}}%%
flowchart TB
    A[entries] --> B{ico_exists?}
    B -- no --> C[add to skipped]
    B -- yes --> D[build spec: path, target=VSCode, args, workdir, icon, existed]
    D --> E[collect into ready specs]
    C --> F{any ready?}
    E --> F
    F -- no --> G[return written=0, skipped, log='']
    F -- yes --> H[write specs as JSON to a temp file]
    H --> I[run write_shortcuts.ps1 -Json tmp via subprocess]
    I --> J{exit code == 0?}
    J -- no --> K[raise RuntimeError with stderr]
    J -- yes --> L[return written, skipped, log=stdout]
    K --> M[[finally: delete temp file]]
    L --> M
```

Pseudocode (language-neutral):

    ready   = entries whose ICO file exists
    skipped = entries whose ICO file does not exist yet (name recorded)
    IF ready is empty: RETURN {written: 0, skipped, log: ""}

    ensure the desktop shortcut folder exists
    specs = [build_spec(e) for e in ready]     # one dict per shortcut

    write specs as JSON to a fresh temp file
    TRY:
        run write_shortcuts.ps1 (PowerShell, WScript.Shell COM) over the
        temp file's path
        IF the process exit code != 0: raise with its stderr
        RETURN {written: len(ready), skipped, log: process stdout}
    FINALLY:
        delete the temp file (always, even on raise)

`write_shortcuts.ps1` itself, per spec: ensure the shortcut's parent folder
exists, `CreateShortcut`, set TargetPath/Arguments/WorkingDirectory/
IconLocation, `Save()`, print `created`/`updated`.
