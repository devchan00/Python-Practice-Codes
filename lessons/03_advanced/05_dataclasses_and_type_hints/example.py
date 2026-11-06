"""Lesson 3.5 - Dataclasses & type hints.

``@dataclass`` writes the boring parts of a class for you (``__init__``,
``__repr__``, ``__eq__``, optionally ordering, hashing, immutability and
``__slots__``) from annotated fields. Type hints describe what types a value
should have. They are documentation that tools such as mypy, pyright and IDEs
check *before* you run the program. Python itself does NOT enforce them at
runtime; this file demonstrates that too.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from collections.abc import Callable
from typing import (Final, Generic, Literal, Protocol, TypedDict, TypeVar,
                    get_type_hints)


# --- 1. A basic dataclass ---------------------------------------------------
@dataclass
class Point:
    x: float
    y: float = 0.0                 # fields with defaults must come after the rest


def demo_basic_dataclass():
    print("--- 1. Basic dataclass ---")
    p = Point(1.5)
    print(p)                       # -> Point(x=1.5, y=0.0)   (free __repr__)
    print(p == Point(1.5, 0.0))    # -> True                  (free __eq__)
    print(dataclasses.asdict(p))   # -> {'x': 1.5, 'y': 0.0}
    print(dataclasses.replace(p, y=9))  # -> Point(x=1.5, y=9)  (a modified copy)


# --- 2. field(default_factory=...) -----------------------------------------
@dataclass
class Cart:
    owner: str
    items: list[str] = field(default_factory=list)  # NEW list per instance
    discount: float = field(default=0.0, repr=False)  # hidden from repr
    total: int = field(init=False, default=0)        # not an __init__ arg

    def __post_init__(self):       # runs right after the generated __init__
        self.total = len(self.items)


def demo_default_factory():
    print("\n--- 2. field(default_factory) ---")
    a, b = Cart("ann"), Cart("bob")
    a.items.append("apple")
    print(a, b)    # -> Cart(owner='ann', items=['apple'], total=0) Cart(owner='bob', items=[], total=0)
    # `items: list = []` would be rejected: a single shared mutable default
    # is a classic bug, so dataclasses force you to use default_factory.
    print(Cart("cy", ["x", "y"]).total)   # -> 2  (computed in __post_init__)


# --- 3. frozen=True, slots=True, order=True ---------------------------------
@dataclass(frozen=True, slots=True, order=True)
class Card:
    rank: int
    suit: str


@dataclass(slots=True, frozen=True)    # the cheatsheet's example
class Point:
    x: float
    y: float = 0.0
    tags: tuple[str, ...] = ()         # immutable default is safe (a list is not)


def demo_frozen_slots():
    print("\n--- 3. frozen / slots / order ---")
    c = Card(10, "hearts")
    try:
        c.rank = 11                # frozen: no assignment after creation
    except dataclasses.FrozenInstanceError as e:
        print("FrozenInstanceError:", e)   # -> FrozenInstanceError: cannot assign to field 'rank'
    print(hash(c) == hash(Card(10, "hearts")))  # -> True (frozen => hashable)
    print(hasattr(c, "__dict__"))  # -> False (slots=True: compact instances)
    print(sorted([Card(3, "s"), Card(2, "h")]))  # -> [Card(rank=2, suit='h'), Card(rank=3, suit='s')]
    print(Point(1.5))              # -> Point(x=1.5, y=0.0, tags=())
    print(Point(1, 2, ("home",)))  # -> Point(x=1, y=2, tags=('home',))


# --- 4. Basic hints: built-in generics, X | None, Callable ------------------
def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def find(names: dict[str, int], key: str) -> int | None:   # "int or None"
    return names.get(key)


def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)


def demo_basic_hints():
    print("\n--- 4. Basic hints ---")
    print(mean([1, 2, 3]))                 # -> 2.0
    print(find({"a": 1}, "z"))             # -> None
    print(apply(lambda x, y: x * y, 6, 7)) # -> 42
    print(mean.__annotations__)  # -> {'values': 'list[float]', 'return': 'float'}
    # (strings because of `from __future__ import annotations`)


# --- 5. Hints are NOT enforced at runtime ----------------------------------
def double(n: int) -> int:
    return n * 2


def demo_not_enforced():
    print("\n--- 5. Hints aren't enforced ---")
    print(double("ha"))            # -> haha   no error! str * 2 is valid
    print(Point("not", "numbers")) # -> Point(x='not', y='numbers')
    # mypy would flag both lines. If you need runtime checks, write them
    # yourself (isinstance) or use a validation library such as pydantic.
    hints = get_type_hints(double)
    value = "ha"
    print(isinstance(value, hints["n"]))   # -> False (a manual check)


# --- 6. TypeVar & Generic (classic syntax) ---------------------------------
T = TypeVar("T")


def first_classic(items: list[T]) -> T:    # returns the SAME type it gets
    return items[0]


class Box(Generic[T]):
    def __init__(self, item: T) -> None:
        self.item = item

    def get(self) -> T:
        return self.item


# --- 7. 3.12+ inline generics and the `type` statement ---------------------
def first[T](items: list[T]) -> T:          # no TypeVar boilerplate needed
    return items[0]


class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()


type Vector = list[float]                   # a type alias (3.12+)
type Pair[K] = tuple[K, K]                  # aliases can be generic too


def scale(v: Vector, k: float) -> Vector:
    return [x * k for x in v]


def demo_generics():
    print("\n--- 6/7. Generics ---")
    print(first_classic(["a", "b"]), Box(42).get())   # -> a 42
    print(first([3, 4]))                   # -> 3
    s = Stack[int]()
    s.push(1); s.push(2)
    print(s.pop())                         # -> 2
    print(scale([1.0, 2.0], 3))            # -> [3.0, 6.0]
    print(Vector.__value__, Pair.__type_params__)   # -> list[float] (K,)


# --- 8. Protocol: structural ("duck") typing --------------------------------
class Drawable(Protocol):
    def draw(self) -> str: ...


class Circle:                     # does NOT inherit from Drawable...
    def draw(self) -> str:
        return "()"


class Square:
    def draw(self) -> str:
        return "[]"


def render(shapes: list[Drawable]) -> str:   # ...but still type-checks
    return " ".join(s.draw() for s in shapes)


# --- 9. Literal, Final, TypedDict ------------------------------------------
Mode = Literal["r", "w", "a"]               # only these exact values
MAX_RETRIES: Final = 3                      # type checker forbids reassigning


class Movie(TypedDict):                     # a dict with known keys/types
    title: str
    year: int


def open_mode(mode: Mode) -> str:
    return f"opening in {mode!r} mode"


def demo_protocol_literal_etc():
    print("\n--- 8. Protocol ---")
    print(render([Circle(), Square()]))     # -> () []
    print("\n--- 9. Literal / Final / TypedDict ---")
    print(open_mode("w"))                   # -> opening in 'w' mode
    print(MAX_RETRIES)                      # -> 3
    m: Movie = {"title": "Alien", "year": 1979}
    print(type(m).__name__, m["title"])     # -> dict Alien (just a dict at runtime)


if __name__ == "__main__":
    demo_basic_dataclass()
    demo_default_factory()
    demo_frozen_slots()
    demo_basic_hints()
    demo_not_enforced()
    demo_generics()
    demo_protocol_literal_etc()
