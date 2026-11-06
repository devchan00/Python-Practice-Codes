"""Built-in functions, part 2: collections and iteration.

These built-ins build collections (dict, list, set, tuple, frozenset) and work
with any iterable: len, all, any, sum, max/min, sorted, reversed, enumerate,
zip, map, filter, range, slice, iter/next and the async versions aiter/anext.
They are the everyday tools that make Python loops short and readable.
"""

import asyncio


# --- 1. dict / list / set / tuple / frozenset: build collections ---
def demo_constructors():
    print(list("abc"))                      # -> ['a', 'b', 'c']   any iterable -> list
    print(tuple([1, 2]))                    # -> (1, 2)            immutable sequence
    print(set([1, 1, 2]))                   # -> {1, 2}            duplicates removed
    print(dict(a=1, b=2))                   # -> {'a': 1, 'b': 2}
    print(dict([("x", 1), ("y", 2)]))       # -> {'x': 1, 'y': 2}  from pairs
    fs = frozenset([1, 2, 2])
    print(fs)                               # -> frozenset({1, 2})
    # frozenset is immutable, so it's hashable and can be a dict key or set item:
    print({fs: "ok"}[frozenset({1, 2})])    # -> ok


# --- 2. len / all / any / sum ---
def demo_len_all_any_sum():
    print(len([1, 2, 3]), len("hello"), len({"a": 1}))   # -> 3 5 1
    print(all([1, "x", True]))              # -> True   every item truthy
    print(all([]))                          # -> True   (nothing is falsy in an empty list!)
    print(any([0, "", 5]))                  # -> True   at least one truthy
    print(any([]))                          # -> False
    print(sum([1, 2, 3]))                   # -> 6
    print(sum([1, 2, 3], 10))               # -> 16     second arg = starting value
    print(any(n > 2 for n in [1, 2, 3]))    # -> True   works great with generators


# --- 3. max / min with key= ---
def demo_max_min():
    print(max(3, 9, 2), min([3, 9, 2]))     # -> 9 2
    words = ["kiwi", "banana", "fig"]
    print(max(words, key=len))              # -> banana  key = "compare by this"
    print(min(words, key=len))              # -> fig
    print(max([], default=0))               # -> 0       avoids ValueError on empty input


# --- 4. sorted / reversed ---
def demo_sorted_reversed():
    nums = [3, 1, 2]
    print(sorted(nums), nums)               # -> [1, 2, 3] [3, 1, 2]  NEW list; original unchanged
    print(sorted(nums, reverse=True))       # -> [3, 2, 1]
    people = [("Ann", 30), ("Bob", 25)]
    print(sorted(people, key=lambda p: p[1]))   # -> [('Bob', 25), ('Ann', 30)]
    print(list(reversed("abc")))            # -> ['c', 'b', 'a']  reversed gives an ITERATOR


# --- 5. enumerate / zip ---
def demo_enumerate_zip():
    for i, fruit in enumerate(["apple", "pear"], start=1):
        print(i, fruit)                     # -> 1 apple / 2 pear
    names, ages = ["Ann", "Bob"], [30, 25]
    print(list(zip(names, ages)))           # -> [('Ann', 30), ('Bob', 25)]
    print(dict(zip(names, ages)))           # -> {'Ann': 30, 'Bob': 25}
    # zip stops at the SHORTEST input; strict=True raises if lengths differ.
    print(list(zip([1, 2, 3], "ab")))       # -> [(1, 'a'), (2, 'b')]


# --- 6. map / filter ---
def demo_map_filter():
    print(list(map(str.upper, ["a", "b"]))) # -> ['A', 'B']   apply f to each item
    print(list(map(lambda x: x * x, [1, 2, 3])))   # -> [1, 4, 9]
    print(list(filter(lambda x: x % 2 == 0, range(7))))   # -> [0, 2, 4, 6]
    print(list(filter(None, [0, 1, "", "a"])))     # -> [1, 'a']  None = keep truthy
    # Both are lazy (return iterators), which is why we wrap them in list().
    # A comprehension is often clearer: [x * x for x in nums if x % 2 == 0]


# --- 7. range / slice ---
def demo_range_slice():
    print(list(range(5)))                   # -> [0, 1, 2, 3, 4]   stop is EXCLUDED
    print(list(range(2, 10, 3)))            # -> [2, 5, 8]
    print(list(range(5, 0, -1)))            # -> [5, 4, 3, 2, 1]
    print(range(10**12)[-1])                # -> 999999999999  (range never builds a list)

    s = slice(1, 5, 2)                      # a reusable "[1:5:2]"
    print("abcdefg"[s], [0, 1, 2, 3, 4, 5][s])   # -> bd [1, 3]


# --- 8. iter / next: manual iteration ---
def demo_iter_next():
    it = iter([10, 20])
    print(next(it), next(it))               # -> 10 20
    print(next(it, "done"))                 # -> done   default instead of StopIteration
    # This is exactly what a `for` loop does behind the scenes.


# --- 9. aiter / anext: async iteration ---
async def countdown(n):
    while n > 0:
        await asyncio.sleep(0)
        yield n
        n -= 1


async def demo_aiter_anext():
    it = aiter(countdown(3))                # async version of iter()
    print(await anext(it))                  # -> 3
    print(await anext(it))                  # -> 2
    print(await anext(it), await anext(it, "end"))   # -> 1 end


if __name__ == "__main__":
    print("--- 1. constructors ---");      demo_constructors()
    print("--- 2. len/all/any/sum ---");   demo_len_all_any_sum()
    print("--- 3. max/min ---");           demo_max_min()
    print("--- 4. sorted/reversed ---");   demo_sorted_reversed()
    print("--- 5. enumerate/zip ---");     demo_enumerate_zip()
    print("--- 6. map/filter ---");        demo_map_filter()
    print("--- 7. range/slice ---");       demo_range_slice()
    print("--- 8. iter/next ---");         demo_iter_next()
    print("--- 9. aiter/anext ---");       asyncio.run(demo_aiter_anext())
