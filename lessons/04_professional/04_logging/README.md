# 4.4 Logging

## What you'll learn

- Why `logging` beats `print` for anything that runs unattended
- `logging.basicConfig(...)` and `logging.getLogger(__name__)`
- The five levels and how filtering works
- Lazy `%s` formatting: `log.info("started %s", name)`
- `log.exception(...)` to record a traceback
- Logger hierarchy, handlers and a `FileHandler`

## Explanation

### Setup once, log everywhere

```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)
```

`basicConfig` configures the **root** logger: its level, format and a handler
(console by default). Call it once, in your program's entry point. Libraries
should only call `getLogger(__name__)` and never configure logging, so the
application stays in control.

`__name__` gives each module its own logger (`myapp.db`, `myapp.http`), so the
log shows where each message came from.

### Levels

| Level | Value | Use for |
|---|---|---|
| `DEBUG` | 10 | Detailed diagnostics |
| `INFO` | 20 | Normal progress ("started", "saved 3 files") |
| `WARNING` | 30 | Something unexpected, still working (the default level) |
| `ERROR` | 40 | An operation failed |
| `CRITICAL` | 50 | The program may not continue |

A record is emitted only if its level is at least the logger's (effective) level.

### Lazy formatting

```python
log.info("started %s", name)     # good: string built only if emitted
log.debug(f"state {big_dict}")   # wasteful: built even when DEBUG is off
```

Passing arguments separately also lets log tools group identical messages.

### Logging exceptions

```python
try:
    risky()
except Exception:
    log.exception("failed")      # ERROR level + full traceback
```

### Hierarchy and handlers

Logger names are dotted: `myapp.db` is a child of `myapp`, which is a child of
the root. Records travel up to parent handlers (`propagate`), so one handler on
the root sees everything. Set a level on a parent to quiet a whole subtree:

```python
logging.getLogger("urllib3").setLevel(logging.WARNING)
```

Handlers decide *where* records go; formatters decide *how* they look:

```python
handler = logging.FileHandler("app.log", encoding="utf-8")
handler.setFormatter(logging.Formatter("%(levelname)s|%(name)s|%(message)s"))
log.addHandler(handler)
```

`RotatingFileHandler` / `TimedRotatingFileHandler` (in `logging.handlers`) stop
log files from growing forever.

## Common mistakes

- Using `print` for diagnostics - you can't turn it off or redirect it per module.
- Calling `basicConfig` in a library, or calling it twice (the second call does
  nothing unless `force=True`).
- `log.info("x =", x)` - missing `%s`, so formatting fails. Use `log.info("x = %s", x)`.
- `log.exception` outside an `except` block (there is no traceback to log).
- Logging secrets (passwords, tokens) - logs are often widely readable.
- Adding a handler every time a function runs, which duplicates every line.

## How to run

```bash
cd lessons/04_professional/04_logging
python example.py
```

## Try it yourself

1. Change the `basicConfig` level to `logging.WARNING`. Which lines disappear?
2. Add `%(funcName)s:%(lineno)d` to the format string.
3. Replace the `FileHandler` with a `RotatingFileHandler(path, maxBytes=200,
   backupCount=2)`, log 50 lines, and list the files created in the temp dir.
