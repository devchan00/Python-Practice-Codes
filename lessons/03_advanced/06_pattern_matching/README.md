# Lesson 3.6 — Pattern Matching (`match` / `case`)

## What you'll learn

- Literal patterns and the wildcard `_`
- OR patterns with `|`
- Sequence patterns: `[x, y]`, `[first, *rest]`
- Mapping patterns: `{"type": "click", "pos": (x, y)}`, `**rest`
- Class patterns: `Point(x=0, y=0)`, `Point(0, y)`, `str(k)`
- Guards: `case int(x) if x < 0`
- Capturing with `as`
- The "bare names capture" gotcha

## Explanation

`match` checks a value against each `case` from top to bottom and runs the
**first** one that matches. A pattern can test the *shape* of the data and bind variables in the
same step.

### Literals, OR, wildcard
```python
match code:
    case 200: ...
    case 401 | 403: ...      # either
    case _: ...              # anything (the default)
```

### Sequences
```python
match words:
    case ["go", direction]:  # exactly two items
    case ["drop", *items]:   # one or more; the rest go into a list
    case [first, *_, last]:  # at least two
```
Sequence patterns match lists and tuples but **not strings**.

### Mappings
`{"type": "click", "pos": (x, y)}` matches any dict that has those keys. **Extra keys
are ignored.** Use `**rest` to collect the remaining keys.

### Classes
`Point(x=0, y=0)` checks `isinstance(v, Point)` and then compares the attributes. Positional
patterns like `Point(0, y)` rely on `__match_args__`, which dataclasses generate
automatically. `str(k)` / `int()` check the type (and capture the value).

### Guards
`case pattern if condition:` matches only when the pattern fits **and** the condition
is true. Otherwise matching moves on to the next case.

### `as`
`case ("+" | "-") as op:` binds the whole matched value, which is useful with OR patterns
and nested sub-patterns.

### Gotcha: bare names capture
`case RED:` doesn't compare against a variable named `RED`. It **captures** the
value into `RED`, so it matches everything. Use dotted names (`Color.RED`, an `Enum`)
or literals for constants.

## Common mistakes

- Writing `case RED:` with a bare constant name. This captures instead of comparing.
- Expecting `case [x]:` to match a one-character string.
- Forgetting that mapping patterns ignore extra keys, so a broad pattern placed early "steals"
  matches meant for later cases.
- Putting `case _:` (or another catch-all) before the specific cases. Python reports a
  `SyntaxError` for unreachable patterns.
- Using `match` when one `if`/`elif` or a dict lookup would be clearer.

## How to run

```bash
python example.py
```

## Try it yourself

1. Write a calculator that matches `["add", a, b]`, `["neg", a]` and `["sum", *nums]`.
2. Write a JSON-like event router that handles `{"type": "login", "user": str(name)}`
   and rejects everything else with an error message.
3. Write a `Shape` hierarchy (`Rect`, `Circle`) and compute `area(shape)` with class patterns.
