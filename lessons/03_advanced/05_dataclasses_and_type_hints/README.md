# Lesson 3.5 — Dataclasses & Type Hints

## What you'll learn

- `@dataclass`: the methods it generates, `asdict`, `replace`, `__post_init__`
- `field(default_factory=list)`, and why mutable defaults need it
- `frozen=True`, `slots=True`, `order=True`
- Type hints: `list[int]`, `dict[str, int]`, `int | None`, `Callable[[int, int], int]`
- Generics: `TypeVar` + `Generic` (classic), and 3.12+ `def first[T]` / `class Stack[T]`
- The `type` alias statement (3.12+)
- `Protocol`, `Literal`, `Final`, `TypedDict`
- **Hints are not enforced at runtime**

## Explanation

### Dataclasses
```python
@dataclass
class Point:
    x: float
    y: float = 0.0
```
From the annotated fields, Python generates `__init__`, `__repr__` and `__eq__`.
`dataclasses.asdict(p)` turns an instance into a dict, and `dataclasses.replace(p, y=9)` makes a modified copy.
`__post_init__` runs after `__init__`, which is the place for computed fields or validation.

### `field(default_factory=...)`
Default values are evaluated **once**, so `items: list = []` would make every
instance share one list. Dataclasses refuse mutable defaults; write
`field(default_factory=list)` so each instance gets a fresh list. `field()` can
also hide a field from the repr (`repr=False`) or leave it out of `__init__` (`init=False`).

### Options
- `frozen=True` makes instances immutable (assignment raises `FrozenInstanceError`) and hashable.
- `slots=True` uses `__slots__`, which gives smaller and faster instances.
- `order=True` generates `<`, `>`, and so on, comparing fields as a tuple in definition order.

### Type hints
```python
def find(names: dict[str, int], key: str) -> int | None: ...
def apply(func: Callable[[int, int], int], a: int, b: int) -> int: ...
```
`X | None` means "an X or `None`" (the older spelling is `Optional[X]`).
`Callable[[args], return]` describes a function's signature.

### Generics
A type variable says "the same type in and out":
```python
def first[T](items: list[T]) -> T:   # 3.12+
    return items[0]
class Stack[T]: ...
type Vector = list[float]             # alias statement
```
The classic spelling is `T = TypeVar("T")` and `class Box(Generic[T])`. You'll still see it in
older code.

### Protocol, Literal, Final, TypedDict
- `Protocol` gives structural typing: any class with a matching `draw()` method counts,
  without inheriting from the protocol.
- `Literal["r", "w"]` allows only those exact values.
- `Final` tells the type checker the name must never be reassigned.
- `TypedDict` describes a dict with fixed keys. At runtime it's still a plain `dict`.

### Not enforced!
```python
def double(n: int) -> int: return n * 2
double("ha")    # 'haha' — no error at runtime
```
Hints are checked only by tools like **mypy** and **pyright** and by your IDE. If you need runtime validation,
write `isinstance` checks or use a library such as pydantic.

## Common mistakes

- Writing `items: list = []` in a dataclass, which raises `ValueError: mutable default`.
- Putting a field without a default after one that has a default, which raises `TypeError`.
- Expecting `int` hints to convert or reject values at runtime. They do neither.
- Writing `Optional[int]` when you mean "this argument is optional". It only means "may be `None`".
- Mutating a list held inside a `frozen` dataclass. Frozen is shallow, so this is allowed.

## How to run

```bash
python example.py
```

## Try it yourself

1. Write `@dataclass(frozen=True) class Money` with a `__post_init__` that rejects
   negative amounts.
2. Write a generic `def last[T](items: list[T]) -> T | None` that returns `None` for empty lists.
3. Define a `Protocol` called `SupportsClose` with `close()`, and a function that closes a list
   of such objects. Pass it two unrelated classes.
