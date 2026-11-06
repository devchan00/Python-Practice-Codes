# Lesson 2.4 — Modules, packages & the standard library

## What you'll learn

- The forms of `import`: `import m`, `import m as y`, `from m import x as y`
- What makes a folder a package (`__init__.py`) and how to re-export names
- Why every script ends with `if __name__ == "__main__":`
- A quick tour of `os`, `sys`, `pathlib`, `json`, `csv`, `re`, `datetime`,
  `time`, `random`, `math`, `argparse`, `logging`, `subprocess`

## Files

| File | Purpose |
|---|---|
| `example.py` | Import forms, using `mypkg`, the `__name__` guard; then runs the tour |
| `stdlib_tour.py` | One small demo per standard-library module (also runnable alone) |
| `mypkg/__init__.py` | Marks `mypkg` as a package and re-exports `greet`, `shout` |
| `mypkg/greetings.py` | A module inside the package |

## Explanation

### Modules and imports

Any `.py` file is a module. Importing it runs it once and caches it in
`sys.modules`; later imports reuse the cached module.

```python
import math                    # math.sqrt(2)
import json as js              # alias
from math import pi, sqrt      # bring names in directly
from collections import Counter as C
```

Prefer `import module` or explicit `from module import name`. Avoid
`from module import *`: it hides where names come from and can overwrite yours.

Python finds modules by searching `sys.path`. Its first entry is the folder of
the script being run, which is why `example.py` can import `mypkg` and
`stdlib_tour` from any working directory.

### Packages

A folder containing `__init__.py` is a package. Its `__init__.py` runs on first
import and can re-export names for a nicer API:

```python
# mypkg/__init__.py
from .greetings import greet, shout    # "." = this package
```

```python
import mypkg
from mypkg import greet
from mypkg.greetings import DEFAULT_GREETING
```

### `if __name__ == "__main__":`

When a file is run directly, its `__name__` is `"__main__"`. When it is
imported, `__name__` is the module name (`"mypkg.greetings"`). Code under the
guard therefore runs only for `python file.py`, so the file can also be
imported safely without its demo running.

### Standard library tour

| Module | Used for |
|---|---|
| `os` | Environment variables, working directory, OS details |
| `sys` | Interpreter info, `sys.argv`, `sys.path`, `sys.executable` |
| `pathlib` | Paths as objects: `Path(__file__).parent / "data.json"` |
| `json` / `csv` | Read and write JSON and CSV |
| `re` | Regular expressions |
| `datetime` / `time` | Dates and durations / clocks and timers (`perf_counter`) |
| `random` | Pseudo-random numbers (seed with `random.Random(42)` for repeatability) |
| `math` | `sqrt`, `gcd`, `isclose`, `pi`, ... |
| `argparse` | Parse command-line options |
| `logging` | Levelled log messages instead of `print` |
| `subprocess` | Run other programs: `subprocess.run([sys.executable, "-c", "print('hi')"])` |

Always pass `subprocess.run` a **list** of arguments rather than one string
with `shell=True` — that avoids shell-injection bugs.

## Common mistakes

- Naming your own file after a standard module (`random.py`, `json.py`) — it
  shadows the real module and imports break mysteriously.
- Forgetting `__init__.py` or using a relative import (`from .x import y`) in a
  file you run as a script.
- Putting demo/test code at module level without the `__main__` guard, so it
  runs on every import.
- Circular imports (a imports b, b imports a) — move shared code to a third module.
- Using `subprocess` with `shell=True` and user input.

## How to run

```bash
python example.py          # imports + package + full stdlib tour
python stdlib_tour.py      # only the tour
python mypkg/greetings.py  # shows the module's own __main__ block
```

`example.py` sets `sys.dont_write_bytecode = True` so no `__pycache__` folders
are left behind; normal projects don't need to do this.

## Try it yourself

1. Add `mypkg/farewells.py` with a `bye(name)` function, re-export it from
   `mypkg/__init__.py`, and call it from `example.py`.
2. Extend `tour_argparse` with a `--lang` option restricted to
   `choices=["en", "fr"]`, and see what error you get for `--lang de`.
3. Use `pathlib` to list every `.py` file in this lesson folder
   (hint: `Path(__file__).parent.rglob("*.py")`).
