"""Lesson 2.2 - Functional helpers.

Python ships a set of built-in functions that work on any iterable and accept
other functions as arguments: lambda for tiny throwaway functions, sorted with
a key function, the lazy map/filter/zip, the short-circuiting any/all, and the
aggregators sum/min/max. Combining them lets you express "transform, filter,
pair up, summarise" without writing explicit loops.
"""


# --- 1. lambda: anonymous one-expression functions ---
def lambdas():
    print("--- 1. lambda ---")

    double = lambda x: x * 2            # same as: def double(x): return x * 2
    print(double(21))                   # -> 42

    # A lambda may only contain ONE expression (no statements, no return).
    # WHY use it: as a short, inline argument to another function (see below).
    # If you are giving it a name, a normal def is clearer and has a real __name__.
    print(double.__name__)              # -> <lambda>


# --- 2. sorted with a key function ---
def sorting():
    print("\n--- 2. sorted(key=...) ---")

    people = [("ann", 31), ("bob", 25), ("cy", 31), ("dee", 19)]

    # key= is called once per item; items are ordered by its return value.
    by_age = sorted(people, key=lambda t: t[1])
    print(by_age)
    # -> [('dee', 19), ('bob', 25), ('ann', 31), ('cy', 31)]
    # Stable sort: ann and cy tie on 31 and keep their original order.

    print(sorted(people, key=lambda t: t[1], reverse=True)[0])  # -> ('ann', 31)

    # Sort by several keys by returning a tuple: age descending, then name.
    print(sorted(people, key=lambda t: (-t[1], t[0])))
    # -> [('ann', 31), ('cy', 31), ('bob', 25), ('dee', 19)]

    # Any function works as a key, not just lambdas.
    print(sorted(["banana", "Apple", "cherry"], key=str.lower))
    # -> ['Apple', 'banana', 'cherry']   (case-insensitive)

    # sorted() returns a NEW list; list.sort() sorts in place and returns None.
    nums = [3, 1, 2]
    print(nums.sort(), nums)            # -> None [1, 2, 3]


# --- 3. map and filter (lazy) ---
def map_filter():
    print("\n--- 3. map / filter ---")

    nums = [1, 2, 3, 4, 5]
    m = map(lambda x: x * 10, nums)
    print(m)                            # -> <map object at 0x...>  (lazy: nothing computed yet)
    print(list(m))                      # -> [10, 20, 30, 40, 50]

    # filter keeps items for which the function returns something truthy.
    print(list(filter(lambda x: x % 2, nums)))   # -> [1, 3, 5]

    # filter(None, it) keeps only truthy items - a quick way to drop blanks.
    print(list(filter(None, ["a", "", "b", None, 0])))  # -> ['a', 'b']

    # map with an existing function is very clean.
    print(list(map(int, ["7", "8", "9"])))      # -> [7, 8, 9]

    # Comprehensions do the same job and are often more readable:
    print([x * 10 for x in nums if x % 2])      # -> [10, 30, 50]


# --- 4. zip: pair up and transpose ---
def zipping():
    print("\n--- 4. zip ---")

    names = ["ann", "bob", "cy"]
    scores = [90, 85, 77]
    print(list(zip(names, scores)))     # -> [('ann', 90), ('bob', 85), ('cy', 77)]
    print(dict(zip(names, scores)))     # -> {'ann': 90, 'bob': 85, 'cy': 77}

    # zip stops at the SHORTEST input - extra items are silently dropped...
    print(list(zip([1, 2, 3], "ab")))   # -> [(1, 'a'), (2, 'b')]

    # ...so pass strict=True when the lengths must match (Python 3.10+).
    try:
        list(zip([1, 2, 3], "ab", strict=True))
    except ValueError as e:
        print("ValueError:", e)         # -> ValueError: zip() argument 2 is shorter than argument 1

    # zip(*rows) transposes: * unpacks the rows as separate arguments.
    rows = [(1, 2, 3), (4, 5, 6)]
    print(list(zip(*rows)))             # -> [(1, 4), (2, 5), (3, 6)]


# --- 5. any and all ---
def any_all():
    print("\n--- 5. any / all ---")

    nums = [2, 4, 7, 8]
    print(any(n % 2 for n in nums))     # -> True   (at least one odd)
    print(all(n > 0 for n in nums))     # -> True   (every one positive)
    print(all(n % 2 == 0 for n in nums))  # -> False

    # Both short-circuit: they stop as soon as the answer is known.
    # Edge cases worth remembering:
    print(any([]), all([]))             # -> False True   (all() of nothing is True)


# --- 6. sum, min, max ---
def aggregates():
    print("\n--- 6. sum / min / max ---")

    nums = [4, 9, 1, 7]
    print(sum(nums), min(nums), max(nums))   # -> 21 1 9
    print(sum(nums, start=100))              # -> 121

    words = ["pear", "fig", "banana"]
    # key= works here too: compare by length, return the original item.
    print(max(words, key=len))          # -> banana
    print(min(words, key=len))          # -> fig

    # On an empty iterable min/max raise ValueError unless you give default=.
    print(max([], default="nothing"))   # -> nothing


# --- 7. Putting it together ---
def pipeline():
    print("\n--- 7. Combined ---")

    orders = [("pen", 1.5, 10), ("book", 12.0, 2), ("bag", 30.0, 0)]
    # Total value of items that are in stock, most valuable first.
    in_stock = filter(lambda o: o[2] > 0, orders)
    totals = map(lambda o: (o[0], o[1] * o[2]), in_stock)
    print(sorted(totals, key=lambda t: t[1], reverse=True))
    # -> [('book', 24.0), ('pen', 15.0)]


if __name__ == "__main__":
    lambdas()
    sorting()
    map_filter()
    zipping()
    any_all()
    aggregates()
    pipeline()
