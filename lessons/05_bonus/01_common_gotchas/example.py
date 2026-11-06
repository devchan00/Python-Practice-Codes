"""Bonus 1 - Common gotchas: the bug and the fix, side by side.

Every row of the cheatsheet's "Common gotchas" table, as runnable code. Each
section first shows the surprising BUG, then the FIX, and explains WHY Python
behaves that way: mutable defaults, late-binding closures, ``==`` vs ``is``,
mutating a list while iterating, aliasing, floating-point error, bare
``except``, ``from x import *``, ``/`` vs ``//`` and ``str + int``.
"""

import copy
import math
from decimal import Decimal


# --- 1. Mutable default argument: def f(x=[]) ---
def append_bug(item, bucket=[]):  # the [] is created ONCE, when def runs
    bucket.append(item)
    return bucket


def append_fix(item, bucket=None):  # use None as "not given"
    if bucket is None:
        bucket = []  # a NEW list on every call
    bucket.append(item)
    return bucket


def demo_mutable_default() -> None:
    print("\n--- 1. Mutable default ---")
    print("bug:", append_bug(1), append_bug(2))  # -> bug: [1, 2] [1, 2]  (shared!)
    print("fix:", append_fix(1), append_fix(2))  # -> fix: [1] [2]
    print("the shared default lives here:", append_bug.__defaults__)  # -> ([1, 2],)


# --- 2. Late binding in closures: [lambda: i for i in r] ---
def demo_late_binding() -> None:
    print("\n--- 2. Late binding ---")
    bug = [lambda: i for i in range(3)]
    print("bug:", [f() for f in bug])  # -> bug: [2, 2, 2]
    # Each lambda looks up `i` when CALLED, and by then the loop has finished.
    fix = [lambda i=i: i for i in range(3)]  # default captures the value NOW
    print("fix:", [f() for f in fix])  # -> fix: [0, 1, 2]


# --- 3. a == b vs a is b ---
def demo_eq_vs_is() -> None:
    print("\n--- 3. == vs is ---")
    a = [1, 2, 3]
    b = [1, 2, 3]
    print("a == b:", a == b)  # -> True   same VALUE
    print("a is b:", a is b)  # -> False  different OBJECTS
    x = "hello world"
    y = " ".join(["hello", "world"])  # equal text, built at runtime
    print("bug: x is y ->", x is y)  # -> False: `is` asks "same object?", not "same text?"
    print("fix: x == y ->", x == y)  # -> True
    # Small ints and some strings are cached, so `is` SOMETIMES appears to
    # work - that's exactly what makes this bug sneaky.
    value = None
    print("`is` is right for singletons:", value is None)  # -> True  (None, True, False)


# --- 4. Mutating a list while iterating over it ---
def demo_mutate_while_iterating() -> None:
    print("\n--- 4. Mutating while iterating ---")
    lst = [1, 2, 2, 3, 4]
    for x in lst:
        if x % 2 == 0:
            lst.remove(x)  # shifts later items left -> the loop skips one
    print("bug:", lst)  # -> bug: [1, 2, 3]  (a 2 survived!)

    lst = [1, 2, 2, 3, 4]
    for x in lst[:]:  # iterate over a COPY, change the original
        if x % 2 == 0:
            lst.remove(x)
    print("fix (copy):", lst)  # -> fix (copy): [1, 3]
    lst = [1, 2, 2, 3, 4]
    print("fix (comprehension):", [x for x in lst if x % 2 != 0])  # -> [1, 3]  (best)


# --- 5. b = a is an alias, not a copy ---
def demo_alias() -> None:
    print("\n--- 5. Alias vs copy ---")
    a = [1, 2, [3, 4]]
    b = a  # another NAME for the same list
    b.append(5)
    print("bug: a =", a)  # -> bug: a = [1, 2, [3, 4], 5]  (a changed too)

    a = [1, 2, [3, 4]]
    shallow = a.copy()  # new outer list, SAME inner list
    shallow[2].append(99)
    print("shallow copy: a =", a)  # -> [1, 2, [3, 4, 99]]  inner list still shared

    a = [1, 2, [3, 4]]
    deep = copy.deepcopy(a)  # copies everything, recursively
    deep[2].append(99)
    print("fix (deepcopy): a =", a, "deep =", deep)  # -> a unchanged


# --- 6. 0.1 + 0.2 != 0.3 ---
def demo_float() -> None:
    print("\n--- 6. Floating point ---")
    print("bug:", 0.1 + 0.2 == 0.3, 0.1 + 0.2)  # -> bug: False 0.30000000000000004
    # Binary floats can't represent 0.1 exactly (like 1/3 in decimal).
    print("fix isclose:", math.isclose(0.1 + 0.2, 0.3))  # -> True
    print("fix Decimal:", Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))  # -> True
    # Use Decimal (from STRINGS) for money; Decimal(0.1) inherits the float error.


# --- 7. Bare except: hides bugs ---
def parse_bug(text):
    try:
        return int(txt)  # typo! NameError... silently swallowed below
    except:  # noqa: E722 - catches EVERYTHING, even KeyboardInterrupt
        return 0


def parse_fix(text):
    try:
        return int(text)
    except ValueError:  # only the failure we expect
        return 0


def demo_bare_except() -> None:
    print("\n--- 7. Bare except ---")
    print("bug:", parse_bug("42"))  # -> bug: 0   (the NameError was hidden!)
    print("fix:", parse_fix("42"), parse_fix("abc"))  # -> fix: 42 0
    # With the fix, the typo would raise NameError immediately - which is good.


# --- 8. from x import * pollutes the namespace ---
def demo_import_star() -> None:
    print("\n--- 8. from x import * ---")
    ns: dict = {}
    exec("from math import *\nfrom cmath import *\nresult = sqrt(-1)", ns)
    print("bug: sqrt(-1) =", ns["result"])  # -> 1j: cmath's sqrt silently replaced math's
    print("     names dumped into namespace:", len(ns) - 2)  # dozens of unknown names
    # (exec is used here ONLY to show a star-import in an isolated namespace.)
    from math import sqrt  # fix: import explicitly
    print("fix: math.sqrt(4) =", sqrt(4), "| explicit and greppable")  # -> 2.0


# --- 9. / always returns float ---
def demo_division() -> None:
    print("\n--- 9. / vs // ---")
    items = ["a", "b", "c", "d"]
    mid = len(items) / 2
    print("bug: 10 / 2 =", 10 / 2, "| mid =", mid)  # -> 5.0 | mid = 2.0
    try:
        items[mid]
    except TypeError as e:
        print("     items[mid] ->", e)  # -> list indices must be integers or slices, not float
    print("fix: 10 // 2 =", 10 // 2, "| items[len//2] =", items[len(items) // 2])  # -> 5 | c
    print("note: -7 // 2 =", -7 // 2)  # -> -4  (floor division rounds DOWN)


# --- 10. 'a' + 1 -> TypeError ---
def demo_str_plus_int() -> None:
    print("\n--- 10. str + int ---")
    age = 36
    try:
        print("Age: " + age)
    except TypeError as e:
        print("bug:", e)  # -> can only concatenate str (not "int") to str
    # Python never guesses: is "1" + 1 == "11" or 2? Convert explicitly.
    print("fix:", "Age: " + str(age), "|", f"Age: {age}", "|", int("1") + 1)
    # -> fix: Age: 36 | Age: 36 | 2


def main() -> None:
    demo_mutable_default()
    demo_late_binding()
    demo_eq_vs_is()
    demo_mutate_while_iterating()
    demo_alias()
    demo_float()
    demo_bare_except()
    demo_import_star()
    demo_division()
    demo_str_plus_int()


if __name__ == "__main__":
    main()
