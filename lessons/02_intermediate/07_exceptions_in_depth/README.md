# Lesson 2.7 — Exceptions in depth

## What you'll learn

- Raising exceptions with `raise` and re-raising with a bare `raise`
- Building a custom exception hierarchy (`class AppError(Exception)`)
- Chaining errors with `raise NewErr(...) from e` (and `from None`)
- Catching several types with `except (A, B) as e:`
- Handling grouped errors with `ExceptionGroup` and `except*` (3.11+)
- Ignoring an expected error with `contextlib.suppress`

## Explanation

### raise

```python
if amount <= 0:
    raise ValueError(f"amount must be positive, got {amount}")
```

Raise the most fitting built-in type (`ValueError` for a bad value,
`TypeError` for a wrong type, `KeyError` for a missing key) with a helpful
message. Inside an `except` block, a bare `raise` re-raises the current
exception unchanged — useful after logging.

### Custom hierarchy

```python
class AppError(Exception): ...
class ConfigError(AppError): ...
class ValidationError(AppError):
    def __init__(self, field, message):
        super().__init__(f"{field}: {message}")
        self.field = field
```

One base class for your app lets callers write `except AppError` to catch all
of your errors without also catching unrelated bugs. Subclasses allow more
specific handling, and can carry extra data as attributes. Put the most
specific `except` clauses first.

### raise ... from ...

```python
except ValueError as e:
    raise ConfigError("port is not a number") from e
```

This translates a low-level error into one that makes sense to your callers
while keeping the original in `e.__cause__`; the traceback shows both. Use
`from None` to hide the original when it is just noise.

### Several types

`except (ValueError, ZeroDivisionError) as e:` handles either type with one
block. `else:` runs when no exception happened; `finally:` always runs.

### ExceptionGroup and except*

```python
raise ExceptionGroup("invalid records", [KeyError(...), TypeError(...)])

try: ...
except* KeyError as eg:   # eg.exceptions holds just the KeyErrors
    ...
except* TypeError as eg:
    ...
```

An `ExceptionGroup` carries several exceptions at once (batch validation,
`asyncio.TaskGroup`). Each `except*` clause handles the matching part of the
group, and — unlike normal `except` — several clauses can run for one group.

### contextlib.suppress

```python
with suppress(KeyError):
    del cache["missing"]
```

A readable replacement for `try: ... except KeyError: pass`. The rest of the
`with` block is skipped once the error occurs.

## Common mistakes

- Bare `except:` or `except Exception:` that swallows every bug silently.
- Catching a parent class before a child (`except AppError` above
  `except ValidationError`) — the child clause never runs.
- Raising a new exception inside `except` without `from e` when the cause
  matters, or losing the message entirely.
- Using exceptions for normal control flow where a simple `if` is clearer.
- Mixing `except` and `except*` in the same `try` (not allowed).
- Wrapping too much code in `suppress`, hiding real errors.

## How to run

```bash
python example.py
```

## Try it yourself

1. Create `class NotFoundError(AppError)` and a function `find_user(users, name)`
   that raises it, chaining from the underlying `KeyError`.
2. Write `parse_ints(strings)` that collects a `ValueError` for every bad
   string and raises them together in an `ExceptionGroup`; handle it with `except*`.
3. Use `suppress(ValueError)` to sum only the numeric items in
   `["1", "x", "3"]`.
