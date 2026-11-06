"""Lesson 2: Operators.

Operators are the symbols that combine values: arithmetic (+ - * / // % **),
comparisons (== != < > <= >=, which can be chained), boolean logic (and, or,
not, which short-circuit), membership (in, not in), identity (is, is not),
augmented assignment (+= -= *= //=), the walrus operator (:=) that assigns
inside an expression, and the bitwise operators (& | ^ ~ << >>). The lesson
ends with truthiness: which values Python treats as False in an `if`.
"""


# --- 1. Arithmetic ---
def arithmetic():
    print("--- 1. Arithmetic ---")
    print(7 + 2)     # -> 9    add
    print(7 - 2)     # -> 5    subtract
    print(7 * 2)     # -> 14   multiply
    print(7 / 2)     # -> 3.5  true division ALWAYS gives a float
    print(6 / 2)     # -> 3.0  ...even when it divides evenly
    print(7 // 2)    # -> 3    floor division: rounds DOWN to a whole number
    print(-7 // 2)   # -> -4   "down" means toward minus infinity, not toward 0
    print(7 % 2)     # -> 1    modulo: the remainder after //
    print(7 ** 2)    # -> 49   power

    # % is handy for "is it even?" and for wrapping around (clock maths).
    print(10 % 2 == 0)   # -> True   10 is even
    print((22 + 5) % 24)  # -> 3     5 hours after 22:00 is 03:00

    # Precedence: ** before * / // % before + -. Use brackets to be clear.
    print(2 + 3 * 4)     # -> 14
    print((2 + 3) * 4)   # -> 20


# --- 2. Comparisons ---
def comparisons():
    print("\n--- 2. Comparisons ---")
    x = 5
    print(x == 5, x != 5)    # -> True False   (== compares, = assigns)
    print(x < 10, x > 10)    # -> True False
    print(x <= 5, x >= 6)    # -> True False

    # Chaining reads like maths: 0 < x < 10 means (0 < x) and (x < 10).
    print(0 < x < 10)        # -> True
    print(0 < x < 3)         # -> False

    # Strings compare alphabetically (by character code).
    print("apple" < "banana")  # -> True
    print("Zebra" < "apple")   # -> True  (uppercase letters sort first)


# --- 3. Boolean logic: and, or, not ---
def boolean_logic():
    print("\n--- 3. Boolean logic ---")
    age, has_ticket = 20, True
    print(age >= 18 and has_ticket)   # -> True   both must be true
    print(age < 18 or has_ticket)     # -> True   at least one is true
    print(not has_ticket)             # -> False  flips the value

    # Short-circuit: Python stops as soon as the answer is known. Here the
    # division never runs, because `False and ...` must already be False.
    divisor = 0
    print(divisor != 0 and 10 / divisor > 1)   # -> False (no ZeroDivisionError!)

    # `or` returns the first truthy value, which gives an easy default.
    name = ""
    print(name or "Anonymous")        # -> Anonymous


# --- 4. Membership: in, not in ---
def membership():
    print("\n--- 4. Membership ---")
    print("a" in "cat")               # -> True   substring check
    print("dog" not in "cat")         # -> True
    print(3 in [1, 2, 3])             # -> True   item in a list
    print("key" in {"key": 1})        # -> True   checks dict KEYS, not values


# --- 5. Identity: is, is not ---
def identity():
    print("\n--- 5. Identity ---")
    a = [1, 2]
    b = [1, 2]
    c = a
    print(a == b)        # -> True   same contents
    print(a is b)        # -> False  two different list objects
    print(a is c)        # -> True   c is another name for the same object

    # Use `is` for None (and True/False singletons), == for everything else.
    value = None
    print(value is None)  # -> True


# --- 6. Augmented assignment ---
def augmented_assignment():
    print("\n--- 6. Augmented assignment ---")
    score = 10
    score += 5       # same as score = score + 5
    print(score)     # -> 15
    score -= 3
    print(score)     # -> 12
    score *= 2
    print(score)     # -> 24
    score //= 5
    print(score)     # -> 4
    # Also exist: /=, %=, **=, and the bitwise ones like |=.


# --- 7. The walrus operator := ---
def walrus():
    print("\n--- 7. Walrus := ---")
    a = [10, 20, 30, 40]
    # Without walrus you would compute len(a) twice, or use an extra line.
    # := assigns AND gives back the value, so it works inside an `if`.
    if (n := len(a)) > 3:
        print(f"List is long ({n} items)")   # -> List is long (4 items)

    # Classic use: loop while reading values, keeping the value you tested.
    numbers = [3, 8, 1, 0, 5]
    i = 0
    while (value := numbers[i]) != 0:        # stop at the 0 "sentinel"
        print("got", value)                  # -> got 3 / got 8 / got 1
        i += 1
    # The brackets matter: n := len(a) > 3 would store the bool True in n.


# --- 8. Bitwise operators ---
def bitwise():
    print("\n--- 8. Bitwise ---")
    # These work on the binary digits (bits) of integers.
    a, b = 0b1100, 0b1010          # 12 and 10
    print(bin(a & b), a & b)       # -> 0b1000 8     AND: bit set in both
    print(bin(a | b), a | b)       # -> 0b1110 14    OR: bit set in either
    print(bin(a ^ b), a ^ b)       # -> 0b110 6      XOR: set in exactly one
    print(~a)                      # -> -13          NOT: equals -(a + 1)
    print(1 << 3)                  # -> 8            shift left = multiply by 2**3
    print(32 >> 2)                 # -> 8            shift right = floor-divide by 2**2

    # Practical example: flags packed into one number.
    READ, WRITE, EXECUTE = 1, 2, 4
    perms = READ | WRITE           # turn on two flags
    print(bool(perms & WRITE))     # -> True   is WRITE on?
    print(bool(perms & EXECUTE))   # -> False


# --- 9. Truthy and falsy values ---
def truthiness():
    print("\n--- 9. Truthy and falsy ---")
    # These values count as False in an `if` or `while`:
    falsy = [0, 0.0, "", [], {}, set(), None, False]
    for value in falsy:
        print(repr(value), "->", bool(value))   # -> each line ends in False

    # Everything else is truthy, including some surprises:
    print(bool("False"))    # -> True  a non-empty string, whatever it says
    print(bool([0]))        # -> True  a list with one item is not empty
    print(bool(-1))         # -> True  any non-zero number

    # This is why `if items:` is the idiomatic "is the list non-empty?"
    items = []
    if not items:
        print("No items yet")   # -> No items yet


if __name__ == "__main__":
    arithmetic()
    comparisons()
    boolean_logic()
    membership()
    identity()
    augmented_assignment()
    walrus()
    bitwise()
    truthiness()
