# 4.5 Performance

## What you'll learn

- **Profile before optimising**: `cProfile` and `pstats`
- Timing with `timeit` and `time.perf_counter()`
- Measuring memory with `tracemalloc`
- Quick wins: set/dict lookups, `''.join`, generators, `functools.cache`
- Where to go next: `py-spy`, NumPy, polars, Cython

## Explanation

### Profile first

```bash
python -m cProfile -s cumtime app.py     # whole program, sorted by cumulative time
```

```python
import cProfile, pstats
with cProfile.Profile() as prof:         # or prof.enable() / prof.disable()
    report()
pstats.Stats(prof).strip_dirs().sort_stats("cumulative").print_stats(5)
```

- `ncalls` - how many times it ran
- `tottime` - time inside the function itself
- `cumtime` - time including everything it called

Look for big `cumtime` or huge `ncalls`. Fix the top item, then measure again.

### Timing

```python
import timeit, time
timeit.timeit("sorted(data)", setup="data = list(range(1000))", number=2000)

start = time.perf_counter()
work()
elapsed = time.perf_counter() - start
```

`timeit` repeats a snippet many times (smoothing out noise); `perf_counter` is
a high-resolution clock for timing a block. Avoid `time.time()` for timing.

### Memory

```python
import tracemalloc
tracemalloc.start()
...
current, peak = tracemalloc.get_traced_memory()
top = tracemalloc.take_snapshot().statistics("lineno")[:5]   # biggest lines
```

### Quick wins

| Slow | Fast | Why |
|---|---|---|
| `x in big_list` | `x in big_set` | Hash lookup O(1) vs scan O(n) |
| `s += part` in a loop | `"".join(parts)` | One allocation instead of many copies |
| `[f(x) for x in huge]` | `(f(x) for x in huge)` | Generators stream; constant memory |
| recomputing a pure function | `@functools.cache` | Memoise: compute each input once |

`itertools` (`islice`, `chain`, `groupby`...) lets you stream large data
without building lists.

### Beyond pure Python

- **py-spy** - `py-spy top --pid N` samples a running process (no code changes).
- **NumPy / polars** - vectorise: `arr * 2` runs one loop in C instead of a
  Python loop over a million objects.
- **Cython / mypyc / numba** - compile hot loops to native code.
- Concurrency (lesson 4.1) for waiting or multi-core work.

## Common mistakes

- Optimising without profiling ("I'm sure it's the regex").
- Micro-optimising code that runs once, while a loop elsewhere runs a million times.
- Benchmarking only once, or with `time.time()`.
- Caching impure functions (results depending on time, files, randomness).
- Unbounded caches in long-running servers - use `lru_cache(maxsize=...)`.

## How to run

```bash
cd lessons/04_professional/05_performance
python example.py
```

Timings depend on your machine; the *ratios* are what matter.

## Try it yourself

1. Profile `fib_slow(25)` with cProfile. How many calls does it make?
2. Time `x in d` for a dict and `x in d.values()`. Explain the difference.
3. Use `tracemalloc` to compare the peak memory of `sum([i for i in range(10**6)])`
   and `sum(i for i in range(10**6))`.
