# 4.6 Internals worth knowing

## What you'll learn

- Reference counting (`sys.getrefcount`) and the cycle collector (`gc`)
- `weakref` - pointing at an object without keeping it alive
- `dis.dis(fn)` - reading bytecode
- `sys.getsizeof(x)` - and why it is *shallow*
- `sys.modules` (the import cache) and `importlib` (dynamic imports)
- Classes are objects made by `type(name, bases, ns)`
- Descriptors (`Positive`) and metaclasses (`Meta`)

## Explanation

### Reference counting + GC

Every object counts how many references point at it. When the count drops to
0, CPython frees it immediately - that's why files opened in a function often
close "by themselves". Cycles (`a.other = b; b.other = a`) never reach 0, so a
**cycle collector** (`gc`) runs now and then to find unreachable groups.

```python
sys.getrefcount(obj)   # 3.14+ may not count its own argument; older adds +1
gc.collect()           # force a collection; returns number of objects found
```

### weakref

```python
ref = weakref.ref(obj)
ref()          # the object, or None once it's been freed
cache = weakref.WeakValueDictionary()   # entries disappear with their objects
```

Use for caches, observers and parent pointers that shouldn't cause leaks.

### dis

```python
import dis
dis.dis(lambda x: x + 1)
# LOAD_FAST x, LOAD_SMALL_INT 1, BINARY_OP (+), RETURN_VALUE
```

Bytecode is what the interpreter loop executes. Handy for seeing why one
version of code does more work than another. Instruction names change between
Python versions.

### sys.getsizeof

Returns the size of the object itself, **not** what it refers to: a list of
1000 big strings reports only the list's array of pointers.

### sys.modules and importlib

`import x` first checks the `sys.modules` dict; only on a miss does it find,
run and cache the module. So a module's top-level code runs once per process.

```python
mod = importlib.import_module("json")         # import by a string name
plugin = importlib.import_module(f"plugins.{name}")
```

### Classes are objects

```python
Person = type("Person", (object,), {"species": "human"})
# same as:   class Person: species = "human"
```

`type` is the default **metaclass** - the class of classes.

### Descriptors

An object with `__get__` / `__set__` placed on a class controls attribute access:

```python
class Positive:                         # descriptor
    def __set_name__(self, owner, name):
        self.n = "_" + name
    def __get__(self, obj, owner=None):
        return getattr(obj, self.n)
    def __set__(self, obj, v):
        if v <= 0:
            raise ValueError("must be > 0")
        setattr(obj, self.n, v)

class Account:
    balance = Positive()
```

`property`, methods, `classmethod` and `staticmethod` all work this way.

### Metaclasses

```python
class Meta(type):                       # metaclass
    def __new__(mcls, name, bases, ns):
        return super().__new__(mcls, name, bases, ns)
```

`Meta.__new__` runs when a `class` statement is executed, so it can register,
check or modify classes. Prefer `__init_subclass__` or a class decorator when
they are enough.

## Common mistakes

- Relying on exact `getrefcount` numbers - they vary by version.
- Assuming `del x` deletes the object (it deletes one *name*; the object goes
  when the last reference does).
- Using `getsizeof` to measure a nested structure's total memory.
- Forgetting `if obj is None: return self` in `__get__`, so `Account.balance`
  crashes.
- Using metaclasses where a decorator would do.

## How to run

```bash
cd lessons/04_professional/06_internals
python example.py
```

## Try it yourself

1. `dis.dis` both `[x*2 for x in xs]` and `list(map(lambda x: x*2, xs))`. Which does more?
2. Write a `deep_sizeof(obj)` that recursively sums `getsizeof` for lists,
   dicts, tuples and sets (track `id`s you've seen to avoid double-counting).
3. Write a `NonEmptyStr` descriptor and use it on a `User.name` attribute.
