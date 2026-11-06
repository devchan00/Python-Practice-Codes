# Lesson 6: Functions

## What you'll learn

- Defining a function with `def`, and documenting it with a docstring
- Calling it with positional and keyword arguments
- Default parameter values
- `return`, returning several values, and why "no return" means `None`
- Local variables, and how functions can be passed around as values
- **The mutable-default trap**: never use `[]` or `{}` as a default

## Explanation

### Defining and calling

```python
def greet(name, greeting="Hello"):
    """Return a greeting string."""
    return f"{greeting}, {name}!"

greet("Ana")                       # positional: "Hello, Ana!"
greet(greeting="Hi", name="Bo")    # keyword arguments: "Hi, Bo!"
```

- `name` and `greeting` are **parameters**. The values you pass in are
  **arguments**.
- *Positional* arguments are matched by their order. *Keyword* arguments are
  matched by name, so their order doesn't matter, and they make calls easier
  to read.
- The triple-quoted string on the first line is the **docstring**. It's
  shown by `help(greet)`.

### Default values

`greeting="Hello"` means "use `"Hello"` when the caller doesn't pass one".
Parameters with defaults must come after the ones without defaults.

### return and None

`return` sends a value back to the caller and **ends the function**
immediately. A function that never reaches a `return` gives back `None`.
Printing a value is not the same as returning it: printed output can't be
stored in a variable.

To return several values, separate them with commas. Python packs them into
a tuple, which you can unpack:

```python
low, high = min_max([4, 9, 1, 7])
```

### Local scope

A variable created inside a function is *local*: it exists only while the
function runs, and it doesn't change a global variable with the same name.
That keeps functions independent of one another. The intermediate lesson
covers `global` and `nonlocal`.

### Functions are values

A function name without brackets refers to the function object itself, so
you can store it in a variable or pass it to another function
(`apply_twice(power, 3)`).

### The mutable-default trap

Default values are evaluated **once, when `def` runs**, not each time the
function is called. A list default is a single list shared by every call:

```python
def add_item(item, basket=[]):     # BUG
    basket.append(item)
    return basket

add_item("apple")   # ['apple']
add_item("pear")    # ['apple', 'pear']  <- the same list again!
```

The fix is to use `None` as the default and create the list inside:

```python
def add_item(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket
```

## Common mistakes

- Using `[]`, `{}`, or `set()` as a default value.
- Calling `print()` inside a function and expecting the caller to receive
  the value. Use `return`.
- Forgetting the brackets when calling: `greet` refers to the function,
  while `greet()` calls it.
- Putting a parameter that has a default before one that doesn't.
- Code after a `return` in the same block never runs.

## How to run

```bash
python example.py
```

## Try it yourself

1. Write `celsius_to_fahrenheit(c)` that returns `c * 9 / 5 + 32`, plus a
   docstring. Call it with `0`, `100`, and `-40`.
2. Write `describe_pet(name, kind="dog")` and call it in three ways:
   positionally, with keywords in a different order, and using the default.
3. Write `stats(numbers)` that returns the count, sum, and average as three
   values, then unpack them in one line.
