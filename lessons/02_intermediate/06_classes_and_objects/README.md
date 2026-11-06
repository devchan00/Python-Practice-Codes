# Lesson 2.6 — Classes & objects

## What you'll learn

- Defining a class, `__init__` and `self`
- Class attributes vs instance attributes
- Inheritance, overriding and `super()`
- `__repr__` for useful debug output
- `@property`, `@classmethod`, `@staticmethod`
- `_x` (internal) and `__x` (name-mangled) attributes
- Multiple inheritance and the method resolution order (`__mro__`)

## Explanation

### Class, `__init__`, `self`

```python
class Animal:
    kingdom = "animalia"            # class attribute
    def __init__(self, name):       # constructor
        self.name = name            # instance attribute
    def speak(self):
        return f"{self.name} makes a sound"
```

Calling `Animal("Rex")` creates an object and runs `__init__` on it. `self` is
that object; `a.speak()` is really `Animal.speak(a)`.

### Class vs instance attributes

Class attributes live on the class and are shared. Instance attributes live
on each object (`obj.__dict__`). Lookup checks the instance first, then the
class — so assigning `a.kingdom = ...` creates a new instance attribute that
hides the class one. Keep mutable data (lists, dicts) in `__init__`, not on
the class.

### Inheritance and `super()`

```python
class Dog(Animal):
    def __init__(self, name, breed="mutt"):
        super().__init__(name)      # run the parent's setup
        self.breed = breed
    def speak(self):                # override
        return f"{self.name}: woof"
```

A subclass gets all of its parent's attributes and methods, and can override
any of them. `super()` calls the parent's version so you extend instead of
copy.

### `__repr__`

`__repr__` returns an unambiguous string, ideally looking like the code that
builds the object: `Dog('Rex', breed='lab')`. It's used by the REPL, in lists,
and by `print` when there's no `__str__`.

### `@property`

A method used like an attribute. Use it for computed values (`fahrenheit`) or
to validate on assignment with a `@x.setter`. A property without a setter is
read-only.

### `@classmethod` and `@staticmethod`

- `@classmethod` receives the class (`cls`) instead of an instance — ideal for
  alternative constructors like `Date.from_string("2024-03-15")`. Using `cls(...)`
  means subclasses get instances of themselves.
- `@staticmethod` receives nothing automatically — a plain helper function
  that belongs with the class logically (`Date.is_leap(2024)`).

### `_x` and `__x`

`_x` is a convention meaning "internal, don't rely on it". `__x` (two leading
underscores) is renamed to `_ClassName__x`, which prevents subclasses from
clashing with it by accident. Neither is real privacy.

### Multiple inheritance and the MRO

`class Duck(Walker, Swimmer)` inherits from both. When a method exists in
several parents, Python searches the classes in `Duck.__mro__` order:
`Duck → Walker → Swimmer → object`. `super()` follows the same order.

## Common mistakes

- Forgetting `self` as the first method parameter, or forgetting `self.` when
  setting attributes (`name = name` just makes a local variable).
- Mutable class attributes shared between all instances.
- Overriding `__init__` in a subclass and forgetting `super().__init__(...)`.
- Calling a property with parentheses (`t.fahrenheit()`) — it's not callable.
- Giving a property and its storage the same name (`self.celsius` inside the
  getter) — infinite recursion. Store it as `self._celsius`.
- Using deep inheritance where composition (holding another object) is simpler.

## How to run

```bash
python example.py
```

## Try it yourself

1. Write a `Rectangle` class with `width`/`height`, an `area` property, a
   `__repr__`, and a `@classmethod square(cls, side)`.
2. Make `Rectangle.width` a property that raises `ValueError` for negative values.
3. Create `class Amphibian(Swimmer, Walker)` and predict `Amphibian().move()`
   and `Amphibian.__mro__` before running it.
