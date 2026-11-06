"""Lesson 3.1 - Iterators & generators.

An *iterable* is anything you can loop over; an *iterator* is the object that
actually hands out values one at a time via ``next()``. Generators are the
easiest way to build iterators: any function containing ``yield`` pauses at
each ``yield`` and resumes where it left off on the next ``next()`` call. Because
they produce values lazily (on demand) they use almost no memory, even for
huge or infinite sequences.
"""

import sys


# --- 1. A simple generator -------------------------------------------------
def countdown(n):
    """Yield n, n-1, ..., 1. Nothing runs until someone asks for a value."""
    while n > 0:
        yield n          # pause here, hand n to the caller
        n -= 1           # resume here on the next next()


def demo_simple_generator():
    print("--- 1. A simple generator ---")
    gen = countdown(3)
    print(type(gen).__name__)      # -> generator   (calling it ran no code yet)
    print(next(gen))               # -> 3
    print(next(gen))               # -> 2
    print(list(gen))               # -> [1]  (list() drains whatever is left)
    # A generator is single-use: once exhausted it stays exhausted.
    print(list(gen))               # -> []


# --- 2. next() and StopIteration, iter()/next() with a default -------------
def demo_iter_next():
    print("\n--- 2. iter() / next() and defaults ---")
    it = iter([10, 20])            # iter() turns an iterable into an iterator
    print(next(it), next(it))      # -> 10 20
    # A third next() would raise StopIteration. Passing a default avoids that:
    print(next(it, "done"))        # -> done
    try:
        next(it)
    except StopIteration:
        print("StopIteration raised")  # -> StopIteration raised
    # for-loops call iter() and next() for you and catch StopIteration silently.

    # Handy idiom: first item matching a condition, or a fallback.
    nums = [3, 7, 12, 18]
    first_even = next((n for n in nums if n % 2 == 0), None)
    print(first_even)              # -> 12


# --- 3. yield from: delegate to another iterable ---------------------------
def flatten(nested):
    """Recursively flatten nested lists. `yield from` re-yields every item."""
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)   # same as: for x in flatten(item): yield x
        else:
            yield item


def demo_yield_from():
    print("\n--- 3. yield from ---")
    print(list(flatten([1, [2, [3, 4]], 5])))   # -> [1, 2, 3, 4, 5]

    def chain_two(a, b):
        yield from a
        yield from b
    print(list(chain_two("ab", range(2))))      # -> ['a', 'b', 0, 1]


# --- 4. A custom iterator class (__iter__ / __next__) ----------------------
class Countdown:
    """The class version of countdown(): more code, but you can add methods
    and state. __iter__ returns the iterator; __next__ returns the next value
    or raises StopIteration to signal the end."""

    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self              # this object is its own iterator

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


class Squares:
    """An *iterable* (not an iterator): each iter() call gives a fresh
    generator, so you can loop over it many times."""

    def __init__(self, n):
        self.n = n

    def __iter__(self):
        for i in range(self.n):
            yield i * i


def demo_custom_iterator():
    print("\n--- 4. Custom iterator class ---")
    print(list(Countdown(3)))      # -> [3, 2, 1]
    for x in Countdown(2):
        print("tick", x)           # -> tick 2 / tick 1
    sq = Squares(4)
    print(list(sq), list(sq))      # -> [0, 1, 4, 9] [0, 1, 4, 9] (reusable)


# --- 5. Infinite generators -------------------------------------------------
def fibonacci():
    a, b = 0, 1
    while True:                    # infinite is fine: values come one at a time
        yield a
        a, b = b, a + b


def demo_infinite():
    print("\n--- 5. Infinite generator ---")
    fib = fibonacci()
    print([next(fib) for _ in range(10)])   # -> [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


# --- 6. Generator expressions & memory -------------------------------------
def demo_genexpr_memory():
    print("\n--- 6. Generator expressions vs lists ---")
    squares_list = [x * x for x in range(1_000_000)]   # builds all 1M now
    squares_gen = (x * x for x in range(1_000_000))    # builds nothing yet
    print(f"list: {sys.getsizeof(squares_list):,} bytes")  # -> list: ~8,000,000+ bytes
    print(f"gen : {sys.getsizeof(squares_gen):,} bytes")   # -> gen : ~200 bytes
    # Same answer, tiny memory: sum() pulls values one at a time.
    print(sum(squares_gen) == sum(squares_list))           # -> True
    # When passing a genexp as the only argument, the extra () can be dropped:
    print(sum(x for x in range(5)))                        # -> 10


# --- 7. Pipelines of generators --------------------------------------------
def demo_pipeline():
    print("\n--- 7. Generator pipeline ---")
    lines = ["  apple ", "", "Banana", "  ", "cherry"]
    stripped = (s.strip() for s in lines)          # stage 1
    non_empty = (s for s in stripped if s)         # stage 2
    upper = (s.upper() for s in non_empty)         # stage 3
    # Nothing has run yet; list() pulls each item through all stages in turn.
    print(list(upper))     # -> ['APPLE', 'BANANA', 'CHERRY']


if __name__ == "__main__":
    demo_simple_generator()
    demo_iter_next()
    demo_yield_from()
    demo_custom_iterator()
    demo_infinite()
    demo_genexpr_memory()
    demo_pipeline()
