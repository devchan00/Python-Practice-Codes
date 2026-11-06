# Python Lessons — from the Python Cheatsheet

Runnable sample code and explanations for every section of `python_cheatsheet.pdf`,
organised Beginner → Professional.

Each lesson folder contains:

- `example.py` — runnable sample code, with comments showing the expected output
  (longer lessons split this into `example_1_...py`, `example_2_...py`; run each one)
- `README.md` — a plain-language explanation, common mistakes, and exercises

Run any lesson with:

```bash
cd lessons/01_beginner/03_strings
python example.py
```

All examples need Python 3.12+ (written and tested on 3.15). They need no extra
packages, except the optional `test_calc.py` in the pytest lesson.

## Suggested order

| Folder | Cheatsheet section |
|---|---|
| `00_reference/` | A. Reserved keywords · B. Soft keywords · C. Built-in functions · D. Syntax at a glance |
| `01_beginner/` | Variables & types · Operators · Strings · Control flow · Collections · Functions · I/O, loops & errors · mini-project |
| `02_intermediate/` | Comprehensions · Functional helpers · Arguments & scope · Modules · Files & JSON · Classes · Exceptions · Regex & dates · mini-project |
| `03_advanced/` | Iterators & generators · Decorators & closures · Context managers · Dunder methods · Dataclasses & type hints · Pattern matching · Stdlib power tools · mini-project |
| `04_professional/` | Concurrency · Testing · Tooling · Logging · Performance · Internals · Best practices · Security · Ecosystem · mini-project |
| `05_bonus/` | Common gotchas · Big-O complexity · Practice projects |

Tip: start with `01_beginner/` and treat `00_reference/` as a lookup table you
come back to.
