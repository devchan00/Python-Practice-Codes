"""Lesson 4: Control flow.

Control flow decides WHICH lines run and HOW MANY times. `if / elif / else`
picks one branch; `for` repeats once per item in a sequence; `while` repeats
as long as a condition stays true; `break` leaves a loop early and
`continue` skips to the next round. The conditional (ternary) expression
`a if cond else b` chooses a value in a single line. Python marks blocks
with indentation (4 spaces), not braces, so indentation is part of the
syntax.
"""


# --- 1. if / elif / else ---
def describe(x):
    # Python checks the conditions top to bottom and runs ONLY the first
    # branch whose condition is true. else catches everything left over.
    if x > 0:
        return "positive"
    elif x == 0:
        return "zero"
    else:
        return "negative"


def if_elif_else():
    print("--- 1. if / elif / else ---")
    for x in (5, 0, -3):
        print(x, "is", describe(x))   # -> 5 is positive / 0 is zero / -3 is negative

    # Order matters: the first true branch wins, so put specific tests first.
    score = 95
    if score >= 90:
        grade = "A"
    elif score >= 80:       # not reached for 95, even though it is also true
        grade = "B"
    else:
        grade = "C"
    print("grade:", grade)  # -> grade: A


# --- 2. for loops and range ---
def for_loops():
    print("\n--- 2. for loops ---")
    for i in range(3):          # range(3) gives 0, 1, 2 (stops BEFORE 3)
        print(i)                # -> 0 / 1 / 2

    # for works on any sequence: strings, lists, tuples, dicts, ...
    for letter in "hi!":
        print(letter, end=" ")  # -> h i !
    print()

    total = 0
    for price in [2.5, 4.0, 1.5]:
        total += price
    print("total:", total)      # -> total: 8.0


# --- 3. while loops, break and continue ---
def while_loops():
    print("\n--- 3. while, break, continue ---")
    # while repeats as long as the condition is true. Something inside the
    # loop MUST change the condition, or it runs forever.
    countdown = 3
    while countdown > 0:
        print("countdown", countdown)   # -> countdown 3 / 2 / 1
        countdown -= 1

    # The cheatsheet example, traced: n goes 9, 8, 7, 6, 5...
    n = 10
    while n > 0:
        n -= 1
        if n == 5:
            break           # leave the loop completely
        if n % 2:
            continue        # odd n: skip the print, go to the next round
        print("even n:", n)  # -> even n: 8 / even n: 6
    print("loop ended with n =", n)   # -> loop ended with n = 5


# --- 4. Loop else (runs only if no break happened) ---
def loop_else():
    print("\n--- 4. for ... else ---")
    # A less known feature: else on a loop runs when the loop finished
    # normally, i.e. WITHOUT hitting break. Useful for "search" loops.
    for n in [3, 7, 11]:
        if n % 2 == 0:
            print("found an even number:", n)
            break
    else:
        print("no even number found")   # -> no even number found


# --- 5. Conditional (ternary) expression ---
def ternary():
    print("\n--- 5. Ternary expression ---")
    ok = True
    label = "yes" if ok else "no"       # value_if_true if condition else value_if_false
    print(label)                        # -> yes

    age = 15
    print("adult" if age >= 18 else "minor")   # -> minor
    # Use it for choosing a VALUE. For running different statements,
    # a normal if/else block is clearer.


# --- 6. Nested blocks and indentation ---
def nesting():
    print("\n--- 6. Nesting ---")
    # Indentation shows which lines belong to which block.
    for row in range(1, 4):
        line = ""
        for col in range(1, 4):
            line += f"{row * col:3}"
        print(line)
    # ->   1  2  3
    # ->   2  4  6
    # ->   3  6  9

    # `pass` is a placeholder for an empty block (Python needs SOMETHING).
    if True:
        pass


if __name__ == "__main__":
    if_elif_else()
    for_loops()
    while_loops()
    loop_else()
    ternary()
    nesting()
