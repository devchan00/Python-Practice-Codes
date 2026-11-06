# Bonus 1: Common gotchas

Mistakes everyone makes once. Each one is shown in `example.py` as **bug**
then **fix**.

## What you'll learn

| # | Gotcha | Fix |
|---|---|---|
| 1 | `def f(x=[])` - the default is shared between calls | Default to `None`, create the list inside |
| 2 | `[lambda: i for i in r]` - all see the last `i` | `lambda i=i: i` |
| 3 | `a == b` vs `a is b` | `==` for values, `is` only for `None`/`True`/`False` |
| 4 | `for x in lst: lst.remove(x)` skips items | Iterate a copy, or build a new list |
| 5 | `b = a` is an alias, not a copy | `a.copy()` (shallow) / `copy.deepcopy(a)` |
| 6 | `0.1 + 0.2 != 0.3` | `math.isclose`, or `Decimal("0.1")` |
| 7 | `except:` hides bugs | Catch specific errors |
| 8 | `from x import *` pollutes the namespace | Import names explicitly |
| 9 | `10 / 2` gives `5.0` | `//` for integer division |
| 10 | `'a' + 1` raises `TypeError` | Convert explicitly: `str(1)`, `int("1")`, f-strings |

## Explanation

### 1. Mutable default arguments

```python
def f(x=[]):            # [] is evaluated ONCE, when `def` runs
    x.append(1); return x
f(); f()                # [1, 1]  - same list every time

def f(x=None):
    if x is None:
        x = []
```

### 2. Late binding

A closure remembers the *variable*, not its value at creation time. By the
time you call the lambdas, the loop is over and `i` is 2. A default argument
(`lambda i=i: i`) is evaluated immediately, freezing the current value.

### 3. `==` vs `is`

`==` compares values; `is` checks whether two names refer to the *same
object*. CPython caches small ints and some strings, so `is` sometimes appears
to work for them - then fails in production. Use `is` only for singletons:
`if x is None:`.

### 4. Mutating while iterating

Removing an item shifts the rest left; the loop's internal index moves on and
skips the next element. Use `for x in lst[:]` or, better,
`lst = [x for x in lst if keep(x)]`.

### 5. Aliasing

Assignment never copies. `b = a` gives the same list two names.
`a.copy()` / `list(a)` / `a[:]` copy the outer list only; nested lists are
still shared. `copy.deepcopy(a)` copies everything.

### 6. Floating point

Floats are binary fractions, so `0.1` is really `0.1000000000000000055...`.
Compare with `math.isclose(a, b)`. For money use `Decimal("0.10")` - built from
a **string**.

### 7. Bare `except:`

It catches everything, including typos (`NameError`), `KeyboardInterrupt` and
`SystemExit`. Catch what you expect: `except ValueError:`.

### 8. `from x import *`

You can't tell where names came from, and later imports silently overwrite
earlier ones (`cmath.sqrt` replacing `math.sqrt`). Write
`from math import sqrt` or `import math`.

### 9. `/` vs `//`

`/` is true division and always returns a float, even `10 / 2 == 5.0`. Use
`//` for floor division (`-7 // 2 == -4`, rounds down) - e.g. list indices.

### 10. `str + int`

Python is strongly typed: it never guesses whether `"1" + 1` means `"11"` or
`2`. Convert explicitly, or use f-strings: `f"Age: {age}"`.

## Common mistakes

The whole lesson is common mistakes! Two more meta-mistakes:

- "Fixing" a gotcha by memorising the symptom instead of the reason. Each fix
  above follows from one rule (defaults evaluated once, names are references...).
- Not using a linter: `ruff` flags #1 (B006), #7 (E722), #8 (F403) automatically.

## How to run

```bash
cd lessons/05_bonus/01_common_gotchas
python example.py
```

## Try it yourself

1. A class attribute `items = []` shared by all instances is gotcha #1 in
   disguise. Write a class that shows the bug, then fix it in `__init__`.
2. Predict, then check: `grid = [[0] * 3] * 3; grid[0][0] = 1; print(grid)`.
   Fix it with a comprehension.
3. Compute `sum([0.1] * 10)`. Is it `1.0`? Try `math.fsum` and `Decimal`.
