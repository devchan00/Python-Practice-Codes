# The 35 Reserved Keywords

Reserved keywords are words Python itself owns. You cannot use them as variable,
function or class names (`class = 3` is a `SyntaxError`). There are exactly 35 of
them, and you can always see the list with:

```python
import keyword
print(keyword.kwlist)   # 35 names
```

## What you'll learn

- The value keywords `True`, `False`, `None` and what "truthy/falsy" means
- Logic and tests: `and`, `or`, `not`, `is`, `in` (including short-circuiting)
- Control flow: `if`, `elif`, `else`, `for`, `while`, `break`, `continue`, `pass`, `del`
- Functions and scope: `def`, `return`, `lambda`, `global`, `nonlocal`
- Classes: `class`
- Exceptions: `try`, `except`, `else`, `finally`, `raise`, `assert`
- Modules: `import`, `from`, `as`
- Context managers: `with`
- Generators and async: `yield`, `yield from`, `async`, `await`, `async with`, `async for`

## Files

| File | Keywords covered |
|------|------------------|
| `example_1_values_logic_control.py` | True False None and or not is in if elif else for while break continue pass del |
| `example_2_functions_classes_errors.py` | def return lambda global nonlocal class try except else finally raise assert import from as with |
| `example_3_generators_async.py` | yield (yield from) async await (async with / async for) |

## Explanation

### Values: `True`, `False`, `None`
`True` and `False` are the two booleans (they are actually the ints 1 and 0).
`None` means "no value" and there is only one `None` object, so test it with
`is`: `if x is None: ...`. In an `if`, these values count as false ("falsy"):
`False`, `None`, `0`, `0.0`, `''`, `[]`, `{}`, `set()`. Everything else is truthy.

### Logic: `and`, `or`, `not`
`and` stops at the first falsy operand, `or` stops at the first truthy one, and
both return **that operand**, not necessarily `True`/`False`:

```python
name = user_input or "default"   # fallback idiom
0 and 99    # -> 0
```
`not` flips truthiness: `if not items:` means "if the list is empty".

### Tests: `is`, `in`
`in` checks membership (`'a' in 'cat'`, `key in my_dict`). `is` checks
**identity** (the very same object), while `==` checks **equal value**. Two
separate lists `[1, 2]` are `==` but not `is`.

### Control flow
- `if` / `elif` / `else` choose a branch. `elif` is only checked when earlier conditions were false.
- `for` iterates over any iterable; `while` repeats while a condition is truthy.
- `break` leaves the loop; `continue` jumps to the next iteration.
- `else` after a loop runs only if the loop **did not** `break` - perfect for "not found".
- `pass` does nothing; it fills a block that must not be empty (`class Stub: pass`).
- `del` removes a name, list item, slice or dict key: `del d['key']`, `del nums[1:3]`.

### Functions and scope
`def` defines a function, `return` exits it and sends a value back (no `return`
means it returns `None`). `lambda x: x * 2` is a one-expression anonymous
function, mostly used as a short argument (`sorted(words, key=lambda w: len(w))`).
`global counter` lets a function rebind a module-level variable; `nonlocal total`
rebinds a variable of the enclosing function (used in closures).

### Classes
`class Dog(Animal): ...` defines a blueprint for objects; the name in brackets is
the parent class it inherits from.

### Exceptions
```python
try:
    value = int(text)
except ValueError as e:   # only if that error happened
    ...
else:                     # only if NO error happened
    ...
finally:                  # always, for cleanup
    ...
```
`raise ValueError('bad')` throws an error; a bare `raise` inside `except`
re-throws the current one; `raise X from e` chains errors. `assert n > 0, 'msg'`
raises `AssertionError` when the condition is false - for debugging and tests.

### Imports: `import`, `from`, `as`
`import json` loads a module; `from os import path` takes one name out of it;
`import numpy as np` gives an alias. `from` has two other jobs: `raise ... from ...`
and `yield from ...`. `as` also appears in `except E as e` and `with ... as f`.

### `with`
`with open(p) as f:` runs a context manager: setup on entry, guaranteed cleanup
on exit (the file is closed even if an error occurs).

### Generators and async
`yield` turns a function into a generator that produces values lazily, one per
`next()` call. `yield from it` hands out every item of another iterable.
`async def` declares a coroutine; `await` pauses it until another awaitable
finishes so other tasks can run. `async with` and `async for` are the async
versions of `with` and `for`.

## Common mistakes

- Writing `if x == None` instead of `if x is None`.
- Using `is` to compare numbers or strings (`a is 1000`) - use `==`.
- Forgetting that `or` returns an operand: `0 or "default"` gives `"default"` even when 0 was a valid value.
- Modifying a global inside a function without `global` -> `UnboundLocalError`.
- Using `assert` to validate user input - asserts disappear with `python -O`.
- A bare `except:` that swallows every error, including typos - catch specific exceptions.
- Thinking loop-`else` means "if the loop didn't run" - it means "if it didn't `break`".
- Calling a coroutine without `await` - you get a coroutine object, nothing runs.

## How to run

```
python example_1_values_logic_control.py
python example_2_functions_classes_errors.py
python example_3_generators_async.py
```

## Try it yourself

1. Write `find_index(items, target)` using `for ... else` that prints "not found" when the target is missing.
2. Write a generator `evens(limit)` with `yield` that produces even numbers below `limit`, then print `list(evens(10))`.
3. Write `safe_divide(a, b)` with `try/except/else/finally` that returns `None` on `ZeroDivisionError` and always prints "done".
