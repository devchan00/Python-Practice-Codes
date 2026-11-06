"""Lesson 3.7 - Standard-library power tools, part 3: pathlib, Enum, ABC.

``pathlib.Path`` is the modern object-oriented way to work with file paths:
you join them with ``/``, and reading, writing and globbing are methods.
``enum`` gives named constants that can't be mixed up with plain values.
``abc`` lets you define abstract base classes, i.e. interfaces whose
subclasses must implement certain methods before they can be instantiated.
"""

import tempfile
from abc import ABC, abstractmethod
from enum import Enum, IntEnum, StrEnum, auto
from pathlib import Path


# --- 1. pathlib -------------------------------------------------------------
def demo_pathlib():
    print("--- 1. pathlib ---")
    # Use a temporary directory so nothing is left behind.
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        notes = root / "docs" / "notes.txt"        # `/` joins paths portably
        notes.parent.mkdir(parents=True, exist_ok=True)
        notes.write_text("line 1\nline 2\n", encoding="utf-8")
        (root / "docs" / "todo.md").write_text("- learn pathlib", encoding="utf-8")
        (root / "main.py").write_text("print('hi')", encoding="utf-8")

        print(notes.name, notes.stem, notes.suffix)  # -> notes.txt notes .txt
        print(notes.parent.name)                     # -> docs
        print(notes.exists(), notes.is_file())       # -> True True
        print(notes.read_text(encoding="utf-8").splitlines())  # -> ['line 1', 'line 2']
        print(sorted(p.name for p in root.rglob("*.*")))  # -> ['main.py', 'notes.txt', 'todo.md']
        print(sorted(p.name for p in (root / "docs").glob("*.md")))  # -> ['todo.md']
        print(notes.with_suffix(".bak").name)        # -> notes.bak
        print(notes.relative_to(root).as_posix())    # -> docs/notes.txt
    print(root.exists())                             # -> False (cleaned up)
    print(Path("a/b/c.tar.gz").suffixes)             # -> ['.tar', '.gz'] (pure path ops, no disk)


# --- 2. Enum, auto, StrEnum -------------------------------------------------
class Color(Enum):
    RED = auto()                   # auto() picks values for you: 1, 2, 3
    GREEN = auto()
    BLUE = auto()


class Status(StrEnum):             # members ARE strings (3.11+)
    ACTIVE = auto()                # auto() in StrEnum -> lower-case name
    DISABLED = auto()


class Priority(IntEnum):           # members are ints: comparable, sortable
    LOW = 1
    HIGH = 3


def demo_enum():
    print("\n--- 2. Enum / auto / StrEnum ---")
    c = Color.GREEN
    print(c, c.name, c.value)      # -> Color.GREEN GREEN 2
    print(Color["RED"], Color(3))  # -> Color.RED Color.BLUE (lookup by name / value)
    print([m.name for m in Color]) # -> ['RED', 'GREEN', 'BLUE']
    print(Color.RED == 1)          # -> False (plain Enum is NOT its value: safer)
    print(Status.ACTIVE == "active", f"{Status.DISABLED}")  # -> True disabled
    print(Priority.HIGH > Priority.LOW)                     # -> True
    match c:                       # Enums are ideal for match/case constants
        case Color.GREEN:
            print("go!")           # -> go!


# --- 3. ABC & abstractmethod ------------------------------------------------
class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        """Every concrete shape MUST implement this."""

    def describe(self):            # normal methods can use the abstract ones
        return f"{type(self).__name__} with area {self.area():.2f}"


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2


class Broken(Shape):               # forgot to implement area()
    pass


def demo_abc():
    print("\n--- 3. ABC / abstractmethod ---")
    print(Square(3).describe())    # -> Square with area 9.00
    for cls in (Shape, Broken):
        try:
            cls()                  # the error happens at creation, not at call time
        except TypeError as e:
            print("TypeError:", e)
    # -> TypeError: Can't instantiate abstract class Shape without an implementation for abstract method 'area'
    # -> TypeError: Can't instantiate abstract class Broken ... 'area'
    print(isinstance(Square(1), Shape))   # -> True


if __name__ == "__main__":
    demo_pathlib()
    demo_enum()
    demo_abc()
