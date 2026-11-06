# Lesson 3.7 — Standard-Library Power Tools

## What you'll learn

| File | Tools |
|---|---|
| `example.py` | `Counter`, `defaultdict`, `deque`, `namedtuple`, `ChainMap`, `heapq`, `bisect`, `copy` / `deepcopy` |
| `example_functional.py` | `chain`, `product`, `combinations`, `groupby`, `islice`, `accumulate`, `partial`, `reduce`, `lru_cache`, `cached_property`, `singledispatch` |
| `example_types.py` | `pathlib.Path`, `Enum`, `auto`, `StrEnum`, `IntEnum`, `ABC`, `abstractmethod` |

## Explanation

### collections
- **`Counter(iterable)`** tallies items. `.most_common(n)` gives the top n, missing keys count as `0`, and
  you can add and subtract counters.
- **`defaultdict(list)`**: when you access a missing key, it creates the value by calling the factory first.
  It's perfect for grouping (`d[key].append(x)`) and counting (`defaultdict(int)`).
- **`deque`** has O(1) `append`/`appendleft`/`pop`/`popleft`. Use it for queues instead of
  `list.pop(0)`. `deque(maxlen=n)` keeps only the last n items.
- **`namedtuple("Point", "x y")`** is an immutable tuple with named fields, `_replace` and `_asdict`.
- **`ChainMap(a, b, c)`** looks keys up in `a`, then `b`, then `c`. It's handy for CLI > user > default
  settings. Writes go to the first mapping.

### heapq & bisect
- **`heapq`** turns a plain list into a min-heap. `heappush`/`heappop` are O(log n), `heap[0]` is
  the smallest item, and `nsmallest`/`nlargest` give the top n. Push `(priority, item)` tuples to build a
  priority queue.
- **`bisect`** does binary search on a *sorted* list. `bisect_left` finds the insertion index,
  and `insort` inserts while keeping the list sorted. It's also a neat way to map scores to grades.

### copy
`copy.copy(x)` is **shallow**: you get a new outer object, but the inner objects are shared.
`copy.deepcopy(x)` recursively copies everything.

### itertools (all lazy)
```python
chain([1, 2], "ab")              # 1 2 'a' 'b'
product("ab", [1, 2])            # nested loops: a1 a2 b1 b2
combinations("ABC", 2)           # AB AC BC
groupby(sorted(xs, key=f), f)    # groups of ADJACENT equal keys
islice(gen, 5)                   # gen[:5] for any iterator
accumulate([1, 2, 3])            # 1 3 6 (running total)
```

### functools
- **`partial(f, exp=2)`** makes a new function with some arguments already filled in.
- **`reduce(op, seq)`** folds a sequence into one value: `reduce(mul, [1, 2, 3, 4]) == 24`.
- **`@lru_cache`** memoises results by their arguments, which turns exponential recursion like `fib`
  into linear. The arguments must be hashable.
- **`@cached_property`** computes the value once per instance and then stores it. Use `del obj.attr` to reset it.
- **`@singledispatch`** picks an implementation based on the type of the first argument
  (`@describe.register` on a function with a type annotation).

### pathlib
```python
p = Path(tmp) / "docs" / "notes.txt"
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text("hi", encoding="utf-8")
p.name, p.stem, p.suffix, p.read_text(), list(root.rglob("*.py"))
```

### enum
`Enum` members are named constants (`Color.RED`). `auto()` assigns their values for you. `StrEnum` members
*are* strings, which is handy for JSON and APIs; `IntEnum` members are ints. A plain `Enum` member is
never equal to its raw value, and that prevents accidental mix-ups.

### abc
Inherit from `ABC` and mark methods with `@abstractmethod`. Trying to instantiate a class that
hasn't implemented them all raises `TypeError` immediately, not later when the method is called.

## Common mistakes

- Using `groupby` without sorting by the same key first, which splits groups.
- Reading a missing key from a `defaultdict`. This **inserts** it.
- Using `copy.copy` on nested data and then being surprised that the inner changes are shared.
- Passing lists to an `@lru_cache` function, which raises `TypeError: unhashable type`.
- Calling `bisect` on an unsorted list. You get wrong answers and no error.
- Using `heapq` and expecting the list to be fully sorted. Only `heap[0]` is guaranteed to be the minimum.
- Using `str` paths with `+` instead of `Path` with `/`.

## How to run

```bash
python example.py
python example_functional.py
python example_types.py
```

## Try it yourself

1. Use `Counter` and `pathlib` to find the five most common words across all `.txt`
   files in a temporary folder you create.
2. Build a `TaskQueue` class on top of `heapq` with `add(task, priority)` and `next()`.
3. Use `@singledispatch` to write `to_json_like(obj)` that handles `dict`, `list`, `str`,
   `int` and a dataclass.
