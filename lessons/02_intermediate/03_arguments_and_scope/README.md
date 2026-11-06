# Lesson 2.3 — Arguments & scope

## What you'll learn

- Default values, `*args` and `**kwargs`
- Positional-only (`/`) and keyword-only (`*`) parameters
- Unpacking lists and dicts into a call with `*` and `**`
- The LEGB rule for name lookup
- Rebinding outer names with `global` and `nonlocal`

## Explanation

### Defaults, *args, **kwargs

```python
def f(a, b=2, *args, key=None, **kwargs): ...
```

- `a` is required; `b` falls back to `2`.
- `*args` collects extra **positional** arguments into a tuple.
- `key` comes after `*args`, so it can only be passed by keyword.
- `**kwargs` collects extra **keyword** arguments into a dict.

Default values are evaluated once, when `def` runs. Never use a mutable
default like `[]`; use `None` and create the list inside.

### Positional-only and keyword-only

```python
def g(pos_only, /, normal, *, kw_only): ...
g(1, 2, kw_only=3)
```

Parameters before `/` must be passed by position; parameters after a bare `*`
must be passed by keyword. Keyword-only makes calls readable
(`connect(timeout=5)`); positional-only lets you rename parameters freely.

### Unpacking when calling

```python
f(*[1, 2, 3], **{"key": 1})   # same as f(1, 2, 3, key=1)
first, *rest = [10, 20, 30]
merged = {**defaults, **overrides}
```

### LEGB

When Python sees a name it searches: **L**ocal (current function),
**E**nclosing (outer functions), **G**lobal (module), **B**uilt-in (`len`,
`print`, ...). The first match wins. If a function assigns to a name anywhere,
that name is local for the whole function — reading it before the assignment
raises `UnboundLocalError`.

### global and nonlocal

```python
def increment():
    global count      # module-level name
    count += 1

def make_counter():
    n = 0
    def step():
        nonlocal n    # enclosing function's name
        n += 1
        return n
    return step
```

You only need these to *rebind* a name. Mutating an object (`items.append`)
doesn't need them.

## Common mistakes

- Mutable default arguments (`def f(x, seen=[])`).
- Putting `**kwargs` before `*args` or a default before a required parameter
  (syntax errors).
- Forgetting `nonlocal` in a closure and getting `UnboundLocalError`.
- Overusing `global` — pass values in and return them out instead.
- Shadowing built-ins: `list = [1, 2]` hides the `list` type (LEGB finds yours first).

## How to run

```bash
python example.py
```

## Try it yourself

1. Write `describe(name, /, *tags, sep=", ")` that returns
   `"name: tag1, tag2"`. Check that `describe(name="x")` raises `TypeError`.
2. Write `make_accumulator()` returning a function that adds its argument to a
   running total and returns the total (use `nonlocal`).
3. Write `call_with_log(func, *args, **kwargs)` that prints the arguments, then
   calls `func(*args, **kwargs)` and returns its result.
