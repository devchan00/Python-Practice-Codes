# Lesson 2.2 — Functional helpers

## What you'll learn

- Writing small anonymous functions with `lambda`
- Sorting by any rule with `sorted(..., key=...)`
- Lazy transforms with `map` and `filter`
- Pairing and transposing with `zip` (and `strict=True`)
- Truth tests with `any` / `all`
- Aggregating with `sum`, `min`, `max` (and their `key=` / `default=`)

## Explanation

### lambda

`lambda x: x * 2` is a function with no name and a single expression as its
body. It is meant to be passed straight into another function. If you would
assign it to a name, write a `def` instead.

### sorted with key

`sorted(items, key=f)` calls `f` on each item and orders items by the result.
Python's sort is **stable**: items with equal keys keep their original order.
Return a tuple to sort by several fields:

```python
sorted(people, key=lambda t: (-t[1], t[0]))   # age desc, then name
```

`sorted()` returns a new list; `list.sort()` sorts in place and returns `None`.

### map and filter

`map(f, it)` applies `f` to every item; `filter(f, it)` keeps items where
`f(item)` is truthy. Both are **lazy** — they return iterators that compute
values only when you loop over them (or wrap them in `list()`).
`filter(None, it)` keeps only truthy items.

### zip

`zip(a, b)` pairs items position by position and stops at the shortest input.
Use `strict=True` to get a `ValueError` when lengths differ. `zip(*rows)`
transposes rows into columns.

### any / all

`any(it)` is True if at least one item is truthy; `all(it)` if every item is.
Both stop early. Note `all([])` is `True` and `any([])` is `False`.

### sum / min / max

`sum(it, start=0)`, `min(it)`, `max(it)`. `min`/`max` accept `key=` (compare by
`key(item)` but return the item) and `default=` for empty inputs.

## Common mistakes

- Printing a `map`/`filter` object and expecting a list — wrap it in `list()`.
- Iterating a `map`/`filter`/`zip` twice — they are exhausted after one pass.
- `x = x.sort()` — sets `x` to `None`.
- Forgetting `zip` silently truncates; use `strict=True` when lengths matter.
- Calling `max([])` without `default=` — raises `ValueError`.

## How to run

```bash
python example.py
```

## Try it yourself

1. Sort `["kiwi", "Fig", "apple", "date"]` by length, then alphabetically
   (case-insensitive) for ties.
2. Given `names` and `ages` lists, use `zip` + `max(key=...)` to find the
   oldest person's name.
3. Use `map` and `filter` to turn `["3", "x", "10", ""]` into `[3, 10]`
   (hint: `str.isdigit`).
