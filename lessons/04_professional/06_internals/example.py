"""Lesson 4.6 - Internals worth knowing.

A peek under the hood of CPython: objects are freed when their reference count
hits zero, with a cycle-detecting garbage collector as backup; ``weakref`` lets
you point at an object without keeping it alive; ``dis`` shows the bytecode
the interpreter runs; ``sys.getsizeof`` reports shallow size; ``sys.modules``
is the import cache and ``importlib`` imports by name at runtime. Finally,
classes are themselves objects made by ``type`` - which leads to descriptors
(the ``Positive`` validator) and metaclasses (``Meta``) from the cheatsheet.
"""

import dis
import gc
import importlib
import sys
import weakref


# --- 1. Reference counting ---
def demo_refcount() -> None:
    print("\n--- 1. Reference counting ---")
    data = [1, 2, 3]
    # Older Pythons count getrefcount's own argument too (+1); 3.14+ may
    # "borrow" that reference, so expect 1 or 2 here. Watch the CHANGE.
    print("refs to data:", sys.getrefcount(data))  # -> 1 on 3.14+ (2 on older)
    alias = data
    holder = {"x": data}
    print("after alias + dict:", sys.getrefcount(data))  # -> 3 on 3.14+ (+2 references)
    del alias, holder
    print("after del:", sys.getrefcount(data))  # -> back to 1
    # When the count reaches 0, CPython frees the object IMMEDIATELY.


# --- 2. The cycle collector (gc) ---
class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.other: "Node | None" = None


def demo_gc() -> None:
    print("\n--- 2. Garbage collector ---")
    a, b = Node("a"), Node("b")
    a.other, b.other = b, a  # a <-> b: a reference CYCLE
    probe = weakref.ref(a)  # lets us check if `a` is still alive
    del a, b  # refcounts never hit 0: each still points at the other
    print("alive after del:", probe() is not None)  # -> True (stuck in a cycle)
    found = gc.collect()  # the cycle collector finds unreachable groups
    print("gc.collect() freed objects:", found > 0)  # -> True
    print("alive after collect:", probe() is not None)  # -> False
    print("gc thresholds:", gc.get_threshold())  # automatic collection triggers


# --- 3. weakref: refer without keeping alive ---
class BigImage:
    def __init__(self, name: str) -> None:
        self.name = name


def demo_weakref() -> None:
    print("\n--- 3. weakref ---")
    img = BigImage("cat.png")
    ref = weakref.ref(img)
    print("ref() ->", ref().name)  # -> cat.png
    del img
    print("after del, ref() ->", ref())  # -> None: the object was freed

    cache: weakref.WeakValueDictionary[str, BigImage] = weakref.WeakValueDictionary()
    pic = BigImage("dog.png")
    cache["dog"] = pic
    print("in cache:", "dog" in cache)  # -> True
    del pic
    print("in cache after del:", "dog" in cache)  # -> False: entries vanish automatically
    # Great for caches and observers that shouldn't cause memory leaks.


# --- 4. dis: see the bytecode ---
def add_one(x: int) -> int:
    return x + 1


def demo_dis() -> None:
    print("\n--- 4. dis.dis ---")
    dis.dis(add_one)
    # -> LOAD_FAST(_BORROW) x / LOAD_SMALL_INT 1 / BINARY_OP 0 (+) / RETURN_VALUE
    # Python source compiles to bytecode, which the interpreter loop executes.
    # (Exact instruction names change between Python versions.)


# --- 5. sys.getsizeof: shallow size in bytes ---
def demo_sizeof() -> None:
    print("\n--- 5. sys.getsizeof ---")
    for obj in (0, 2**100, "", "hello", [], [1, 2, 3], (), {}, set()):
        print(f"  {obj!r:<40} {sys.getsizeof(obj):>4} bytes")
    nested = [list(range(1000))]
    print("outer list only:", sys.getsizeof(nested), "bytes")  # -> ~64: SHALLOW!
    print("inner list:", sys.getsizeof(nested[0]), "bytes")  # -> ~8000
    # getsizeof counts the container, not the objects it points to.


# --- 6. sys.modules and importlib ---
def demo_imports() -> None:
    print("\n--- 6. sys.modules / importlib ---")
    print("json loaded yet?", "json" in sys.modules)  # -> False (probably)
    json_mod = importlib.import_module("json")  # import by NAME (a string)
    print("json loaded now?", "json" in sys.modules)  # -> True
    import json  # second import is just a dictionary lookup in sys.modules
    print("same module object:", json is json_mod)  # -> True
    print(json_mod.dumps({"dynamic": True}))  # -> {"dynamic": true}
    # Use for plugins: importlib.import_module(f"plugins.{name}")
    # importlib.reload(mod) re-executes a module (rarely needed).


# --- 7. Classes are objects: type(name, bases, ns) ---
def demo_type() -> None:
    print("\n--- 7. type(name, bases, ns) ---")

    def greet(self) -> str:
        return f"hi, I'm {self.name}"

    # Exactly equivalent to:  class Person: species = "human"; def greet(self)...
    Person = type("Person", (object,), {"species": "human", "greet": greet})
    p = Person()
    p.name = "Ada"
    print(p.greet(), "|", Person.species)  # -> hi, I'm Ada | human
    print(type(p) is Person, type(Person))  # -> True <class 'type'>
    print(type(type))  # -> <class 'type'>: type is its own metaclass


# --- 8. A descriptor: Positive ---
class Positive:  # descriptor
    def __set_name__(self, owner, name):
        self.n = "_" + name  # called once, when the owning class is created

    def __get__(self, obj, owner=None):
        if obj is None:  # accessed on the class itself, e.g. Account.balance
            return self
        return getattr(obj, self.n)

    def __set__(self, obj, v):
        if v <= 0:
            raise ValueError("must be > 0")
        setattr(obj, self.n, v)


class Account:
    balance = Positive()  # the descriptor lives on the CLASS

    def __init__(self, balance: float) -> None:
        self.balance = balance  # goes through Positive.__set__


def demo_descriptor() -> None:
    print("\n--- 8. Descriptor ---")
    acc = Account(100)
    print("balance:", acc.balance, "stored as:", vars(acc))  # -> 100 {'_balance': 100}
    try:
        acc.balance = -5
    except ValueError as e:
        print("rejected:", e)  # -> rejected: must be > 0
    # property, classmethod, staticmethod and methods themselves are descriptors.


# --- 9. A metaclass: Meta ---
class Meta(type):  # metaclass
    registry: list[str] = []

    def __new__(mcls, name, bases, ns):
        # Runs when a CLASS statement using this metaclass is executed.
        cls = super().__new__(mcls, name, bases, ns)
        mcls.registry.append(name)
        return cls


class Plugin(metaclass=Meta):
    pass


class CsvPlugin(Plugin):  # subclasses inherit the metaclass
    pass


def demo_metaclass() -> None:
    print("\n--- 9. Metaclass ---")
    print("registered:", Meta.registry)  # -> ['Plugin', 'CsvPlugin']
    print("type(CsvPlugin):", type(CsvPlugin).__name__)  # -> Meta
    # Most needs are simpler with __init_subclass__ or a class decorator;
    # reach for metaclasses only when those aren't enough.


def main() -> None:
    demo_refcount()
    demo_gc()
    demo_weakref()
    demo_dis()
    demo_sizeof()
    demo_imports()
    demo_type()
    demo_descriptor()
    demo_metaclass()


if __name__ == "__main__":
    main()
