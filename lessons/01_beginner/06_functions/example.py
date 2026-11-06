"""Lesson 6: Functions.

A function is a named, reusable block of code. You define it once with
`def`, give it parameters (inputs), and `return` a result (output).
Functions let you avoid repeating yourself and break a big problem into
small, testable pieces. This lesson covers defining and calling functions,
docstrings, default values, positional vs keyword arguments, what happens
when there is no return, returning several values, local variables, and
the classic mutable-default-argument trap.
"""


# --- 1. Defining and calling a function ---
def greet(name, greeting="Hello"):
    """Return a greeting string."""
    return f"{greeting}, {name}!"


def defining_and_calling():
    print("--- 1. def and call ---")
    print(greet("Ana"))                       # -> Hello, Ana!   positional
    print(greet("Bo", "Hi"))                  # -> Hi, Bo!       both positional
    print(greet(greeting="Hi", name="Bo"))    # -> Hi, Bo!       keyword arguments
    # Keyword arguments can come in any order and make calls self-explaining.
    # The docstring documents the function:
    print(greet.__doc__)                      # -> Return a greeting string.


# --- 2. Default values ---
def power(base, exponent=2):
    """Raise base to exponent (squares by default)."""
    return base ** exponent


def default_values():
    print("\n--- 2. Default values ---")
    print(power(5))        # -> 25    exponent defaulted to 2
    print(power(2, 10))    # -> 1024
    # Rule: parameters with defaults must come AFTER those without.
    # def bad(a=1, b): ...  would be a SyntaxError.


# --- 3. No return means None ---
def say_hi(name):
    print(f"hi {name}")      # prints, but returns nothing explicitly


def no_return():
    print("\n--- 3. No return -> None ---")
    result = say_hi("Cy")    # -> hi Cy
    print(result)            # -> None
    # Printing is not returning! Use return when the caller needs the value.


# --- 4. return ends the function early; returning several values ---
def classify(n):
    if n < 0:
        return "negative"    # function stops here for negatives
    return "non-negative"


def min_max(numbers):
    """Return the smallest and largest number as a tuple."""
    return min(numbers), max(numbers)


def returning_values():
    print("\n--- 4. Return values ---")
    print(classify(-1), classify(3))   # -> negative non-negative
    low, high = min_max([4, 9, 1, 7])  # the tuple is unpacked
    print(low, high)                   # -> 1 9


# --- 5. Local variables (scope) ---
counter = 0      # a global variable


def local_scope():
    print("\n--- 5. Local scope ---")
    counter = 99   # this is a NEW local variable, not the global one
    print("inside:", counter)   # -> inside: 99


def show_global():
    print("global:", counter)   # -> global: 0   (unchanged)


# --- 6. Functions are values ---
def apply_twice(func, value):
    return func(func(value))


def functions_are_values():
    print("\n--- 6. Functions as values ---")
    print(apply_twice(power, 3))   # -> 81    power(power(3)) = (3**2)**2
    f = greet                      # no brackets: refer to the function itself
    print(f("Dee"))                # -> Hello, Dee!


# --- 7. WARNING: the mutable default argument trap ---
# Default values are evaluated ONCE, when `def` runs, not on every call.
# A list default is therefore one shared list that keeps growing.
def add_item_buggy(item, basket=[]):
    basket.append(item)
    return basket


# The fix: use None as the default and create a fresh list inside.
def add_item_fixed(item, basket=None):
    if basket is None:
        basket = []          # a brand new list on every call
    basket.append(item)
    return basket


def mutable_default_trap():
    print("\n--- 7. Mutable default trap ---")
    print(add_item_buggy("apple"))    # -> ['apple']
    print(add_item_buggy("pear"))     # -> ['apple', 'pear']   surprise!
    print(add_item_fixed("apple"))    # -> ['apple']
    print(add_item_fixed("pear"))     # -> ['pear']            correct
    # The same applies to {} and set() defaults. Never use them.


if __name__ == "__main__":
    defining_and_calling()
    default_values()
    no_return()
    returning_values()
    local_scope()
    show_global()
    functions_are_values()
    mutable_default_trap()
