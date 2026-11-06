"""Soft keywords: match / case, type, and _.

Soft keywords are only special in a particular context; everywhere else they are
ordinary names you may use for variables. `match`/`case` give structural pattern
matching (3.10+), `type` creates a type alias (3.12+), and `_` is the
throwaway variable, the wildcard pattern in `case _:`, and the "last result" in
the interactive REPL. This file demonstrates each one and shows that they still
work as normal names outside their special context.
"""

import keyword


# --- 0. Which soft keywords does my Python know? ---
def show_soft_keywords():
    print(keyword.softkwlist)
    # -> ['_', 'case', 'match', 'type'] on 3.12-3.14
    #    (3.15 also lists 'lazy', for the new `lazy import` statement)
    print(keyword.iskeyword("match"))      # -> False  (not a *reserved* keyword)
    print(keyword.issoftkeyword("match"))  # -> True


# --- 1. match / case: literal patterns ---
def run_command(cmd):
    match cmd:
        case "go":
            return "moving"
        case "stop" | "halt":              # `|` = OR between patterns
            return "stopping"
        case _:                            # `_` = wildcard: matches anything, binds nothing
            return f"unknown command {cmd!r}"


def demo_match_literals():
    print(run_command("go"))               # -> moving
    print(run_command("halt"))             # -> stopping
    print(run_command("jump"))             # -> unknown command 'jump'


# --- 2. match / case: structure (sequences, dicts, classes, guards) ---
class Point:
    __match_args__ = ("x", "y")            # lets us write Point(x, y) positionally

    def __init__(self, x, y):
        self.x, self.y = x, y


def describe(value):
    match value:
        case []:
            return "empty list"
        case [x]:
            return f"one item: {x}"
        case [first, *rest]:               # unpack a sequence; *rest grabs the remainder
            return f"starts with {first}, {len(rest)} more"
        case {"action": "move", "to": dest}:   # dict pattern: checks key, captures value
            return f"move to {dest}"
        case Point(x=0, y=0):
            return "origin"
        case Point(x, y) if x == y:        # `if` guard: extra condition
            return f"diagonal point at {x}"
        case Point(x, y):
            return f"point({x}, {y})"
        case int() | float() as num:       # type check + `as` captures the whole value
            return f"number {num}"
        case _:
            return "something else"


def demo_match_structure():
    print(describe([]))                    # -> empty list
    print(describe([7]))                   # -> one item: 7
    print(describe([1, 2, 3]))             # -> starts with 1, 2 more
    print(describe({"action": "move", "to": "kitchen"}))   # -> move to kitchen
    print(describe(Point(0, 0)))           # -> origin
    print(describe(Point(2, 2)))           # -> diagonal point at 2
    print(describe(Point(1, 5)))           # -> point(1, 5)
    print(describe(3.5))                   # -> number 3.5
    print(describe("hi"))                  # -> something else
    # WHY: match checks the SHAPE of data, which replaces long if/elif chains
    # full of isinstance() and len() checks.


# --- 3. match / case are still normal names elsewhere ---
def demo_match_as_name():
    import re
    match = re.match(r"\d+", "123abc")     # perfectly legal: `match` is only special
    print(match.group())                   # -> 123     at the start of a match statement
    case = "upper"
    print(case)                            # -> upper


# --- 4. type: the type-alias statement (3.12+) ---
type Vec = list[float]                     # a named alias for a type
type Pair[T] = tuple[T, T]                 # aliases can be generic


def norm(v: Vec) -> float:
    return sum(x * x for x in v) ** 0.5


def demo_type_alias():
    print(norm([3.0, 4.0]))                # -> 5.0
    print(Vec)                             # -> Vec
    print(Vec.__value__)                   # -> list[float]   (evaluated lazily)
    print(Pair.__type_params__)            # -> (T,)
    # `type` is still the normal built-in function too:
    print(type(42))                        # -> <class 'int'>


# --- 5. _: throwaway variable, wildcard, REPL last result ---
def demo_underscore():
    # Throwaway: "I need a loop variable but don't care about it".
    for _ in range(3):
        print("hi", end=" ")
    print()                                # -> hi hi hi

    # Ignore parts when unpacking.
    name, _, age = ("Ann", "unused", 30)
    print(name, age)                       # -> Ann 30

    # Wildcard in match (see section 1): `case _:` matches anything.

    # In the interactive REPL only, `_` holds the last printed result:
    #   >>> 2 + 3
    #   5
    #   >>> _ * 10
    #   50
    # (This does not happen in scripts.)

    # Big numbers: the underscore in 1_000_000 is digit grouping, not the variable.
    print(1_000_000)                       # -> 1000000


if __name__ == "__main__":
    print("--- 0. soft keyword list ---");  show_soft_keywords()
    print("--- 1. match literals ---");     demo_match_literals()
    print("--- 2. match structure ---");    demo_match_structure()
    print("--- 3. match as a name ---");    demo_match_as_name()
    print("--- 4. type alias ---");         demo_type_alias()
    print("--- 5. underscore ---");         demo_underscore()
