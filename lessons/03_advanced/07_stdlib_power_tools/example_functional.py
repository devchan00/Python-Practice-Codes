"""Lesson 3.7 - Standard-library power tools, part 2: itertools & functools.

``itertools`` provides fast, lazy building blocks for iteration: chaining,
cartesian products, combinations, grouping, slicing and running totals.
``functools`` provides tools that act on functions: freezing arguments
(``partial``), folding (``reduce``), memoising (``lru_cache``,
``cached_property``) and type-based dispatch (``singledispatch``).
"""

import functools
import operator
from functools import cached_property, lru_cache, partial, reduce, singledispatch
from itertools import accumulate, chain, combinations, count, groupby, islice, product


# --- 1. chain: glue iterables together -------------------------------------
def demo_chain():
    print("--- 1. chain ---")
    print(list(chain([1, 2], (3,), "ab")))          # -> [1, 2, 3, 'a', 'b']
    nested = [[1, 2], [3], [4, 5]]
    print(list(chain.from_iterable(nested)))        # -> [1, 2, 3, 4, 5] (flatten 1 level)


# --- 2. product & combinations ---------------------------------------------
def demo_product_combinations():
    print("\n--- 2. product / combinations ---")
    # product = nested for-loops in one call
    print(list(product("ab", [1, 2])))   # -> [('a', 1), ('a', 2), ('b', 1), ('b', 2)]
    print(len(list(product(range(2), repeat=3))))   # -> 8  (all 3-bit patterns)
    # combinations = order doesn't matter, no repeats
    print(list(combinations("ABC", 2)))  # -> [('A', 'B'), ('A', 'C'), ('B', 'C')]


# --- 3. groupby: group CONSECUTIVE items -----------------------------------
def demo_groupby():
    print("\n--- 3. groupby ---")
    words = ["apple", "avocado", "banana", "blueberry", "cherry", "apricot"]
    # groupby only groups ADJACENT equal keys, so sort by the same key first!
    for letter, group in groupby(sorted(words), key=lambda w: w[0]):
        print(letter, list(group))
    # -> a ['apple', 'apricot', 'avocado'] / b ['banana', 'blueberry'] / c ['cherry']
    print([(k, len(list(g))) for k, g in groupby("aaabccaa")])
    # -> [('a', 3), ('b', 1), ('c', 2), ('a', 2)]  (unsorted: 'a' appears twice)


# --- 4. islice: slicing for any iterator -----------------------------------
def demo_islice():
    print("\n--- 4. islice ---")
    evens = (n for n in count() if n % 2 == 0)      # infinite: can't use [:5]
    print(list(islice(evens, 5)))                   # -> [0, 2, 4, 6, 8]
    print(list(islice("abcdefgh", 2, 7, 2)))        # -> ['c', 'e', 'g'] (start, stop, step)


# --- 5. accumulate: running totals -----------------------------------------
def demo_accumulate():
    print("\n--- 5. accumulate ---")
    print(list(accumulate([1, 2, 3, 4])))           # -> [1, 3, 6, 10]
    print(list(accumulate([3, 1, 4, 1, 5], max)))   # -> [3, 3, 4, 4, 5] (running max)
    print(list(accumulate([1, 2, 3], operator.mul, initial=10)))  # -> [10, 10, 20, 60]


# --- 6. partial & reduce ----------------------------------------------------
def power(base, exp):
    return base ** exp


def demo_partial_reduce():
    print("\n--- 6. partial / reduce ---")
    square = partial(power, exp=2)       # a new function with exp frozen
    cube = partial(power, exp=3)
    print(square(5), cube(2))            # -> 25 8
    to_int_base2 = partial(int, base=2)
    print(to_int_base2("1011"))          # -> 11
    # reduce folds a sequence into one value: ((1*2)*3)*4
    print(reduce(operator.mul, [1, 2, 3, 4]))       # -> 24
    print(reduce(lambda acc, s: acc + len(s), ["ab", "cde"], 0))  # -> 5
    # (for plain sums use sum(); reduce shines for custom combining logic)


# --- 7. lru_cache: memoisation ---------------------------------------------
@lru_cache(maxsize=None)                 # functools.cache is the same thing
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


def demo_lru_cache():
    print("\n--- 7. lru_cache ---")
    print(fib(80))                 # -> 23416728348467685  (instant; uncached would take forever)
    info = fib.cache_info()
    print(info.hits, info.misses)  # -> 78 81  (each n computed only once)
    fib.cache_clear()
    # Arguments must be hashable (no lists/dicts) since they're dict keys.


# --- 8. cached_property: compute once per instance --------------------------
class Dataset:
    def __init__(self, values):
        self.values = values
        self.computations = 0

    @cached_property
    def stats(self):
        self.computations += 1     # count how often the body really runs
        return {"min": min(self.values), "max": max(self.values)}


def demo_cached_property():
    print("\n--- 8. cached_property ---")
    d = Dataset([4, 8, 1])
    print(d.stats, d.stats["max"])     # -> {'min': 1, 'max': 8} 8
    print(d.computations)              # -> 1  (second access used the cache)
    del d.stats                        # invalidate; next access recomputes
    d.stats
    print(d.computations)              # -> 2


# --- 9. singledispatch: overload by argument type ---------------------------
@singledispatch
def describe(obj):                     # fallback for unregistered types
    return f"something: {obj!r}"


@describe.register
def _(obj: int):                       # the type comes from the annotation
    return f"int with {len(str(abs(obj)))} digit(s)"


@describe.register
def _(obj: list):
    return f"list of {len(obj)} -> [{', '.join(describe(x) for x in obj)}]"


@describe.register(str)                # or pass the type explicitly
def _(obj):
    return f"string {obj!r}"


def demo_singledispatch():
    print("\n--- 9. singledispatch ---")
    print(describe(1234))              # -> int with 4 digit(s)
    print(describe("hi"))              # -> string 'hi'
    print(describe([7, "x"]))          # -> list of 2 -> [int with 1 digit(s), string 'x']
    print(describe(3.5))               # -> something: 3.5
    print(functools.singledispatch is singledispatch)   # -> True


if __name__ == "__main__":
    demo_chain()
    demo_product_combinations()
    demo_groupby()
    demo_islice()
    demo_accumulate()
    demo_partial_reduce()
    demo_lru_cache()
    demo_cached_property()
    demo_singledispatch()
