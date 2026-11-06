# Lesson 3.4 — Special (Dunder) Methods

## What you'll learn

- How Python's syntax turns into method calls (`len(x)` → `x.__len__()`)
- Representation: `__init__`, `__repr__`, `__str__`, `__format__`
- Comparison & hashing: `__eq__`, `__lt__`, `__hash__`, `functools.total_ordering`
- Arithmetic: `__add__`, `__radd__`, `__iadd__`, `__mul__`/`__rmul__`, `__neg__`, `__bool__`
- Containers: `__len__`, `__getitem__`, `__setitem__`, `__delitem__`, `__contains__`, `__iter__`, `__reversed__`
- `__call__`, `__getattr__` / `__setattr__`, `__enter__` / `__exit__`
- Class-level machinery: `__slots__`, descriptors (`__get__`, `__set__`, `__set_name__`),
  `__init_subclass__`, `__new__`

Files: `example.py` (everyday protocols) and `example_advanced.py` (class machinery).

## Explanation

### Representation
- `__repr__` is for developers. It should be unambiguous, ideally valid code (`Money(9.5, 'EUR')`).
  Lists, the REPL and debuggers use it.
- `__str__` is the friendly form, used by `print()` and `str()`. If it's missing, Python falls back to `__repr__`.
- `__format__(spec)` handles `f"{obj:spec}"`.

### Comparison & hashing
Write `__eq__` and `__lt__`; `@functools.total_ordering` fills in the other
comparisons. **If you define `__eq__`, Python sets `__hash__ = None`**, so the objects
can't go in sets or be dict keys until you define `__hash__` yourself. Equal objects must have equal
hashes. Return `NotImplemented` (don't raise) for types you don't support.

### Arithmetic and `__radd__`
For `a + b`, Python calls `a.__add__(b)`. If that returns `NotImplemented`, it
tries `b.__radd__(a)`. That is why `1 + Money(10)` works, and why `sum()` (which
starts from `0`) needs `__radd__`. `__iadd__` handles `+=`.

```python
def __radd__(self, other):
    return self.__add__(other)
```

### Containers
`__len__` and `__getitem__` alone give you `len()`, indexing, slicing and even
iteration. Add `__contains__` for a fast or custom `in`, and `__iter__` for direct
iteration.

### `__call__` and attribute hooks
`__call__` makes instances callable like functions. `__getattr__` runs only
when normal lookup fails, which makes it handy for proxies and configs. `__setattr__` runs on
*every* assignment, so use `object.__setattr__` inside it to avoid infinite recursion.

### `__slots__`
`__slots__ = ("x", "y")` removes the per-instance `__dict__`. Objects get smaller
and faster, and assigning a misspelled attribute raises an error.

### Descriptors
An object with `__get__` / `__set__`, stored as a **class attribute**, takes over
`instance.attr` access. `__set_name__(owner, name)` tells it the attribute name it was assigned to.
`property`, methods, `classmethod` and `staticmethod` are all built on descriptors.

```python
class Positive:
    def __set_name__(self, owner, name): self.storage = "_" + name
    def __get__(self, obj, owner): return getattr(obj, self.storage)
    def __set__(self, obj, value):
        if value <= 0: raise ValueError
        setattr(obj, self.storage, value)
```

### `__init_subclass__`
`__init_subclass__` is a classmethod hook that runs whenever a subclass is defined, and it receives
any class keyword arguments (`class Csv(Plugin, name="csv")`). It's an easy way to build
plugin registries without metaclasses.

### `__new__`
`__new__(cls)` **creates** the object and `__init__(self)` then **initialises** it.
Override `__new__` for singletons, caching, or subclassing immutable types
(`float`, `str`, `tuple`), where the value is already fixed by the time `__init__` runs.

## Common mistakes

- Raising `TypeError` in `__add__` instead of returning `NotImplemented`, which stops
  `__radd__` from ever being tried.
- Defining `__eq__` without `__hash__`, then getting `TypeError: unhashable type`.
- Calling `self.x = ...` inside `__setattr__`, which recurses forever.
- Using `__getattribute__` when you meant `__getattr__`. The first one runs on *every* lookup.
- Expecting `__del__` to run at a predictable time. Use context managers for cleanup.
- Giving `__slots__` classes default class attributes with the same names as the slots, which raises `ValueError`.

## How to run

```bash
python example.py
python example_advanced.py
```

## Try it yourself

1. Write a `Matrix2x2` with `__matmul__` (`@`), `__eq__`, and a `__repr__`.
2. Write a descriptor `Typed(int)` that rejects values of the wrong type.
3. Write a `Shape` base class that uses `__init_subclass__` to require every subclass
   to define an `area` method (raise `TypeError` otherwise).
