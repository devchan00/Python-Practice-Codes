"""Lesson 2.4 - Modules & packages.

A module is just a .py file; a package is a folder of modules marked with an
__init__.py file. `import` loads a module once, caches it in sys.modules and
gives you a namespace to reach its contents. This file shows the different
import forms, a real package (./mypkg) and the `if __name__ == "__main__"`
guard. A tour of the most useful standard-library modules lives in
stdlib_tour.py, which this file imports and runs.
"""

import sys

# Importing our own modules would normally write cached bytecode into
# __pycache__ folders. Turn that off so the lesson leaves no files behind.
sys.dont_write_bytecode = True

# --- 1. Import forms ---
import math                         # import a whole module; use math.sqrt
import json as js                   # import with an alias
from math import pi, sqrt           # import specific names
from collections import Counter as C   # specific name with an alias

import mypkg                        # our own package (folder ./mypkg)
from mypkg import greet             # re-exported in mypkg/__init__.py
from mypkg.greetings import DEFAULT_GREETING   # reach into a submodule

import stdlib_tour                  # another module in this folder


def import_forms():
    print("--- 1. Import forms ---")
    print(math.floor(2.7))          # -> 2      (module.name)
    print(js.dumps([1, 2]))         # -> [1, 2] (alias)
    print(round(sqrt(2), 3), round(pi, 2))   # -> 1.414 3.14  (names imported directly)
    print(C("hello").most_common(1))         # -> [('l', 2)]

    # WHY prefer `import math` over `from math import *`: the module prefix
    # shows where a name comes from and avoids silently overwriting your own
    # names. Star imports are discouraged outside interactive sessions.


# --- 2. Using a package ---
def using_package():
    print("\n--- 2. Our package: mypkg ---")
    print(greet("Ada"))                         # -> Hello, Ada!
    print(mypkg.shout("Ada"))                   # -> HELLO, ADA!
    print(mypkg.__version__)                    # -> 1.0.0
    print(DEFAULT_GREETING)                     # -> Hello
    # __name__ of an imported module is its dotted import path.
    print(mypkg.greetings.__name__)             # -> mypkg.greetings

    # How did Python find mypkg? sys.path[0] is the folder of the script being
    # run, so this works no matter which directory you launch it from.
    print("mypkg.greetings" in sys.modules)     # -> True  (imports are cached)


# --- 3. if __name__ == "__main__" ---
def main_guard():
    print("\n--- 3. __name__ ---")
    # When a file is run directly its __name__ is "__main__"; when it is
    # imported, __name__ is the module's name. The guard at the bottom of this
    # file therefore runs the demos only for `python example.py`, and lets
    # other code `import example` to reuse its functions without side effects.
    print(__name__)                     # -> __main__
    print(stdlib_tour.__name__)         # -> stdlib_tour


if __name__ == "__main__":
    import_forms()
    using_package()
    main_guard()
    stdlib_tour.run_all()
