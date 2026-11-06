# Soft Keywords: `match` / `case`, `type`, `_`

Soft keywords are special **only in a certain position**. Outside that context
they are ordinary names, so old code that used `match = ...` or `type(x)` keeps
working. See the current list with `import keyword; keyword.softkwlist`.

## What you'll learn

- Structural pattern matching with `match` / `case` (Python 3.10+)
- Literal, OR (`|`), sequence, dict, class, guard (`if`) and capture (`as`) patterns
- The `type` alias statement (Python 3.12+), including generic aliases
- The three jobs of `_`: throwaway variable, wildcard pattern, last REPL result
- Why soft keywords can still be used as normal names

## Explanation

### `match` / `case`
`match` looks at a value and runs the first `case` whose **pattern** fits:

```python
match cmd:
    case "go":
        ...
    case "stop" | "halt":      # either string
        ...
    case [first, *rest]:       # any sequence with at least one item
        ...
    case {"action": "move", "to": dest}:   # dict with these keys
        ...
    case Point(x, y) if x == y:            # class pattern + guard
        ...
    case _:                    # anything else
        ...
```
Names in a pattern (`first`, `dest`, `x`) are **captured** - they get assigned
the matching part. Only `match` at the start of a statement and `case` inside it
are special; `match = re.match(...)` elsewhere is fine.

### `type`
```python
type Vec = list[float]
type Pair[T] = tuple[T, T]
def norm(v: Vec) -> float: ...
```
This creates a named type alias for type hints. The value is evaluated lazily
(`Vec.__value__`). `type(42)` still works as the built-in function.

### `_`
- Throwaway: `for _ in range(3): ...` or `name, _, age = row`.
- Wildcard: `case _:` matches anything and binds nothing.
- REPL only: after `>>> 2 + 3`, `_` holds `5`.

Note: Python 3.15 adds another soft keyword, `lazy` (for `lazy import ...`);
it shows up in `keyword.softkwlist`.

## Common mistakes

- Writing `case x:` expecting to compare with an existing variable `x` - a bare name **captures** (always matches!). Compare to constants with dotted names (`case Color.RED:`) or a guard (`case v if v == x:`).
- Putting `case _:` first - every case after it is unreachable (Python raises a `SyntaxError`).
- Forgetting `__match_args__` on your class and then using positional class patterns like `Point(x, y)`.
- Using `type X = ...` on Python older than 3.12 - it is a `SyntaxError` there.
- Using `_` as a real variable and then wondering why its value is "lost" - readers (and tools) treat it as garbage.

## How to run

```
python example.py
```

## Try it yourself

1. Write `http_status(code)` with `match` that returns "OK" for 200, "Not Found" for 404, "Server error" for 500/502/503 (use `|`), and "Unknown" otherwise.
2. Match on tuples: `(0, 0)` -> "origin", `(x, 0)` -> "on x-axis", `(0, y)` -> "on y-axis", `(x, y)` -> "elsewhere".
3. Create `type Matrix = list[list[float]]` and write a function annotated with it that returns the number of rows.
