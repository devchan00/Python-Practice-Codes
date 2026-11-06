# Built-in Functions & Types

Built-ins are the functions and types Python gives you without any `import`:
`print`, `len`, `range`, `int`, `sorted` and friends. Knowing them well makes
your code shorter and faster than hand-written loops.

## What you'll learn

- Numbers and conversion: `abs`, `bin`/`hex`/`oct`, `bool`, `int`/`float`/`str`, `chr`/`ord`, `divmod`, `pow`, `round`, `format`, `repr`, `hash`
- Binary data: `bytes`, `bytearray`, `memoryview`
- Collections: `dict`/`list`/`set`/`tuple`, `frozenset`
- Iteration helpers: `len`, `all`, `any`, `sum`, `max`/`min`, `sorted`, `reversed`, `enumerate`, `zip`, `map`, `filter`, `range`, `slice`, `iter`/`next`, `aiter`/`anext`
- Objects and introspection: `type`, `isinstance`, `issubclass`, `object`, `callable`, `id`, `dir`, `vars`, `getattr`/`setattr`/`hasattr`, `globals`/`locals`
- Class helpers: `classmethod`, `staticmethod`, `property`, `super`
- I/O and the rest: `print`, `open`, `input`, `help`, `breakpoint`, `__import__`, `eval`/`exec`

## Files

| File | Built-ins |
|------|-----------|
| `example_1_numbers_text_bytes.py` | abs, bin/hex/oct, bool, int/float/str, chr/ord, divmod, pow, round, format, repr, hash, bytes, bytearray, memoryview |
| `example_2_collections_iteration.py` | dict/list/set/tuple, frozenset, len, all, any, sum, max/min, sorted, reversed, enumerate, zip, map, filter, range, slice, iter/next, aiter/anext |
| `example_3_objects_io_introspection.py` | type, isinstance, issubclass, object, callable, id, dir, vars, getattr/setattr/hasattr, globals/locals, classmethod, staticmethod, property, super, print, open, __import__, eval/exec, (breakpoint, input, help in comments) |

## Explanation

### Numbers and conversion
- `abs(-7)` -> `7`. `bin(5)`, `hex(255)`, `oct(15)` -> `'0b101'`, `'0xff'`, `'0o17'` (strings!).
- `int("42")`, `float("2.5")`, `str(10)`, `bool(x)` convert between types. `int(3.99)` truncates to `3`.
- `chr(65)` -> `'A'`, `ord('A')` -> `65` (Unicode code points).
- `divmod(17, 5)` -> `(3, 2)`; `pow(2, 10, 1000)` computes `2**10 % 1000` efficiently.
- `round(2.5)` -> `2`: exact halves round to the nearest **even** number (banker's rounding).
- `format(3.14159, ".2f")` -> `'3.14'`; `repr(x)` gives the developer view (`'hi\n'` with quotes).
- `hash(x)` is the number dicts and sets use to find keys; lists aren't hashable.

### Binary data
`bytes` is an immutable sequence of 0-255 values (`b'abc'`), `bytearray` is the
mutable version, and `memoryview(b)` is a zero-copy window over a buffer.
Convert text with `"café".encode()` and `b"...".decode()`.

### Collections
`list("abc")`, `tuple(...)`, `set(...)`, `dict(a=1)` build collections from any
iterable. `frozenset` is an immutable (and therefore hashable) set.

### Iteration helpers
```python
for i, item in enumerate(items, start=1): ...
for name, age in zip(names, ages): ...
max(words, key=len)        # compare by length
sorted(people, key=lambda p: p[1])   # returns a NEW list
list(map(str.upper, words)); list(filter(None, values))
```
`all([])` is `True` and `any([])` is `False`. `range(a, b, step)` excludes `b`
and never builds a list. `slice(1, 5, 2)` is a reusable `[1:5:2]`.
`iter(x)` / `next(it, default)` is what `for` does internally; `aiter` / `anext`
are the async versions.

### Objects and introspection
`type(x)` is the exact type (and `type(name, bases, dict)` can create a class);
`isinstance(x, T)` also accepts subclasses - prefer it for type checks.
`dir(x)` lists attribute names, `vars(x)` returns `x.__dict__`, and
`getattr/setattr/hasattr` access attributes by a string name.
`globals()` / `locals()` return the namespace dictionaries. `id(x)` is the
identity number, `callable(x)` tells you whether `x()` would work, and `object`
is the base of every class.

### Class helpers
`@property` makes a method look like an attribute (with optional validation in
a setter). `@classmethod` receives the class (`cls`) - great for alternative
constructors like `from_fahrenheit`. `@staticmethod` receives nothing special.
`super().__init__(...)` calls the parent class's version.

### I/O and the rest
- `print(*args, sep=' ', end='\n', file=...)`.
- `open(path, mode)` - always use it inside `with` so the file closes.
- `input(prompt)` reads a line and **always returns a str**.
- `help(x)` shows documentation; `breakpoint()` opens the debugger.
- `__import__("math")` is the low-level import machinery; use `import` or `importlib`.
- `eval` (one expression) and `exec` (statements) run code from strings. **Avoid them** with any untrusted text; use `ast.literal_eval` or `json.loads` to parse data.

## Common mistakes

- Forgetting that `input()` returns a string: `input() + 1` raises `TypeError`.
- Expecting `sorted()` to change the list (it returns a new one) or `list.sort()` to return it (it returns `None`).
- Using `type(x) == Parent` when you meant `isinstance(x, Parent)`.
- Being surprised that `map`, `filter`, `zip`, `reversed` return one-shot iterators - wrap in `list()` to reuse.
- Calling `max([])` without `default=` -> `ValueError`.
- Naming a variable `list`, `str`, `sum` or `id` - it hides the built-in.
- Expecting `round(2.5)` to give `3`.

## How to run

```
python example_1_numbers_text_bytes.py
python example_2_collections_iteration.py
python example_3_objects_io_introspection.py
```

## Try it yourself

1. Given `scores = {"Ann": 91, "Bob": 78, "Cy": 85}`, print the name with the highest score using `max(..., key=...)`, then print all names sorted by score.
2. Use `enumerate` and `zip` to print `1. Ann - 30`, `2. Bob - 25` from two lists.
3. Write a class `Rectangle` with a read-only `area` `property` and a `classmethod` `square(side)`.
