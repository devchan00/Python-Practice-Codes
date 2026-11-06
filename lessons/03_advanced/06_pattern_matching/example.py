"""Lesson 3.6 - Structural pattern matching (match / case).

``match`` compares a value against a series of *patterns* and runs the first
``case`` that fits. Unlike a C-style switch, patterns can check the SHAPE of
data (sequences, mappings, class instances) and pull pieces out into
variables at the same time. Patterns can be combined with ``|`` (OR), narrowed
with ``if`` guards, captured whole with ``as``, and ``_`` is the wildcard that
matches anything.
"""

from dataclasses import dataclass


# --- 1. Literal patterns and the wildcard _ --------------------------------
def http_status(code):
    match code:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 401 | 403:                # --- OR pattern: either value
            return "Not allowed"
        case _:                        # wildcard: matches anything, binds nothing
            return "Something else"


def demo_literals():
    print("--- 1. Literals, OR, wildcard ---")
    for code in (200, 403, 404, 500):
        print(code, http_status(code))
    # -> 200 OK / 403 Not allowed / 404 Not Found / 500 Something else


# --- 2. Sequence patterns ---------------------------------------------------
def describe_command(words):
    match words:
        case []:
            return "empty"
        case ["quit" | "exit"]:            # OR inside a sequence
            return "bye"
        case ["go", direction]:            # exactly 2 items; capture the 2nd
            return f"going {direction}"
        case ["drop", *items]:             # *rest captures the remainder
            return f"dropping {items}"
        case [first, *_, last]:            # 2+ items: first and last
            return f"from {first} to {last}"
        case _:
            return "unknown"


def demo_sequences():
    print("\n--- 2. Sequence patterns ---")
    for cmd in ([], ["exit"], ["go", "north"], ["drop", "key", "map"], ["a", "b", "c"], ["solo"]):
        print(cmd, "->", describe_command(cmd))
    # -> [] -> empty / ['exit'] -> bye / ['go', 'north'] -> going north
    # -> ['drop', 'key', 'map'] -> dropping ['key', 'map']
    # -> ['a', 'b', 'c'] -> from a to c / ['solo'] -> unknown
    # NB: strings are NOT matched as sequences: case [x] never matches "a".
    print(describe_command("go"))    # -> unknown


# --- 3. Mapping patterns ----------------------------------------------------
def handle_event(event):
    match event:
        case {"type": "click", "pos": (x, y)}:    # nested tuple pattern
            return f"click at {x},{y}"
        case {"type": "key", "key": str(k)}:      # str(k): type check + capture
            return f"key {k!r}"
        case {"type": "scroll", **rest}:          # **rest: the other keys
            return f"scroll with {rest}"
        case {"type": t}:
            return f"unhandled event {t}"
        case _:
            return "not an event"


def demo_mappings():
    print("\n--- 3. Mapping patterns ---")
    print(handle_event({"type": "click", "pos": (3, 4), "button": 1}))  # -> click at 3,4 (extra keys ignored)
    print(handle_event({"type": "key", "key": "q"}))        # -> key 'q'
    print(handle_event({"type": "scroll", "dy": -2}))       # -> scroll with {'dy': -2}
    print(handle_event({"type": "resize"}))                 # -> unhandled event resize
    print(handle_event(42))                                 # -> not an event


# --- 4. Class patterns ------------------------------------------------------
@dataclass
class Point:
    x: int
    y: int


@dataclass
class Circle:
    center: Point
    radius: int


def where(shape):
    match shape:
        case Point(x=0, y=0):                  # keyword attribute patterns
            return "origin"
        case Point(0, y):                      # positional (dataclasses set __match_args__)
            return f"on the y-axis at {y}"
        case Point(x, y):
            return f"point {x},{y}"
        case Circle(center=Point(x=0, y=0), radius=r):   # nested class patterns
            return f"circle of radius {r} at origin"
        case Circle():
            return "some other circle"
        case int() | float():                  # type check only
            return "a number, not a shape"
        case _:
            return "unknown"


def demo_classes():
    print("\n--- 4. Class patterns ---")
    print(where(Point(0, 0)))                  # -> origin
    print(where(Point(0, 5)))                  # -> on the y-axis at 5
    print(where(Point(2, 3)))                  # -> point 2,3
    print(where(Circle(Point(0, 0), 4)))       # -> circle of radius 4 at origin
    print(where(Circle(Point(1, 1), 4)))       # -> some other circle
    print(where(3.5))                          # -> a number, not a shape


# --- 5. Guards (if) ---------------------------------------------------------
def classify(n):
    match n:
        case int(x) if x < 0:          # pattern matches, THEN guard is tested
            return "negative"
        case 0:
            return "zero"
        case int(x) if x % 2 == 0:
            return "positive even"
        case int():
            return "positive odd"
        case _:
            return "not an int"


def demo_guards():
    print("\n--- 5. Guards ---")
    print([classify(n) for n in (-3, 0, 4, 7, "x")])
    # -> ['negative', 'zero', 'positive even', 'positive odd', 'not an int']


# --- 6. Capturing with `as` -------------------------------------------------
def parse(token):
    match token:
        case ("+" | "-" | "*" | "/") as op:          # capture which alternative matched
            return f"operator {op}"
        case [Point() as p, *_]:                     # capture a sub-pattern
            return f"list starting with {p}"
        case {"user": {"name": str() as name}}:
            return f"user {name}"
        case _:
            return "other"


def demo_as():
    print("\n--- 6. Capture with as ---")
    print(parse("*"))                              # -> operator *
    print(parse([Point(1, 2), "x"]))               # -> list starting with Point(x=1, y=2)
    print(parse({"user": {"name": "ada"}}))        # -> user ada


# --- 7. Gotcha: bare names capture, they don't compare ---------------------
RED = "red"


class Color:
    RED = "red"


def demo_gotcha():
    print("\n--- 7. Bare-name gotcha ---")
    color = "blue"
    match color:
        case Color.RED:            # dotted name => compared as a value constant
            print("red!")
        case other:                # bare name => CAPTURES anything (like _)
            print("captured", other)   # -> captured blue
    # Writing `case RED:` would capture too and match everything, so Python
    # rejects a bare name before other cases ("makes remaining patterns
    # unreachable"). Use dotted names (Color.RED) or an Enum for constants.


if __name__ == "__main__":
    demo_literals()
    demo_sequences()
    demo_mappings()
    demo_classes()
    demo_guards()
    demo_as()
    demo_gotcha()
