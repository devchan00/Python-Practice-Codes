"""Lesson 2.3 - Arguments & scope.

Python functions have a rich parameter syntax: defaults, *args (extra
positional arguments collected into a tuple), **kwargs (extra keyword
arguments collected into a dict), positional-only parameters before `/` and
keyword-only parameters after `*`. The same * and ** symbols unpack sequences
and dicts when CALLING a function. Finally, names are looked up in LEGB order
(Local, Enclosing, Global, Built-in), and `global` / `nonlocal` let you rebind
names that live in an outer scope.
"""


# --- 1. Defaults, *args and **kwargs ---
def f(a, b=2, *args, key=None, **kwargs):
    """a: required, b: has a default, args: tuple, key: keyword-only, kwargs: dict."""
    return f"a={a} b={b} args={args} key={key} kwargs={kwargs}"


def args_and_kwargs():
    print("--- 1. defaults, *args, **kwargs ---")
    print(f(1))
    # -> a=1 b=2 args=() key=None kwargs={}
    print(f(1, 5, 6, 7))
    # -> a=1 b=5 args=(6, 7) key=None kwargs={}
    print(f(1, key="k", color="red", size=3))
    # -> a=1 b=2 args=() key=k kwargs={'color': 'red', 'size': 3}

    # WHY: *args/**kwargs let a function accept any number of extra
    # arguments - useful for wrappers that just pass them on.
    def total(*numbers):
        return sum(numbers)
    print(total(1, 2, 3, 4))            # -> 10

    # Gotcha: defaults are evaluated ONCE, when the def runs. A mutable
    # default (list/dict) is shared between calls.
    def bad_append(item, bucket=[]):
        bucket.append(item)
        return bucket

    def good_append(item, bucket=None):
        if bucket is None:              # create a fresh list on every call
            bucket = []
        bucket.append(item)
        return bucket

    bad_append(1)
    print(bad_append(2))                # -> [1, 2]   (surprise!)
    good_append(1)
    print(good_append(2))               # -> [2]


# --- 2. Positional-only (/) and keyword-only (*) ---
def g(pos_only, /, normal, *, kw_only):
    return f"pos_only={pos_only} normal={normal} kw_only={kw_only}"


def special_parameters():
    print("\n--- 2. positional-only / and keyword-only * ---")
    print(g(1, 2, kw_only=3))           # -> pos_only=1 normal=2 kw_only=3
    print(g(1, normal=2, kw_only=3))    # -> same: 'normal' may be either way

    try:
        g(pos_only=1, normal=2, kw_only=3)   # names before / can't be keywords
    except TypeError as e:
        print("TypeError:", e)
        # -> TypeError: g() got some positional-only arguments passed as keyword arguments: 'pos_only'

    try:
        g(1, 2, 3)                           # names after * must be keywords
    except TypeError as e:
        print("TypeError:", e)
        # -> TypeError: g() takes 2 positional arguments but 3 were given

    # WHY: keyword-only forces call sites to be self-documenting
    # (connect(timeout=5) instead of a mystery connect(5)). Positional-only
    # lets you rename a parameter later without breaking callers.


# --- 3. Unpacking when calling ---
def unpacking():
    print("\n--- 3. unpacking with * and ** ---")
    print(f(*[1, 2, 3], **{"key": 1}))
    # -> a=1 b=2 args=(3,) key=1 kwargs={}

    point = (3, 4)
    opts = {"sep": " | ", "end": "\n"}
    print(*point, **opts)               # -> 3 | 4   (same as print(3, 4, sep=" | "))

    # The same syntax merges collections and does "rest" unpacking.
    first, *rest = [10, 20, 30, 40]
    print(first, rest)                  # -> 10 [20, 30, 40]
    print([*"ab", *range(2)])           # -> ['a', 'b', 0, 1]
    print({**{"a": 1}, **{"b": 2, "a": 9}})   # -> {'a': 9, 'b': 2} (later wins)


# --- 4. LEGB scope lookup ---
x = "global x"                          # G: module-level (global) scope


def legb():
    print("\n--- 4. LEGB ---")
    x = "enclosing x"                   # E: for inner() this is the enclosing scope

    def inner():
        x = "local x"                   # L: local to inner()
        print(x)                        # -> local x
        print(len("abc"))               # -> 3   'len' found in B: built-ins
    inner()

    def inner_no_local():
        print(x)                        # -> enclosing x   (no local x, so look outward)
    inner_no_local()

    print(globals()["x"])               # -> global x   (untouched)

    # Assigning to a name ANYWHERE in a function makes it local everywhere in
    # that function, so reading it before the assignment fails:
    counter = 0

    def broken():
        try:
            print(counter)              # counter is local here (assigned below)
        except UnboundLocalError as e:
            print("UnboundLocalError:", e)
        counter = 1                     # noqa: F841  (the assignment that causes it)
    broken()
    # -> UnboundLocalError: cannot access local variable 'counter' where it is not associated with a value


# --- 5. global and nonlocal ---
count = 0


def increment_global():
    global count                        # rebind the MODULE-level name
    count += 1


def make_counter():
    n = 0

    def step():
        nonlocal n                      # rebind the ENCLOSING function's name
        n += 1
        return n
    return step


def global_nonlocal():
    print("\n--- 5. global / nonlocal ---")
    increment_global()
    increment_global()
    print(count)                        # -> 2

    c = make_counter()
    c()
    c()
    print(c())                          # -> 3   ('n' survives between calls: a closure)

    # You only need global/nonlocal to REBIND a name. Mutating an object
    # (e.g. list.append) works without them because the name isn't reassigned.
    items = []

    def add():
        items.append("x")               # no nonlocal needed
    add()
    print(items)                        # -> ['x']
    # Prefer returning values over global state - it is easier to test.


if __name__ == "__main__":
    args_and_kwargs()
    special_parameters()
    unpacking()
    legb()
    global_nonlocal()
