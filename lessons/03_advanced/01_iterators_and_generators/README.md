# Lesson 3.1 — Iterators & Generators

## What you'll learn

- The difference between an **iterable** and an **iterator**
- How `yield` turns a function into a **generator**
- Using `next()`, `iter()`, and `next(it, default)`
- Delegating with `yield from`
- Writing your own iterator class with `__iter__` / `__next__`
- Generator expressions, and why they save memory (`sys.getsizeof`)
- Chaining generators into a lazy pipeline

## Explanation

### Iterables vs iterators
An **iterable** is anything you can loop over (`list`, `str`, `dict`, `range`...).
An **iterator** is the object that hands out the values, one per `next()` call,
and raises `StopIteration` when it runs out. `iter(x)` gets an iterator from an
iterable. A `for` loop does exactly this behind the scenes.

```python
it = iter([10, 20])
next(it)            # 10
next(it)            # 20
next(it, "done")    # "done" instead of StopIteration
```

### Generators and `yield`
A function with `yield` in it returns a **generator** when called; none of its
body runs yet. Each `next()` runs until the next `yield`, hands out that value,
and **pauses**, keeping its local variables. When the function ends, the
generator raises `StopIteration`.

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

list(countdown(3))   # [3, 2, 1]
```

### `yield from`
`yield from other` re-yields every item of another iterable or generator. It's
short for `for x in other: yield x`, and it's the natural way to write recursive
generators such as `flatten`.

### Custom iterator classes
Give a class `__iter__` (return the iterator) and `__next__` (return the next value
or `raise StopIteration`). If `__iter__` returns `self`, the object can only be looped over
once. If `__iter__` is itself a generator (`yield` inside it), you get a fresh
iterator every time, so the object can be looped over again and again.

### Generator expressions & memory
`(x*x for x in range(10**6))` looks like a list comprehension but with
parentheses. It makes values lazily. `sys.getsizeof` shows the list takes
megabytes while the generator object is around 200 bytes, whatever the size of the range.

### Pipelines
You can feed generators into each other (`strip → filter → upper`). Each item passes through every stage
before the next item starts, so memory use stays flat even for huge files.

## Common mistakes

- **Reusing an exhausted generator**: the second `list(gen)` is `[]`. Make a
  new generator, or use a reusable iterable class.
- **Expecting a generator function to run when called**: `countdown(3)` runs
  nothing until you iterate it.
- **Calling `len()` or indexing a generator**: they have no length and no `[i]`.
  Use `list()` first, or `itertools.islice`.
- **Forgetting the default in `next(it, default)`**: without it you'll get
  `StopIteration` at the end.
- **Using `return value` to "yield" a value**: inside a generator, `return` just ends it.

## How to run

```bash
python example.py
```

## Try it yourself

1. Write a generator `chunks(seq, n)` that yields lists of length `n`
   (the last one may be shorter): `list(chunks(range(7), 3))` → `[[0,1,2],[3,4,5],[6]]`.
2. Write a class `Cycle(items, times)` whose iterator walks over `items` `times` times.
3. Write a generator `read_numbers(lines)` that skips blank lines and comments
   (`#...`) and yields `int`s. Chain it with `sum()`.
