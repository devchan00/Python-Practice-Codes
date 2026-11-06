"""Lesson 5: Collections - list, tuple, dict, set.

Collections hold many values under one name. A list is ordered and
mutable (you can change it). A tuple is ordered and immutable. A dict maps
keys to values and keeps insertion order. A set holds unique items and
answers "is x in here?" very fast. Choosing the right one makes code both
clearer and quicker. This lesson shows each type and the methods and
operators listed on the cheatsheet.
"""


# --- 1. The four collection types at a glance ---
def overview():
    print("--- 1. Overview ---")
    nums = [1, 2, 3, 2]          # list: ordered, mutable, duplicates OK
    point = (1, 2)               # tuple: ordered, immutable
    ages = {"a": 1}              # dict: key -> value
    unique = {1, 2, 2, 2}        # set: duplicates are dropped
    print(nums, point, ages, unique)   # -> [1, 2, 3, 2] (1, 2) {'a': 1} {1, 2}

    # A one-item tuple needs a trailing comma; brackets alone just group.
    print(type((1,)), type((1)))       # -> <class 'tuple'> <class 'int'>
    # {} is an EMPTY DICT. An empty set must be written set().
    print(type({}), type(set()))       # -> <class 'dict'> <class 'set'>


# --- 2. List methods: adding and removing ---
def list_methods():
    print("\n--- 2. List methods ---")
    lst = [3, 1, 2]
    lst.append(4)            # add ONE item at the end
    print(lst)               # -> [3, 1, 2, 4]
    lst.extend([5, 6])       # add MANY items from any iterable
    print(lst)               # -> [3, 1, 2, 4, 5, 6]
    # Compare: append([5, 6]) would add the whole list as ONE item.

    lst.insert(0, 99)        # insert at index 0, shifting the rest right
    print(lst)               # -> [99, 3, 1, 2, 4, 5, 6]
    lst.remove(99)           # remove the FIRST item equal to 99
    print(lst)               # -> [3, 1, 2, 4, 5, 6]

    last = lst.pop()         # remove & return the last item
    second = lst.pop(1)      # remove & return the item at index 1
    print(last, second, lst)  # -> 6 1 [3, 2, 4, 5]

    # sort() and reverse() change the list IN PLACE and return None.
    lst.sort()
    print(lst)               # -> [2, 3, 4, 5]
    lst.reverse()
    print(lst)               # -> [5, 4, 3, 2]
    print(lst.sort())        # -> None   (so never write lst = lst.sort())
    # sorted(lst) instead returns a NEW sorted list and leaves lst alone.
    print(sorted([3, 1, 2]), lst)   # -> [1, 2, 3] [2, 3, 4, 5]

    try:
        lst.remove(42)
    except ValueError as e:
        print("ValueError:", e)     # -> ValueError: list.remove(x): x not in list


# --- 3. List slicing and copying ---
def list_slicing():
    print("\n--- 3. Slicing and copying ---")
    lst = [0, 1, 2, 3, 4, 5]
    print(lst[::2])          # -> [0, 2, 4]   every 2nd item
    print(lst[1:3])          # -> [1, 2]
    print(lst[-1])           # -> 5

    # `alias = lst` does NOT copy: both names point at the same list.
    alias = lst
    copy = lst[:]            # a shallow copy: a new list with the same items
    lst.append(6)
    print(alias)             # -> [0, 1, 2, 3, 4, 5, 6]   changed too!
    print(copy)              # -> [0, 1, 2, 3, 4, 5]      independent

    # "Shallow" means nested lists inside are still shared.
    grid = [[1, 2], [3, 4]]
    grid_copy = grid[:]
    grid[0].append(99)
    print(grid_copy)         # -> [[1, 2, 99], [3, 4]]


# --- 4. Tuples ---
def tuples():
    print("\n--- 4. Tuples ---")
    point = (3, 4)
    x, y = point             # unpacking works on any sequence
    print(x, y, point[0])    # -> 3 4 3
    try:
        point[0] = 10
    except TypeError as e:
        print("TypeError:", e)   # -> TypeError: 'tuple' object does not support item assignment
    # Why use a tuple? It signals "this is a fixed record", and because it
    # is immutable it can be used as a dict key or set item.
    distances = {(0, 0): "origin", (3, 4): "five away"}
    print(distances[(3, 4)])     # -> five away


# --- 5. Dicts: lookup, get, views ---
def dict_basics():
    print("\n--- 5. Dict basics ---")
    d = {"apple": 3, "pear": 5}
    print(d["apple"])            # -> 3
    d["kiwi"] = 7                # add or overwrite a key
    print(d)                     # -> {'apple': 3, 'pear': 5, 'kiwi': 7}

    # Square brackets raise KeyError for a missing key...
    try:
        d["mango"]
    except KeyError as e:
        print("KeyError:", e)    # -> KeyError: 'mango'
    # ...get() returns a default instead (None if you give none).
    print(d.get("mango", 0))     # -> 0
    print(d.get("mango"))        # -> None

    # keys(), values(), items() are live "views" you can loop over.
    print(list(d.keys()))        # -> ['apple', 'pear', 'kiwi']
    print(list(d.values()))      # -> [3, 5, 7]
    print(list(d.items()))       # -> [('apple', 3), ('pear', 5), ('kiwi', 7)]
    for fruit, count in d.items():
        print(f"{fruit}={count}", end=" ")   # -> apple=3 pear=5 kiwi=7
    print()


# --- 6. Dicts: merging, setdefault, pop ---
def dict_updates():
    print("\n--- 6. Dict merging and updating ---")
    d = {"a": 1, "b": 2}
    o = {"b": 20, "c": 30}

    merged = d | o               # NEW dict; on clashes the right side wins (3.9+)
    print(merged)                # -> {'a': 1, 'b': 20, 'c': 30}
    print(d)                     # -> {'a': 1, 'b': 2}   unchanged

    d.update(o)                  # changes d IN PLACE
    print(d)                     # -> {'a': 1, 'b': 20, 'c': 30}

    # setdefault: insert the key only if it is missing; returns the value.
    d.setdefault("z", 0)         # z is missing -> inserted
    d.setdefault("a", 100)       # a exists -> left alone
    print(d)                     # -> {'a': 1, 'b': 20, 'c': 30, 'z': 0}

    # Classic use: grouping items into lists.
    groups = {}
    for word in ["ant", "bee", "ape"]:
        groups.setdefault(word[0], []).append(word)
    print(groups)                # -> {'a': ['ant', 'ape'], 'b': ['bee']}

    removed = d.pop("z")         # remove the key and return its value
    print(removed, d)            # -> 0 {'a': 1, 'b': 20, 'c': 30}
    print(d.pop("nope", None))   # -> None   default avoids KeyError


# --- 7. Sets ---
def sets():
    print("\n--- 7. Sets ---")
    s = {1, 2}
    s.add(3)                 # add one item (no effect if already there)
    s.add(3)
    print(s)                 # -> {1, 2, 3}
    s.discard(2)             # remove if present...
    s.discard(42)            # ...and NO error if absent
    print(s)                 # -> {1, 3}
    # remove() is the strict version: it raises KeyError if absent.

    # Fast membership: a set checks `in` almost instantly, however large,
    # while a list has to scan item by item.
    print(3 in s)            # -> True

    # Handy trick: remove duplicates from a list.
    print(sorted(set([3, 1, 3, 2, 1])))   # -> [1, 2, 3]


# --- 8. Set operators ---
def set_operators():
    print("\n--- 8. Set operators ---")
    a = {1, 2, 3, 4}
    b = {3, 4, 5}
    print(a | b)     # -> {1, 2, 3, 4, 5}   union: in either
    print(a & b)     # -> {3, 4}            intersection: in both
    print(a - b)     # -> {1, 2}            difference: in a but not b
    print(a ^ b)     # -> {1, 2, 5}         symmetric difference: in exactly one

    # Real-world example: who is in both clubs?
    chess = {"Ana", "Bo", "Cy"}
    music = {"Bo", "Dee"}
    print(chess & music)     # -> {'Bo'}


if __name__ == "__main__":
    overview()
    list_methods()
    list_slicing()
    tuples()
    dict_basics()
    dict_updates()
    sets()
    set_operators()
