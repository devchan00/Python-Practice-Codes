"""Reserved keywords, part 2: functions, scope, classes, exceptions, imports, with.

This file covers the keywords you use to build and organise programs: def,
return, lambda (functions); global, nonlocal (scope); class (objects); try,
except, else, finally, raise, assert (error handling); import, from, as
(modules); and with (context managers that guarantee cleanup). Each concept is
shown with a short, runnable example and a comment describing the output.
"""

import os
import tempfile


# --- 1. Functions: def / return / lambda ---
def add(a, b):
    return a + b                          # return exits the function AND sends back a value


def first_negative(nums):
    for n in nums:
        if n < 0:
            return n                      # return can exit early, even from inside a loop
    return None


def demo_functions():
    print(add(2, 3))                      # -> 5
    print(first_negative([4, -1, -7]))    # -> -1

    # lambda = a tiny anonymous function made of ONE expression (no statements).
    double = lambda x: x * 2
    print(double(21))                     # -> 42
    # Its real use is as a short throwaway argument, e.g. a sort key:
    words = ["banana", "kiwi", "apple"]
    print(sorted(words, key=lambda w: len(w)))   # -> ['kiwi', 'apple', 'banana']


# --- 2. Scope: global / nonlocal ---
counter = 0                               # module-level ("global") variable


def increment():
    global counter                        # without this line, `counter += 1` would
    counter += 1                          # raise UnboundLocalError: Python would treat
                                          # counter as a brand-new local variable.


def make_accumulator():
    total = 0

    def add_to(n):
        nonlocal total                    # rebind `total` from the ENCLOSING function,
        total += n                        # not a global and not a new local
        return total

    return add_to


def demo_scope():
    increment()
    increment()
    print(counter)                        # -> 2
    acc = make_accumulator()
    acc(10)
    print(acc(5))                         # -> 15  (acc remembers total between calls)
    # Tip: prefer returning values over `global`; it keeps code easier to test.


# --- 3. Classes: class ---
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."


class Dog(Animal):                        # Dog inherits from Animal
    def speak(self):
        return f"{self.name} says woof"


def demo_class():
    d = Dog("Rex")
    print(d.speak())                      # -> Rex says woof
    print(isinstance(d, Animal))          # -> True  (a Dog IS an Animal)


# --- 4. Exceptions: try / except / else / finally ---
def parse_int(text):
    try:                                  # code that might fail goes here
        value = int(text)
    except ValueError as e:               # runs only if a ValueError happened
        print("  bad input:", e)
        return None
    else:                                 # runs only if NO exception happened
        print("  parsed fine")
        return value
    finally:                              # ALWAYS runs - even after return - for cleanup
        print("  finally: done with", repr(text))


def demo_try():
    print(parse_int("42"))
    # ->   parsed fine
    # ->   finally: done with '42'
    # -> 42
    print(parse_int("abc"))
    # ->   bad input: invalid literal for int() with base 10: 'abc'
    # ->   finally: done with 'abc'
    # -> None


# --- 5. raise / assert ---
def set_age(age):
    if age < 0:
        raise ValueError("bad")           # raise = throw an exception yourself
    return age


def demo_raise_assert():
    try:
        set_age(-1)
    except ValueError as e:
        print("caught:", e)               # -> caught: bad

    # Bare `raise` inside an except re-throws the SAME exception (after logging, say).
    try:
        try:
            1 / 0
        except ZeroDivisionError:
            print("logging the error, then re-raising")
            raise
    except ZeroDivisionError as e:
        print("outer caught:", e)         # -> outer caught: division by zero

    # `raise ... from ...` chains errors so the traceback shows the real cause.
    try:
        try:
            {}["missing"]
        except KeyError as e:
            raise RuntimeError("config broken") from e
    except RuntimeError as e:
        print(e, "| cause:", repr(e.__cause__))   # -> config broken | cause: KeyError('missing')

    # assert = sanity check for debugging/tests. Raises AssertionError if false.
    n = 5
    assert n > 0, "n must be > 0"         # passes silently
    try:
        n = -1
        assert n > 0, "n must be > 0"
    except AssertionError as e:
        print("AssertionError:", e)       # -> AssertionError: n must be > 0
    # WARNING: `python -O` strips asserts, so never use them to validate user input.


# --- 6. Imports: import / from / as ---
def demo_imports():
    import json                           # load a whole module; use it as json.xxx
    print(json.dumps({"a": 1}))           # -> {"a": 1}

    from os import path                   # pull ONE name out of a module
    print(path.basename("/tmp/file.txt")) # -> file.txt

    import collections as col             # `as` gives an alias (like `import numpy as np`)
    print(col.Counter("aab"))             # -> Counter({'a': 2, 'b': 1})

    from math import sqrt as square_root  # alias a single imported name
    print(square_root(16))                # -> 4.0
    # `as` is also used in `except E as e` (above) and `with ... as f` (below).


# --- 7. with: context managers guarantee cleanup ---
def demo_with():
    # `with` calls setup on entry and cleanup on exit - even if an error happens.
    # For files that means the file is ALWAYS closed. We use a temp dir so no
    # files are left behind.
    with tempfile.TemporaryDirectory() as folder:
        p = os.path.join(folder, "notes.txt")
        with open(p, "w") as f:
            f.write("hello")
        print(f.closed)                   # -> True  (closed automatically)
        with open(p) as f:
            print(f.read())               # -> hello
    print(os.path.exists(folder))         # -> False (temp folder cleaned up too)


if __name__ == "__main__":
    print("--- 1. functions ---");      demo_functions()
    print("--- 2. scope ---");          demo_scope()
    print("--- 3. class ---");          demo_class()
    print("--- 4. try ---");            demo_try()
    print("--- 5. raise/assert ---");   demo_raise_assert()
    print("--- 6. imports ---");        demo_imports()
    print("--- 7. with ---");           demo_with()
