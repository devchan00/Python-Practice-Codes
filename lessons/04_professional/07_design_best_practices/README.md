# 4.7 Design and best practices

## What you'll learn

- PEP 8 (style) and PEP 20 (the Zen of Python - `import this`)
- EAFP over LBYL
- Composition over inheritance
- Type hints and docstrings on public APIs (and where pydantic fits)
- Dependency injection for testable code
- 12-factor config: environment variables, never hard-coded secrets

## Explanation

### PEP 8 and PEP 20

PEP 8 is the community style guide: 4-space indents, `snake_case` for
functions and variables, `PascalCase` for classes, `UPPER_CASE` for constants,
imports at the top. Don't memorise it - let `ruff format` / `black` apply it.

PEP 20 is the philosophy. Run `python -c "import this"`:
"Explicit is better than implicit. Simple is better than complex.
Readability counts. Errors should never pass silently..."

### EAFP over LBYL

```python
# LBYL - look before you leap
if "timeout" in config and config["timeout"].isdigit():
    timeout = int(config["timeout"])

# EAFP - easier to ask forgiveness than permission (Pythonic)
try:
    timeout = int(config["timeout"])
except (KeyError, ValueError):
    timeout = 30
```

EAFP is shorter, handles every failure path, and avoids races (a file can
disappear between `os.path.exists()` and `open()`). Always catch *specific*
exceptions.

### Composition over inheritance

```python
class Car:
    def __init__(self, engine):
        self.engine = engine          # Car HAS-A engine
```

Small objects that collaborate are easier to swap, test and understand than
deep class trees. Use inheritance for true "is-a" relationships.

### Type hints and docstrings

```python
def mean(values: list[float], *, default: float | None = None) -> float:
    """Return the arithmetic mean of ``values``.

    Raises:
        ValueError: If ``values`` is empty and no default is given.
    """
```

Hints document intent and power mypy, pyright and IDE autocompletion; they
are not checked at runtime. Docstrings (Google, NumPy or reST style) show up in
`help()` and generated docs. For **runtime** validation from hints, the
third-party **pydantic** library (`pip install pydantic`) is the standard choice:

```python
from pydantic import BaseModel
class User(BaseModel):
    name: str
    age: int
User(name="Ada", age="36")   # age becomes 36; age="old" raises ValidationError
```

### Dependency injection

```python
class SignupService:
    def __init__(self, notifier):   # passed in, not created inside
        self.notifier = notifier
```

In production pass a real `EmailNotifier`; in tests pass a `FakeNotifier` that
records calls. No patching, no real emails. A `typing.Protocol` describes what
the collaborator must provide.

### 12-factor config

```python
port = int(os.environ.get("APP_PORT", "8000"))
api_key = os.environ.get("APP_API_KEY")      # secrets come from the environment
```

Config that changes between environments (dev / test / prod) lives in env
vars, not in code. Read it in one place (a `Settings` object) and pass it
around. Never commit passwords or API keys.

## Common mistakes

- `except:` or `except Exception:` around big blocks - hides real bugs.
- Inheriting from a class just to reuse one method.
- Creating collaborators inside `__init__` (`self.db = Database()`), making tests hard.
- Hard-coding secrets or URLs; committing `.env` files.
- Treating type hints as runtime validation.

## How to run

```bash
cd lessons/04_professional/07_design_best_practices
python example.py
APP_PORT=9000 python example.py          # Git Bash / macOS / Linux
$env:APP_PORT=9000; python example.py    # PowerShell
```

## Try it yourself

1. Rewrite a function that uses `if os.path.exists(path): open(path)` in EAFP style.
2. Add an `SmsNotifier` and use it with `SignupService` without changing the service.
3. Add `APP_LOG_LEVEL` to `Settings` (default `"INFO"`) and reject unknown values
   with a clear `ValueError`.
