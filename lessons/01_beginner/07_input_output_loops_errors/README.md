# Lesson 7: Input/Output, Loop Helpers, and Errors

## What you'll learn

- `print()` with `sep=` and `end=`
- `input()`, and why it always returns a `str`
- `range(stop)` and `range(start, stop, step)`
- `enumerate(lst, 1)` for numbered loops
- Looping over a dict with `for k, v in d.items():`
- Handling errors with `try` / `except` / `else` / `finally`
- The common built-in exceptions: `ValueError`, `TypeError`, `KeyError`,
  `IndexError`, `AttributeError`, `ZeroDivisionError`, `FileNotFoundError`,
  `ImportError`

## Explanation

### print: sep and end

```python
print(a, b)                     # apples pears   (separated by a space)
print(a, b, sep=', ', end='')   # apples, pears  (and no newline afterwards)
```

`sep` is placed **between** the values (the default is a space). `end` is
placed **after** the last value (the default is `"\n"`, a newline). Setting
`end=""` or `end=" "` lets the next `print` continue on the same line.

### input

`input('Age? ')` shows the prompt, waits for the user to press Enter, and
returns what they typed as a **string**, even when they typed digits. Convert
it yourself with `int(...)` or `float(...)`, and clean it with `.strip()`.

The example file doesn't call `input()`, so it can run unattended. It uses
hard-coded strings instead, with the real call in a comment:

```python
age_text = "42"   # pretend this came from input('Age? ')
```

### range

| Call               | Produces          |
|--------------------|-------------------|
| `range(5)`         | 0, 1, 2, 3, 4     |
| `range(2, 10, 2)`  | 2, 4, 6, 8        |
| `range(5, 0, -1)`  | 5, 4, 3, 2, 1     |

The stop value is never included. `range` is *lazy*: it produces the numbers
one at a time instead of storing them all.

### enumerate and dict loops

```python
for number, item in enumerate(lst, 1):   # (1, 'eggs'), (2, 'milk'), ...
    print(f"{number}. {item}")

for k, v in d.items():                   # key and value together
    print(k, v)
```

`enumerate` saves you from managing a counter variable by hand. Looping over
a dict directly (`for k in d`) gives you only the keys.

### try / except / else / finally

```python
try:
    n = int(input("n: "))
except ValueError as e:
    print("Not a number:", e)   # runs if that error happened
else:
    print("ok")                 # runs only if there was NO error
finally:
    print("done")               # always runs, error or not
```

- Keep the `try` block small, so you know exactly which line you're guarding.
- `as e` gives you the exception object, and printing it shows the message.
- `else` holds code that should run only when the `try` succeeded.
- `finally` is for clean-up that must always happen.

### Common exceptions

| Exception           | Typical cause                          |
|---------------------|----------------------------------------|
| `ValueError`        | right type, bad value: `int("x")`      |
| `TypeError`         | wrong type: `"a" + 1`                  |
| `KeyError`          | missing dict key: `d["nope"]`          |
| `IndexError`        | list index out of range: `[1, 2][5]`   |
| `AttributeError`    | missing attribute: `(5).upper()`       |
| `ZeroDivisionError` | `1 / 0`                                |
| `FileNotFoundError` | `open("missing.txt")`                  |
| `ImportError`       | `import no_such_module` (raised as its subclass `ModuleNotFoundError`) |

## Common mistakes

- Doing maths on `input()` without converting it first. `"4" + "2"` is `"42"`.
- A bare `except:` that silently hides every error, including typos in your
  code. Catch specific exceptions.
- Putting too much code inside `try`, which makes it unclear what failed.
- Expecting `range(1, 10)` to include 10.
- Forgetting `.items()`, so `for k, v in d:` raises an unpacking error.

## How to run

```bash
python example.py
```

## Try it yourself

1. Print the numbers 10, 8, 6, 4, 2 on a single line, separated by `" | "`,
   using `range` and `print(..., end=...)`.
2. Write `safe_divide(a, b)` that returns `a / b`, or prints a friendly
   message and returns `None` on `ZeroDivisionError`. Add a `finally` that
   prints `"division attempted"`.
3. Turn the fake-answers loop in section 6 into a real program with
   `input()`. Keep asking until the user enters a whole number between 1
   and 10.
