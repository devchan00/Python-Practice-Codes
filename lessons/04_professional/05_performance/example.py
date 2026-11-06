"""Lesson 4.5 - Performance: measure first, then optimise.

The golden rule is *profile before optimising*: guesses about where time goes
are usually wrong. This lesson profiles a function with ``cProfile`` +
``pstats``, micro-benchmarks with ``timeit`` and ``time.perf_counter``,
measures memory with ``tracemalloc``, and then shows the classic wins: set/dict
lookup instead of list scans, ``''.join`` instead of ``+=``, generators for
streaming, and ``functools.cache`` for memoising pure functions. For live
processes use ``py-spy``; for heavy numeric loops reach for NumPy, polars or
Cython (see README).
"""

import cProfile
import functools
import io
import pstats
import sys
import time
import timeit
import tracemalloc


# --- 1. cProfile: find the hot spots ---
def slow_square_sum(n: int) -> int:
    return sum(slow_square(i) for i in range(n))


def slow_square(x: int) -> int:
    return x * x


def report() -> int:
    total = 0
    for _ in range(5):
        total += slow_square_sum(20_000)
    return total


def demo_cprofile() -> None:
    print("\n--- 1. cProfile ---")
    profiler = cProfile.Profile()
    profiler.enable()
    report()
    profiler.disable()

    buf = io.StringIO()
    stats = pstats.Stats(profiler, stream=buf).strip_dirs().sort_stats("cumulative")
    stats.print_stats(5)  # top 5 rows by cumulative time
    for line in buf.getvalue().splitlines():
        if line.strip():
            print(" ", line[:100])
    # -> ncalls for slow_square = 100000: the many tiny calls ARE the cost.
    # Command-line equivalent:  python -m cProfile -s cumtime app.py


# --- 2. timeit and perf_counter ---
def demo_timing() -> None:
    print("\n--- 2. timeit / perf_counter ---")
    # timeit runs a snippet many times and turns off GC: good for micro-benchmarks.
    t = timeit.timeit("sorted(data)", setup="data = list(range(1000))[::-1]", number=2000)
    print(f"sorted() of 1000 items: {t / 2000 * 1e6:.1f} us per call")

    # perf_counter: a high-resolution monotonic clock for timing a block.
    start = time.perf_counter()
    sum(range(1_000_000))
    print(f"sum(range(1e6)) took {(time.perf_counter() - start) * 1000:.1f} ms")
    # Don't use time.time() for timing: it can jump (NTP, DST changes).


# --- 3. tracemalloc: where does memory go? ---
def demo_tracemalloc() -> None:
    print("\n--- 3. tracemalloc ---")
    tracemalloc.start()
    big_list = [str(i) * 10 for i in range(100_000)]
    current, peak = tracemalloc.get_traced_memory()
    snapshot = tracemalloc.take_snapshot()
    tracemalloc.stop()
    print(f"current={current / 1e6:.1f} MB peak={peak / 1e6:.1f} MB")  # -> ~ 8-10 MB
    top = snapshot.statistics("lineno")[0]
    print("biggest allocation line:", top.traceback.format()[-1].strip())
    # -> big_list = [str(i) * 10 for i in range(100_000)]
    del big_list


# --- 4. set / dict lookup is O(1), list lookup is O(n) ---
def demo_lookup() -> None:
    print("\n--- 4. set vs list lookup ---")
    items = list(range(100_000))
    as_set = set(items)
    target = 99_999  # worst case for the list: it's at the end
    t_list = timeit.timeit(lambda: target in items, number=200)
    t_set = timeit.timeit(lambda: target in as_set, number=200)
    print(f"list: {t_list * 1000:.2f} ms   set: {t_set * 1000:.3f} ms   "
          f"-> set is ~{t_list / t_set:.0f}x faster")
    # A set hashes the value and jumps straight to it; a list checks one by one.


# --- 5. ''.join(parts) vs += in a loop ---
def concat_plus(n: int) -> str:
    s = ""
    for i in range(n):
        s += str(i)  # may copy the whole string each time -> O(n^2) worst case
    return s


def concat_join(n: int) -> str:
    return "".join(str(i) for i in range(n))  # one final allocation -> O(n)


def demo_join() -> None:
    print("\n--- 5. ''.join vs += ---")
    n = 100_000
    t_plus = timeit.timeit(lambda: concat_plus(n), number=5)
    t_join = timeit.timeit(lambda: concat_join(n), number=5)
    print(f"+= : {t_plus * 200:.1f} ms   join: {t_join * 200:.1f} ms")
    # CPython has a special trick that sometimes makes += fast, but it is not
    # guaranteed (other implementations, or when another reference exists).
    print("same result:", concat_plus(50) == concat_join(50))  # -> True


# --- 6. Generators stream data instead of building lists ---
def demo_generators() -> None:
    print("\n--- 6. Generators ---")
    as_list = [i * i for i in range(1_000_000)]
    as_gen = (i * i for i in range(1_000_000))
    print(f"list: {sys.getsizeof(as_list):,} bytes   generator: {sys.getsizeof(as_gen)} bytes")
    # -> list: ~8,000,000 bytes   generator: ~200 bytes (it computes lazily)
    print("sum via generator:", sum(as_gen))  # -> 333332833333500000
    del as_list


# --- 7. functools.cache: memoise pure functions ---
def fib_slow(n: int) -> int:
    return n if n < 2 else fib_slow(n - 1) + fib_slow(n - 2)


@functools.cache  # remembers results by argument; = lru_cache(maxsize=None)
def fib_fast(n: int) -> int:
    return n if n < 2 else fib_fast(n - 1) + fib_fast(n - 2)


def demo_cache() -> None:
    print("\n--- 7. functools.cache ---")
    start = time.perf_counter()
    fib_slow(25)
    slow = time.perf_counter() - start
    start = time.perf_counter()
    fib_fast(25)
    fast = time.perf_counter() - start
    print(f"fib(25) uncached {slow * 1000:.1f} ms, cached {fast * 1000:.3f} ms")
    print(fib_fast.cache_info())  # -> CacheInfo(hits=23, misses=26, maxsize=None, currsize=26)
    print("fib(200) =", fib_fast(200))  # impossible without the cache
    # Only cache PURE functions (same input -> same output, no side effects),
    # and remember the cache keeps every result in memory.


def main() -> None:
    demo_cprofile()
    demo_timing()
    demo_tracemalloc()
    demo_lookup()
    demo_join()
    demo_generators()
    demo_cache()
    # --- 8. Beyond pure Python (not run here) ---
    # py-spy top --pid N        sample a live process without restarting it
    # NumPy / polars            vectorise: one C loop instead of a Python loop
    # Cython / mypyc / numba    compile hot loops to machine code


if __name__ == "__main__":
    main()
