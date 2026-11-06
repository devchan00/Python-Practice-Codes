"""Lesson 1: Variables and core types.

A variable is a name that points at a value. Python has no declarations:
you write ``x = 10`` and the name ``x`` now refers to the integer 10. The
type belongs to the value, not to the name, so the same name can later
point at a string. This lesson covers the four core types (int, float,
str, bool), checking types with type() and isinstance(), converting
between types, unpacking and swapping, None, comments and docstrings, and
the naming conventions Python programmers expect.
"""

# Constants are written in UPPER_CASE. Python does not stop you from
# changing them; the name is a promise to other programmers.
MAX_SPEED = 120


# --- 1. Assigning variables ---
def assigning_variables():
    print("--- 1. Assigning variables ---")
    x = 10                      # no "int x" declaration needed
    print(x)                    # -> 10

    # The type is dynamic: the name can be re-pointed at any type.
    x = "ten"
    print(x)                    # -> ten

    # Assignment copies the *reference*, not the value. For numbers and
    # strings this never surprises you, because they cannot be changed.
    y = x
    print(y)                    # -> ten


# --- 2. The four core types ---
def core_types():
    print("\n--- 2. The four core types ---")
    age = 30            # int: whole number, any size
    price = 4.99        # float: number with a decimal point
    name = "Ana"        # str: text, in single or double quotes
    is_member = True    # bool: True or False (capitalised!)
    print(age, price, name, is_member)      # -> 30 4.99 Ana True

    # ints never overflow in Python; they just get bigger.
    print(2 ** 100)     # -> 1267650600228229401496703205376

    # floats are approximations, so tiny rounding errors appear.
    print(0.1 + 0.2)    # -> 0.30000000000000004


# --- 3. Inspecting types: type() and isinstance() ---
def inspecting_types():
    print("\n--- 3. Inspecting types ---")
    x = 10
    print(type(x))                  # -> <class 'int'>
    print(type("hi"))               # -> <class 'str'>
    print(isinstance(x, int))       # -> True

    # isinstance accepts subclasses too. bool is a subclass of int,
    # so True "is an" int, while type() reports the exact class only.
    print(isinstance(True, int))    # -> True
    print(type(True) == int)        # -> False  (exact type is bool)

    # isinstance can check several types at once with a tuple.
    print(isinstance(4.5, (int, float)))   # -> True


# --- 4. Converting (casting) between types ---
def converting_types():
    print("\n--- 4. Converting between types ---")
    print(int("5") + 1)       # -> 6     text "5" became the number 5
    print(str(5) + "1")       # -> 51    number 5 became the text "5"
    print(float("2.5") * 2)   # -> 5.0
    print(int(3.99))          # -> 3     int() cuts off, it does not round
    print(round(3.99))        # -> 4     use round() to round
    print(bool(0), bool(7))   # -> False True

    # Why convert? "5" + 1 is an error: Python refuses to guess whether
    # you meant text joining or number adding.
    try:
        "5" + 1
    except TypeError as e:
        print("TypeError:", e)  # -> TypeError: can only concatenate str (not "int") to str

    # A string that does not look like a number cannot become an int.
    try:
        int("five")
    except ValueError as e:
        print("ValueError:", e)  # -> ValueError: invalid literal for int() with base 10: 'five'


# --- 5. Unpacking and swapping ---
def unpacking():
    print("\n--- 5. Unpacking and swapping ---")
    a, b = 1, 2             # assign two names in one line
    print(a, b)             # -> 1 2

    # Swap without a temporary variable: the right side is built first
    # (as the pair (2, 1)), then unpacked into a and b.
    a, b = b, a
    print(a, b)             # -> 2 1

    # The number of names must match the number of values.
    try:
        a, b = 1, 2, 3
    except ValueError as e:
        print("ValueError:", e)  # -> ValueError: too many values to unpack (expected 2, got 3)


# --- 6. None: the value meaning "nothing" ---
def none_value():
    print("\n--- 6. None ---")
    result = None           # "no value yet"
    print(result)           # -> None
    print(type(result))     # -> <class 'NoneType'>

    # Compare with `is`, not `==`. There is only one None object, and
    # `is` asks "is this that exact object?", which cannot be fooled.
    print(result is None)       # -> True
    print(result is not None)   # -> False


# --- 7. Comments and docstrings ---
def area(width, height):
    '''Return the area of a rectangle.

    This triple-quoted string is a docstring. It documents the function
    and is available at runtime through area.__doc__ and help(area).
    '''
    return width * height  # a comment: ignored by Python, read by humans


def comments_and_docstrings():
    print("\n--- 7. Comments and docstrings ---")
    print(area(3, 4))                       # -> 12
    print(area.__doc__.splitlines()[0])     # -> Return the area of a rectangle.


# --- 8. Naming conventions ---
class ShoppingCart:             # PascalCase for classes
    pass


def naming_conventions():
    print("\n--- 8. Naming conventions ---")
    item_count = 3              # snake_case for variables and functions
    cart = ShoppingCart()
    print(item_count, type(cart).__name__, MAX_SPEED)  # -> 3 ShoppingCart 120
    # Names are case-sensitive: item_count and Item_Count are different.
    # Names cannot start with a digit or be a keyword like `class`.


if __name__ == "__main__":
    assigning_variables()
    core_types()
    inspecting_types()
    converting_types()
    unpacking()
    none_value()
    comments_and_docstrings()
    naming_conventions()
