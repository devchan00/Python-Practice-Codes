# Lesson 1: Variables and Core Types

## What you'll learn

- How to create a variable (no declaration needed)
- The four core types: `int`, `float`, `str`, `bool`
- How to check a type with `type()` and `isinstance()`
- How to convert between types: `int('5')`, `str(5)`, `float('2.5')`
- Unpacking (`a, b = 1, 2`) and swapping (`a, b = b, a`)
- What `None` is and why you compare it with `is`
- Comments, docstrings, and naming conventions

## Explanation

### Assigning variables

A variable is a label stuck on a value. `x = 10` means "let the name `x`
refer to the value 10". You don't declare a type first. The type belongs to
the value, so the same name can point at a number now and a string later.
This is called *dynamic typing*.

```python
x = 10
x = "ten"   # allowed: x now refers to a string
```

### The four core types

| Type    | Example   | Meaning                         |
|---------|-----------|---------------------------------|
| `int`   | `30`      | whole number, any size          |
| `float` | `4.99`    | decimal number (approximate)    |
| `str`   | `"Ana"`   | text                            |
| `bool`  | `True`    | `True` or `False` (capitalised) |

Floats are stored in binary, so `0.1 + 0.2` prints `0.30000000000000004`.
That is normal and happens in almost every programming language.

### Inspecting types

`type(x)` tells you the exact class of a value. `isinstance(x, int)` asks
"is `x` an int, *or a subclass of int*?" Use `isinstance` for checks in real
code, because it handles subclasses correctly:

```python
isinstance(True, int)   # True: bool is a subclass of int
type(True) == int       # False: the exact type is bool
isinstance(4.5, (int, float))  # True: a tuple checks several types
```

### Converting between types

Python never guesses. `"5" + 1` raises a `TypeError` because it can't tell
whether you wanted `"51"` or `6`. You say which one you mean:

```python
int("5") + 1     # 6
str(5) + "1"     # "51"
float("2.5")     # 2.5
int(3.99)        # 3, because int() cuts off the decimals
```

`int("five")` raises a `ValueError`, because the text isn't a number.

### Unpacking and swapping

```python
a, b = 1, 2
a, b = b, a      # swap: the right side (2, 1) is built first, then unpacked
```

The number of names on the left must match the number of values on the
right. If it doesn't, Python raises a `ValueError`.

### None

`None` means "nothing" or "no value yet". There is exactly one `None`
object, so the right check is `x is None` (identity), not `x == None`.

### Comments and docstrings

- `# comment`: Python ignores it. Use it to explain *why* the code does something.
- `'''docstring'''`: a triple-quoted string placed first inside a function,
  class, or module. It is stored in `__doc__` and shown by `help()`.

### Naming conventions

| Style        | Used for                 | Example        |
|--------------|--------------------------|----------------|
| `snake_case` | variables, functions     | `item_count`   |
| `PascalCase` | classes                  | `ShoppingCart` |
| `UPPER_CASE` | constants                | `MAX_SPEED`    |

## Common mistakes

- Writing `true`/`false`/`none` in lowercase. They must be `True`, `False`, `None`.
- Adding a string and a number (`"Age: " + 30`). Convert first with
  `str(30)`, or use an f-string.
- Expecting `int(3.99)` to round. It gives `3`. Use `round()` to round.
- Writing `x == None` instead of `x is None`.
- Using `type(x) == int` where `isinstance(x, int)` is what you mean.

## How to run

```bash
python example.py
```

## Try it yourself

1. Create variables for your name, age, and height in metres. Print each
   one together with its `type()`.
2. Start with `a = "3"` and `b = "4"`. Print `a + b`, then convert both and
   print the numeric sum. Explain why the results differ.
3. Swap three variables in one line: start with `x, y, z = 1, 2, 3` and
   end with `x` as 3, `y` as 1, and `z` as 2.
