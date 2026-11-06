"""Lesson 3.4 - Special (dunder) methods, part 2: class-level machinery.

These hooks control *how classes and attributes work*, not how individual
operators behave: ``__slots__`` replaces the per-instance ``__dict__`` with
fixed storage; descriptors (``__get__`` / ``__set__`` / ``__set_name__``) let
an object living on the class intercept attribute access on instances (this is
how ``property`` works); ``__init_subclass__`` runs whenever someone
subclasses you (great for plugin registries); and ``__new__`` actually
creates the instance before ``__init__`` initialises it.
"""

import sys


# --- 1. __slots__ -----------------------------------------------------------
class PointDict:
    def __init__(self, x, y):
        self.x, self.y = x, y


class PointSlots:
    __slots__ = ("x", "y")         # only these attributes; no __dict__

    def __init__(self, x, y):
        self.x, self.y = x, y


def demo_slots():
    print("--- 1. __slots__ ---")
    d, s = PointDict(1, 2), PointSlots(1, 2)
    print(hasattr(d, "__dict__"), hasattr(s, "__dict__"))   # -> True False
    d_size = sys.getsizeof(d) + sys.getsizeof(d.__dict__)
    print(sys.getsizeof(s) < d_size)   # -> True (smaller: matters for millions)
    try:
        s.z = 3                        # typo-proof: unknown attributes rejected
    except AttributeError as e:
        print("AttributeError:", e)    # -> AttributeError: 'PointSlots' object has no attribute 'z' ...


# --- 2. Descriptors: __get__ / __set__ / __set_name__ -----------------------
class Positive:
    """A reusable validated attribute. One Positive object lives on the
    *class*; it stores each instance's value in that instance's __dict__."""

    def __set_name__(self, owner, name):   # called once, at class creation
        self.name = name                   # learns its attribute name ("price")
        self.storage = "_" + name

    def __get__(self, instance, owner):
        if instance is None:               # accessed on the class itself
            return self
        return getattr(instance, self.storage)

    def __set__(self, instance, value):
        if value <= 0:
            raise ValueError(f"{self.name} must be > 0, got {value}")
        setattr(instance, self.storage, value)


class Product:
    price = Positive()             # __set_name__(Product, "price") runs here
    quantity = Positive()

    def __init__(self, price, quantity):
        self.price = price         # goes through Positive.__set__
        self.quantity = quantity


def demo_descriptors():
    print("\n--- 2. Descriptors ---")
    p = Product(9.99, 3)
    print(p.price, p.quantity)     # -> 9.99 3
    print(Product.price.name)      # -> price  (set by __set_name__)
    try:
        p.quantity = -1
    except ValueError as e:
        print("ValueError:", e)    # -> ValueError: quantity must be > 0, got -1


# --- 3. __init_subclass__: auto-registering plugins -------------------------
class Plugin:
    registry = {}

    def __init_subclass__(cls, /, name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        # Runs when a subclass is *defined* - no decorator or metaclass needed.
        Plugin.registry[name or cls.__name__.lower()] = cls


class CsvExporter(Plugin, name="csv"):   # class keyword args go to the hook
    pass


class JsonExporter(Plugin):
    pass


def demo_init_subclass():
    print("\n--- 3. __init_subclass__ ---")
    print(sorted(Plugin.registry))     # -> ['csv', 'jsonexporter']
    print(Plugin.registry["csv"].__name__)   # -> CsvExporter


# --- 4. __new__: controlling instance creation ------------------------------
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):     # runs BEFORE __init__, returns the object
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class Celsius(float):
    """Immutable types (int, float, str, tuple) can only be customised in
    __new__, because by the time __init__ runs the value is already fixed."""

    def __new__(cls, value):
        if value < -273.15:
            raise ValueError("below absolute zero")
        return super().__new__(cls, round(value, 1))


def demo_new():
    print("\n--- 4. __new__ ---")
    a, b = Singleton(), Singleton()
    print(a is b)                  # -> True (same object both times)
    t = Celsius(21.456)
    print(t, isinstance(t, float), t + 1)   # -> 21.5 True 22.5


# --- 5. __radd__ recap: making sum() work -----------------------------------
class Vector:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        if other == 0:             # the 0 that sum() starts from
            return self
        return NotImplemented

    __radd__ = __add__             # 0 + Vector -> int fails -> Vector.__radd__


def demo_radd():
    print("\n--- 5. __radd__ and sum() ---")
    print(sum([Vector(1, 2), Vector(3, 4), Vector(5, 6)]))   # -> Vector(9, 12)


if __name__ == "__main__":
    demo_slots()
    demo_descriptors()
    demo_init_subclass()
    demo_new()
    demo_radd()
