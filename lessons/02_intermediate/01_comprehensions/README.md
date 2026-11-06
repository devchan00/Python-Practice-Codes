# Lesson 2.1 — Comprehensions

## What you'll learn

- List comprehensions with and without a filter
- Dict and set comprehensions
- Generator expressions (lazy, memory-friendly)
- Nested comprehensions to flatten or build 2-D data
- When a plain `for` loop is the better choice

## Explanation

### List comprehensions

A list comprehension builds a new list from an iterable in one expression:

```python
squares = [x * x for x in range(10) if x % 2 == 0]   # [0, 4, 16, 36, 64]
```

Read it as "x times x, for each x in range(10), if x is even". It replaces
the empty-list + loop + `append` pattern. The trailing `if` is a **filter**
(it drops items). A ternary at the front **transforms** every item:

```python
["even" if n % 2 == 0 else "odd" for n in range(4)]
```

### Dict comprehensions

Use `{key: value for ...}`:

```python
d = {k: v for k, v in pairs}
inverted = {v: k for k, v in d.items()}
```

### Set comprehensions

Use `{expr for ...}` (no colon). Duplicates are removed automatically:

```python
{x % 3 for x in nums}    # {0, 1, 2}
```

### Generator expressions

Round brackets create a **generator**: values are produced one at a time
when asked for, so the full sequence is never held in memory.

```python
gen = (x * x for x in nums)
total = sum(x * x for x in range(1_000_000))   # no giant list built
```

A generator can be consumed only once.

### Nested comprehensions (flatten)

Multiple `for` clauses read left to right, exactly like nested loops:

```python
flat = [y for row in grid for y in row]
```

## Common mistakes

- Putting `if/else` after the `for` (`[x for x in a if x else 0]` is a syntax
  error). A filter `if` goes after `for`; a ternary goes before it.
- Writing `{}` and expecting an empty set — it is an empty dict. Use `set()`.
- Reusing a generator after it is exhausted — the second pass is empty.
- Using a comprehension only for side effects (`[print(x) for x in a]`).
- Cramming three levels of nesting into one line — use a loop when it stops
  being readable.

## How to run

```bash
python example.py
```

## Try it yourself

1. From `words = ["sky", "Ocean", "tree", "Sun"]`, build a list of only the
   words that start with a capital letter, lower-cased.
2. Build a dict mapping each number 1–10 to `"fizz"` if divisible by 3,
   otherwise to the number itself.
3. Given `matrix = [[1, 2], [3, 4], [5, 6]]`, compute the sum of all values
   using a single generator expression.
