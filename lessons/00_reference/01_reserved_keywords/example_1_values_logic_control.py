"""Reserved keywords, part 1: values, logic and control flow.

Python has exactly 35 reserved keywords - words the language itself owns, so you
can never use them as variable names. This first file covers the value keywords
(True, False, None), the logic/test keywords (and, or, not, is, in) and the
control-flow keywords (if, elif, else, for, while, break, continue, pass, del).
Each section shows a tiny example, prints the result, and explains WHY Python
behaves that way.
"""

import keyword


# --- 0. How many keywords are there? ---
def show_keyword_list():
    # The keyword module knows the official list for the Python you are running.
    print(len(keyword.kwlist))            # -> 35
    print(keyword.iskeyword("for"))       # -> True
    print(keyword.iskeyword("print"))     # -> False  (print is a function, not a keyword)
    # Trying `for = 3` would be a SyntaxError, so we only show it in a comment.


# --- 1. Values: True / False / None ---
def demo_values():
    ok = False
    done = True
    print(ok, done)                       # -> False True

    # True and False are really the integers 1 and 0 in disguise.
    print(True + True)                    # -> 2

    # None means "no value". There is only ONE None object in the whole program,
    # so the correct test is identity (`is`), not equality (`==`).
    x = None
    if x is None:
        print("x has no value yet")       # -> x has no value yet

    # Functions that don't `return` anything give back None.
    def nothing():
        pass
    print(nothing())                      # -> None

    # "Falsy" values behave like False in an `if`: False, None, 0, '', [], {}, set()
    for value in [False, None, 0, "", [], {}, "hi", [0]]:
        print(repr(value), "->", bool(value))
    # -> False -> False, None -> False, 0 -> False, '' -> False, [] -> False,
    #    {} -> False, 'hi' -> True, [0] -> True (a list with one item is non-empty!)


# --- 2. Logic: and / or / not ---
def demo_logic():
    a, b = True, False
    if a and b:
        print("both true")
    else:
        print("not both true")            # -> not both true

    # `and` / `or` SHORT-CIRCUIT and return one of the operands (not always a bool).
    # `and` stops at the first falsy operand; `or` stops at the first truthy one.
    print(0 and 99)                       # -> 0     (0 is falsy, so `and` stops there)
    print(5 and 99)                       # -> 99    (5 is truthy, so it checks 99)
    name = "" or "default"
    print(name)                           # -> default  (classic "fallback value" idiom)

    # Short-circuiting means the right side may never run:
    def loud():
        print("  loud() was called")
        return True
    print(False and loud())               # -> False  (loud() never runs)

    items = []
    if not items:
        print("the list is empty")        # -> the list is empty
    print(not 0, not "text")              # -> True False


# --- 3. Tests: is / in ---
def demo_is_in():
    # `in` = membership test. Works on strings, lists, dicts (checks keys), sets...
    print("a" in "cat")                   # -> True
    print(3 in [1, 2, 3])                 # -> True
    print("key" in {"key": 1})            # -> True  (dicts check keys, not values)
    print("z" not in "cat")               # -> True

    # `is` = identity: are these the SAME object in memory? `==` = equal value.
    list1 = [1, 2]
    list2 = [1, 2]
    print(list1 == list2)                 # -> True   (same contents)
    print(list1 is list2)                 # -> False  (two different list objects)
    list3 = list1
    print(list1 is list3)                 # -> True   (two names, one object)
    # Rule of thumb: use `is` only for None (and True/False singletons).


# --- 4. Branching: if / elif / else ---
def describe(x):
    if x > 0:
        return "positive"
    elif x == 0:                          # elif = "else if": checked only if the
        return "zero"                     # previous conditions were all false
    else:
        return "negative"                 # fallback when nothing above matched


def demo_if():
    print(describe(5), describe(0), describe(-2))   # -> positive zero negative


# --- 5. Loops: for / while / break / continue / loop-else ---
def demo_loops():
    # `for` walks over ANY iterable: range, list, string, dict, file...
    for i in range(3):
        print("for:", i)                  # -> for: 0 / for: 1 / for: 2

    # `while` repeats as long as the condition is truthy.
    n = 3
    while n > 0:
        print("while:", n)                # -> while: 3 / while: 2 / while: 1
        n -= 1

    # `break` leaves the nearest loop immediately.
    for x in range(10):
        if x == 3:
            break
        print("before break:", x)         # -> 0, 1, 2

    # `continue` skips the rest of this iteration and moves to the next one.
    for x in range(6):
        if x % 2:                         # odd numbers have remainder 1 (truthy)
            continue
        print("even:", x)                 # -> 0, 2, 4

    # `else` on a loop runs only if the loop finished WITHOUT `break`.
    # Great for "search, and report if not found".
    for x in [1, 3, 5]:
        if x % 2 == 0:
            print("found an even number")
            break
    else:
        print("none")                     # -> none  (no break happened)


# --- 6. pass: the do-nothing placeholder ---
class Stub:
    pass                                  # a class body can't be empty; pass fills it


def todo():
    pass                                  # handy while sketching code


def demo_pass():
    print(Stub(), todo())                 # -> <__main__.Stub object at 0x...> None


# --- 7. del: remove a name, list item, slice or dict key ---
def demo_del():
    d = {"key": 1, "other": 2}
    del d["key"]
    print(d)                              # -> {'other': 2}

    nums = [0, 1, 2, 3, 4, 5]
    del nums[0]                           # remove one item
    print(nums)                           # -> [1, 2, 3, 4, 5]
    del nums[1:3]                         # remove a slice
    print(nums)                           # -> [1, 4, 5]

    temp = "bye"
    del temp                              # the NAME is gone (the object is freed if unused)
    try:
        print(temp)
    except NameError as e:
        print("NameError:", e)            # -> NameError: cannot access local variable 'temp'...


if __name__ == "__main__":
    print("--- 0. keyword list ---");  show_keyword_list()
    print("--- 1. values ---");        demo_values()
    print("--- 2. logic ---");         demo_logic()
    print("--- 3. is / in ---");       demo_is_in()
    print("--- 4. if/elif/else ---");  demo_if()
    print("--- 5. loops ---");         demo_loops()
    print("--- 6. pass ---");          demo_pass()
    print("--- 7. del ---");           demo_del()
