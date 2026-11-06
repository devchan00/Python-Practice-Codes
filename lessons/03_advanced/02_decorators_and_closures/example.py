"""Lesson 3.2 - Decorators & closures.

A *closure* is an inner function that remembers variables from the function
that created it, even after that outer function has returned. A *decorator*
is a function that takes a function and returns a new (usually wrapping)
function; ``@timer`` above ``def f`` is just shorthand for ``f = timer(f)``.
Together they let you add behaviour such as timing, logging, retries or
caching without editing the original function body.
"""

import functools
import time


# --- 1. Functions are objects ----------------------------------------------
def demo_functions_are_objects():
    print("--- 1. Functions are objects ---")

    def shout(text):
        return text.upper() + "!"

    yell = shout                  # no call: we copy a reference to the function
    print(yell("hi"))             # -> HI!
    print([f("ok") for f in (str.upper, shout)])   # -> ['OK', 'OK!']


# --- 2. Closures ------------------------------------------------------------
def make_multiplier(factor):
    def multiply(x):
        return x * factor          # `factor` is captured from the outer scope
    return multiply


def make_counter():
    count = 0

    def increment():
        nonlocal count             # needed to *rebind* an outer variable
        count += 1
        return count
    return increment


def demo_closures():
    print("\n--- 2. Closures ---")
    double, triple = make_multiplier(2), make_multiplier(3)
    print(double(5), triple(5))    # -> 10 15
    # The captured value lives in a "cell" attached to the function:
    print(double.__closure__[0].cell_contents)   # -> 2

    counter = make_counter()
    counter(); counter()
    print(counter())               # -> 3  (state survives between calls)


# --- 3. The timer decorator -------------------------------------------------
def timer(func):
    @functools.wraps(func)         # copy __name__, __doc__ etc. onto wrapper
    def wrapper(*args, **kwargs):  # *args/**kwargs: works for any signature
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result              # don't forget to pass the result through!
    return wrapper


@timer                              # same as: slow_add = timer(slow_add)
def slow_add(a, b):
    """Add two numbers slowly."""
    time.sleep(0.05)
    return a + b


def demo_timer():
    print("\n--- 3. The timer decorator ---")
    print(slow_add(2, 3))          # -> slow_add took 0.05xxs  then  5


# --- 4. Why functools.wraps matters -----------------------------------------
def no_wraps(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@no_wraps
def documented():
    """I have a docstring."""


def demo_wraps():
    print("\n--- 4. functools.wraps ---")
    print(documented.__name__, documented.__doc__)   # -> wrapper None  (lost!)
    print(slow_add.__name__, "|", slow_add.__doc__)  # -> slow_add | Add two numbers slowly.
    print(slow_add.__wrapped__(1, 1))                # -> 2 (original, untimed)


# --- 5. Decorator WITH arguments: @repeat(3) --------------------------------
def repeat(times):
    """A decorator *factory*: repeat(3) returns the real decorator.
    Three layers: factory(args) -> decorator(func) -> wrapper(*args)."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


@repeat(3)                          # repeat(3) runs first, then decorates greet
def greet(name):
    print(f"hello {name}")


def demo_repeat():
    print("\n--- 5. Decorator with arguments ---")
    greet("Ada")                   # -> hello Ada (printed 3 times)


# --- 6. Stacking decorators & a stateful decorator --------------------------
def count_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1         # store state as an attribute on the wrapper
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


@count_calls                        # applied second (outermost)
@repeat(2)                          # applied first (closest to the function)
def ping():
    print("ping")


def demo_stacking():
    print("\n--- 6. Stacking decorators ---")
    ping()                         # -> ping / ping
    ping()                         # -> ping / ping
    print("ping.calls =", ping.calls)   # -> ping.calls = 2 (outer wrapper counted)


# --- 7. Late-binding closure gotcha (and fixes) -----------------------------
def demo_late_binding():
    print("\n--- 7. Late-binding gotcha ---")
    # Closures look up `i` when they are CALLED, not when they are created.
    # By then the loop has finished, so every lambda sees the last i.
    funcs = [lambda: i for i in range(3)]
    print([f() for f in funcs])    # -> [2, 2, 2]   (surprise!)

    # Fix 1: bind the current value as a default argument (evaluated at def time)
    funcs = [lambda i=i: i for i in range(3)]
    print([f() for f in funcs])    # -> [0, 1, 2]

    # Fix 2: functools.partial freezes the argument right now
    funcs = [functools.partial(lambda x: x, i) for i in range(3)]
    print([f() for f in funcs])    # -> [0, 1, 2]


if __name__ == "__main__":
    demo_functions_are_objects()
    demo_closures()
    demo_timer()
    demo_wraps()
    demo_repeat()
    demo_stacking()
    demo_late_binding()
