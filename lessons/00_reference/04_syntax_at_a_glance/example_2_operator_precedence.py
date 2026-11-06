"""Syntax at a glance, part 2: operator precedence (highest to lowest).

When an expression mixes operators, precedence decides which part is evaluated
first - just like "multiply before add" in maths. This file demonstrates every
row of the cheatsheet's precedence table, from grouping (...) at the top down to
the walrus operator := at the bottom, and shows why adding parentheses is often
the clearest choice.
"""


# --- 1. (...) grouping: highest ---
def demo_grouping():
    print(2 + 3 * 4)                      # -> 14   * before +
    print((2 + 3) * 4)                    # -> 20   parentheses win over everything


# --- 2. x[i]  x.attr  f(): subscript, attribute, call ---
def demo_primary():
    words = ["hi", "there"]
    print(words[1].upper())               # -> THERE  index, then attribute, then call
    print(-words.__len__())               # -> -2     the call happens before unary minus
    print(len(words) ** 2)                # -> 4      the call happens before **


# --- 3. ** power ---
def demo_power():
    print(2 ** 3 ** 2)                    # -> 512   ** is RIGHT-associative: 2 ** (3 ** 2)
    print(-2 ** 2)                        # -> -4    ** binds tighter than unary minus: -(2 ** 2)
    print((-2) ** 2)                      # -> 4
    print(2 ** -1)                        # -> 0.5   but unary on the RIGHT of ** is fine


# --- 4. +x  -x  ~x: unary ---
def demo_unary():
    x = 5
    print(+x, -x, ~x)                     # -> 5 -5 -6   ~x == -(x + 1) (bitwise NOT)
    print(-x * 2)                         # -> -10  unary applies before *


# --- 5. *  /  //  %  @: multiply-like ---
class Vec2:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __matmul__(self, other):          # @ is matrix multiplication; here a dot product
        return self.x * other.x + self.y * other.y


def demo_multiply_like():
    print(7 / 2, 7 // 2, 7 % 2)           # -> 3.5 3 1   true div, floor div, remainder
    print(-7 // 2)                        # -> -4        floor division rounds DOWN
    print(2 * 9 % 4)                      # -> 2         same level -> left to right: (2*9)%4
    print(Vec2(1, 2) @ Vec2(3, 4))        # -> 11        @ (used by NumPy for matrices)


# --- 6. +  -: add, subtract ---
def demo_add_sub():
    print(10 - 4 - 3)                     # -> 3     left to right: (10-4)-3
    print(1 + 2 * 3 - 4 / 2)              # -> 5.0   1 + 6 - 2.0


# --- 7. <<  >>: bit shifts ---
def demo_shifts():
    print(1 << 4, 256 >> 2)               # -> 16 64   shift left = *2 per step
    print(1 << 2 + 1)                     # -> 8       + happens first: 1 << 3


# --- 8. &  ^  |: bitwise AND, XOR, OR (in that order) ---
def demo_bitwise():
    print(0b1100 & 0b1010)                # -> 8   (0b1000) bits set in both
    print(0b1100 ^ 0b1010)                # -> 6   (0b0110) bits set in exactly one
    print(0b1100 | 0b1010)                # -> 14  (0b1110) bits set in either
    print(1 | 2 & 3)                      # -> 3   & before |: 1 | (2 & 3) = 1 | 2
    print(4 & 1 << 2)                     # -> 4   shift before &: 4 & 4
    # In Python, & is HIGHER than ==, so 5 & 1 == 1 means (5 & 1) == 1.
    # (C and JavaScript do the opposite!) Brackets make it obvious either way.
    print(5 & 1 == 1)                     # -> True   same as (5 & 1) == 1
    print((5 & 1) == 1)                   # -> True   clearer
    # The real trap is mixing bitwise and boolean ideas: `1 | 2 == 3` is
    # 1 | 2 == 3 -> (1 | 2) == 3 -> True, but `x == 1 | 2` is x == 3, not "1 or 2"!
    x = 1
    print(x == 1 | 2)                     # -> False  (compares x with 3)


# --- 9. ==  !=  <  >  in  is: comparison, membership, identity ---
def demo_comparisons():
    print(1 + 1 == 2)                     # -> True   arithmetic first, then compare
    print(1 < 5 < 10)                     # -> True   chaining: 1 < 5 and 5 < 10
    print(3 in [1, 2] + [3])              # -> True   + before in
    x = None
    print(x is None != False)             # -> True   chained: (x is None) and (None != False)


# --- 10. not: boolean NOT ---
def demo_not():
    print(not 1 == 2)                     # -> True   comparison first: not (1 == 2)
    print(not 0 + 1)                      # -> False  not (0 + 1) -> not 1


# --- 11. and: boolean AND ---
def demo_and():
    print(not True and False)             # -> False  (not True) and False
    print(True or True and False)         # -> True   and before or: True or (True and False)


# --- 12. or: boolean OR ---
def demo_or():
    print(False or not False)             # -> True
    print(0 or 0 and 1 or 5)              # -> 5      0 or (0 and 1) or 5 -> 0 or 0 or 5


# --- 13. x if c else y: ternary (conditional expression) ---
def demo_ternary():
    n = 7
    print("odd" if n % 2 else "even")     # -> odd
    print(1 + 2 if False else 10)         # -> 10     the whole `1 + 2` is the "true" value
    print(1 + (2 if False else 10))       # -> 11     brackets change the meaning


# --- 14. := walrus: assignment expression (lowest) ---
def demo_walrus():
    data = [3, 8, 1, 9]
    if (n := len(data)) > 3:              # assign AND test in one go
        print(f"list is long ({n} items)")    # -> list is long (4 items)
    # Brackets matter: without them, n would get the BOOL result of the comparison.
    if (m := len(data) > 3):
        print(m)                          # -> True  (m = (len(data) > 3))
    print([y for x in data if (y := x * 10) > 50])   # -> [80, 90]


if __name__ == "__main__":
    for i, demo in enumerate([demo_grouping, demo_primary, demo_power, demo_unary,
                              demo_multiply_like, demo_add_sub, demo_shifts,
                              demo_bitwise, demo_comparisons, demo_not, demo_and,
                              demo_or, demo_ternary, demo_walrus], start=1):
        print(f"--- {i}. {demo.__name__.removeprefix('demo_')} ---")
        demo()
