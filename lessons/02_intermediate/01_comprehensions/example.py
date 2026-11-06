"""Lesson 2.1 - Comprehensions.

Comprehensions are a compact, readable way to build a new list, dict or set
(or a lazy generator) from an existing iterable in a single expression. They
replace the common "make an empty container, loop, append" pattern, read like
plain English ("x squared for x in range if x is even"), and are usually a bit
faster than the equivalent loop because the looping happens inside CPython.
"""


# --- 1. List comprehensions ---
def list_comprehensions():
    print("--- 1. List comprehensions ---")

    # The long way: empty list + loop + append.
    squares_loop = []
    for x in range(10):
        if x % 2 == 0:
            squares_loop.append(x * x)

    # The same thing as one expression: [EXPRESSION for ITEM in ITERABLE if CONDITION]
    squares = [x * x for x in range(10) if x % 2 == 0]
    print(squares)                      # -> [0, 4, 16, 36, 64]
    print(squares == squares_loop)      # -> True

    # The condition is optional - without it every item is kept.
    words = ["apple", "Banana", "cherry"]
    print([w.upper() for w in words])   # -> ['APPLE', 'BANANA', 'CHERRY']

    # A ternary in the EXPRESSION part transforms every item (no filtering).
    # Note the position: "if/else" goes BEFORE "for"; a filter "if" goes AFTER.
    print(["even" if n % 2 == 0 else "odd" for n in range(4)])
    # -> ['even', 'odd', 'even', 'odd']


# --- 2. Dict comprehensions ---
def dict_comprehensions():
    print("\n--- 2. Dict comprehensions ---")

    pairs = [("a", 1), ("b", 2), ("c", 3)]
    # {KEY: VALUE for ...} builds a dict.
    d = {k: v for k, v in pairs}
    print(d)                            # -> {'a': 1, 'b': 2, 'c': 3}

    # Handy for inverting a mapping (values must be hashable and unique).
    inverted = {v: k for k, v in d.items()}
    print(inverted)                     # -> {1: 'a', 2: 'b', 3: 'c'}

    # Build a lookup table from a list, with a filter.
    words = ["hi", "hello", "hey", "yo"]
    lengths = {w: len(w) for w in words if len(w) > 2}
    print(lengths)                      # -> {'hello': 5, 'hey': 3}


# --- 3. Set comprehensions ---
def set_comprehensions():
    print("\n--- 3. Set comprehensions ---")

    nums = [1, 2, 3, 4, 5, 6, 7]
    # {EXPRESSION for ...} (no colon) builds a set: duplicates vanish.
    remainders = {x % 3 for x in nums}
    print(sorted(remainders))           # -> [0, 1, 2]   (sorted because sets are unordered)

    # Unique first letters, case-insensitive.
    names = ["Ann", "alice", "Bob", "bill", "Cy"]
    print(sorted({n[0].lower() for n in names}))  # -> ['a', 'b', 'c']

    # Gotcha: {} on its own is an empty DICT, not a set. Use set().
    print(type({}), type(set()))        # -> <class 'dict'> <class 'set'>


# --- 4. Generator expressions ---
def generator_expressions():
    print("\n--- 4. Generator expressions ---")

    nums = [1, 2, 3, 4]
    # Round brackets give a lazy generator: nothing is computed yet.
    gen = (x * x for x in nums)
    print(type(gen).__name__)           # -> generator

    # Values are produced one at a time, on demand.
    print(next(gen))                    # -> 1
    print(list(gen))                    # -> [4, 9, 16]  (continues where it left off)
    print(list(gen))                    # -> []  (a generator is used up after one pass)

    # WHY: a generator never stores the whole sequence, so it uses O(1) memory.
    # Perfect for feeding straight into sum/max/any. When it is the only
    # argument you can drop the extra brackets.
    print(sum(x * x for x in range(1_000_000)))   # -> 333332833333500000


# --- 5. Nested comprehensions (flatten) ---
def nested_comprehensions():
    print("\n--- 5. Nested comprehensions ---")

    grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    # Read the "for" clauses left to right, just like nested loops:
    #   for row in grid:
    #       for y in row:
    #           result.append(y)
    flat = [y for row in grid for y in row]
    print(flat)                         # -> [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # A comprehension INSIDE a comprehension builds a nested structure.
    # Here: transpose the grid (rows become columns).
    transposed = [[row[i] for row in grid] for i in range(3)]
    print(transposed)                   # -> [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

    # All (x, y) pairs where x < y.
    print([(x, y) for x in range(3) for y in range(3) if x < y])
    # -> [(0, 1), (0, 2), (1, 2)]


# --- 6. When NOT to use a comprehension ---
def readability():
    print("\n--- 6. Readability ---")

    # Comprehensions are for BUILDING a collection. If you only want side
    # effects (printing, writing files), use a normal for loop instead -
    # [print(x) for x in ...] builds a useless list of None values.
    for x in ["a", "b"]:
        print(x)                        # -> a  then  b

    # The loop variable does NOT leak out of a comprehension (unlike a for loop).
    y = "outer"
    _ = [y for y in range(3)]
    print(y)                            # -> outer


if __name__ == "__main__":
    list_comprehensions()
    dict_comprehensions()
    set_comprehensions()
    generator_expressions()
    nested_comprehensions()
    readability()
