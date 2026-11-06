"""Lesson 7: Input/output, loop helpers and errors.

Programs talk to people through print() (output) and input() (input).
print() takes `sep` (what goes BETWEEN values) and `end` (what goes AFTER).
input() always returns a string, so you convert it yourself. For looping,
range() produces number sequences, enumerate() gives you index + item
pairs, and dict.items() gives key + value pairs. When something goes wrong
Python raises an exception; try / except / else / finally lets you handle
it instead of crashing. The lesson finishes with the common built-in
exceptions you will meet first.

This file runs without asking for input: wherever a real program would call
input(), we use a hard-coded string and show the real call in a comment.
"""


# --- 1. print with sep and end ---
def printing():
    print("--- 1. print(sep=, end=) ---")
    a, b = "apples", "pears"
    print(a, b)                     # -> apples pears        default sep is a space
    print(a, b, sep=", ")           # -> apples, pears
    print("2024", "01", "15", sep="-")   # -> 2024-01-15
    print(a, b, sep=", ", end="")   # end="" means no newline afterwards...
    print(" <- same line")          # -> apples, pears <- same line
    for i in range(3):
        print(i, end=" ")           # -> 0 1 2
    print()                         # an empty print() just ends the line


# --- 2. input always returns a string ---
def reading_input():
    print("\n--- 2. input() ---")
    # Real code:  age_text = input('Age? ')
    age_text = "42"                 # pretend this came from input('Age? ')
    print(type(age_text))           # -> <class 'str'>
    print(age_text + age_text)      # -> 4242   string joining, not maths!
    age = int(age_text)             # convert explicitly
    print(age + age)                # -> 84

    # Clean up text input before using it.
    # Real code:  answer = input('Continue? (y/n) ')
    answer = "  Y \n"               # pretend the user typed " Y " and Enter
    print(answer.strip().lower() == "y")   # -> True


# --- 3. range ---
def ranges():
    print("\n--- 3. range ---")
    print(list(range(5)))           # -> [0, 1, 2, 3, 4]   stop is excluded
    print(list(range(2, 10, 2)))    # -> [2, 4, 6, 8]      start, stop, step
    print(list(range(5, 0, -1)))    # -> [5, 4, 3, 2, 1]   counting down
    # range is lazy: range(1_000_000) does not build a million-item list.
    print(len(range(1_000_000)))    # -> 1000000


# --- 4. enumerate ---
def enumerating():
    print("\n--- 4. enumerate ---")
    lst = ["eggs", "milk", "bread"]
    # Instead of tracking a counter yourself, enumerate gives (index, item).
    for number, item in enumerate(lst, 1):     # start counting at 1
        print(f"{number}. {item}")             # -> 1. eggs / 2. milk / 3. bread
    print(list(enumerate(lst)))   # -> [(0, 'eggs'), (1, 'milk'), (2, 'bread')]


# --- 5. Looping over dict pairs ---
def dict_loops():
    print("\n--- 5. for k, v in d.items() ---")
    d = {"Ana": 91, "Bo": 78}
    for k, v in d.items():
        print(f"{k} scored {v}")    # -> Ana scored 91 / Bo scored 78
    for k in d:                     # looping a dict directly gives KEYS
        print(k, end=" ")           # -> Ana Bo
    print()


# --- 6. try / except / else / finally ---
def parse_number(text):
    """Demonstrate every part of a try statement with one input."""
    try:
        # Real code:  n = int(input("n: "))
        n = int(text)
    except ValueError as e:
        print("Not a number:", e)   # runs only if int() failed
    else:
        print("ok, n =", n)         # runs only if NO exception happened
    finally:
        print("done")               # ALWAYS runs: good for clean-up


def try_except():
    print("\n--- 6. try / except / else / finally ---")
    parse_number("12")      # -> ok, n = 12 / done
    parse_number("abc")     # -> Not a number: invalid literal for int() with base 10: 'abc' / done

    # A realistic "keep asking until valid" loop, fed by fake answers.
    fake_answers = ["ten", "", "10"]   # pretend each came from input("n: ")
    for attempt in fake_answers:
        try:
            n = int(attempt)
            break                       # valid: stop asking
        except ValueError:
            print(f"{attempt!r} is not a whole number, try again")
    print("accepted:", n)               # -> accepted: 10


# --- 7. Common exceptions ---
def common_exceptions():
    print("\n--- 7. Common exceptions ---")
    # Each lambda triggers one kind of error, which we catch and name.
    examples = [
        ("ValueError", lambda: int("x")),              # right type, bad value
        ("TypeError", lambda: "a" + 1),                # wrong type for operation
        ("KeyError", lambda: {"a": 1}["b"]),           # missing dict key
        ("IndexError", lambda: [1, 2][5]),             # list index out of range
        ("AttributeError", lambda: (5).upper()),       # int has no .upper()
        ("ZeroDivisionError", lambda: 1 / 0),
        ("FileNotFoundError", lambda: open("no_such_file_123.txt")),
        ("ImportError", lambda: __import__("no_such_module_123")),
    ]
    for _label, action in examples:     # _label is just for readers
        try:
            action()
        except Exception as e:      # catch-all, only for this demo
            print(f"{type(e).__name__:<20} {e}")
    # Output (one per line):
    # -> ValueError           invalid literal for int() with base 10: 'x'
    # -> TypeError            can only concatenate str (not "int") to str
    # -> KeyError             'b'
    # -> IndexError           list index out of range
    # -> AttributeError       'int' object has no attribute 'upper'
    # -> ZeroDivisionError    division by zero
    # -> FileNotFoundError    [Errno 2] No such file or directory: 'no_such_file_123.txt'
    # -> ModuleNotFoundError  No module named 'no_such_module_123'
    #    (ModuleNotFoundError is a subclass of ImportError)

    # Catch several specific types with a tuple. Prefer specific
    # exceptions over a bare `except:`, which would hide real bugs.
    try:
        [1, 2][5]
    except (IndexError, KeyError) as e:
        print("lookup failed:", e)   # -> lookup failed: list index out of range


if __name__ == "__main__":
    printing()
    reading_input()
    ranges()
    enumerating()
    dict_loops()
    try_except()
    common_exceptions()
