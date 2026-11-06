# Lesson 3.2 — Decorators & Closures

## What you'll learn

- Functions are ordinary objects: you can store them and pass them around
- Closures: inner functions that remember outer variables (`nonlocal`)
- Writing a `@timer` decorator with `*args, **kwargs`
- Why `functools.wraps` matters
- Decorators that take arguments, such as `@repeat(3)`
- Stacking decorators, and the order they apply in
- The late-binding loop-variable gotcha and two fixes

## Explanation

### Closures
When an inner function uses a variable from its enclosing function, Python keeps
that variable alive inside the inner function (a *closure*).

```python
def make_multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply

double = make_multiplier(2)
double(5)   # 10
```

Reading an outer variable is automatic. To **reassign** it you need `nonlocal count`,
or Python will treat `count` as a new local variable.

### Decorators
A decorator takes a function and returns a replacement function. The `@` line is
just shorthand:

```python
@timer
def slow_add(a, b): ...
# is exactly
slow_add = timer(slow_add)
```

The wrapper should accept `*args, **kwargs` so it works for any signature, and
it must `return` the original result.

### `functools.wraps`
Without it, the decorated function's `__name__` becomes `"wrapper"` and its
docstring disappears. That confuses debugging, `help()` and logging.
`@functools.wraps(func)` copies the metadata across and adds `__wrapped__`, which
points to the original function.

### Decorators with arguments
`@repeat(3)` *calls* `repeat(3)` first. The call must return the real decorator. That gives three
nested levels:

```python
def repeat(times):            # factory: receives the arguments
    def decorator(func):      # decorator: receives the function
        @functools.wraps(func)
        def wrapper(*a, **kw):  # wrapper: receives the call's arguments
            for _ in range(times):
                result = func(*a, **kw)
            return result
        return wrapper
    return decorator
```

### Stacking
Decorators apply from the bottom up: `@a @b def f` means `f = a(b(f))`.

### Late-binding gotcha
`[lambda: i for i in range(3)]` gives three functions that all return `2`.
Closures look up `i` when they are *called*, and by then the loop has
finished. Fix it with `lambda i=i: i` (a default argument is evaluated when the lambda is created) or with
`functools.partial`.

## Common mistakes

- Writing `@timer()` when `timer` takes no arguments, or `@repeat` without
  `(3)` when it does.
- Forgetting to `return result` from the wrapper, so every decorated function returns `None`.
- Leaving out `@functools.wraps`.
- Assigning to an outer variable without `nonlocal`, which raises `UnboundLocalError`.
- The late-binding loop variable in lambdas or callbacks.

## How to run

```bash
python example.py
```

## Try it yourself

1. Write `@retry(times=3, exceptions=(ValueError,))`, which calls the function again
   when it raises one of the listed exceptions.
2. Write `@log_calls`, which prints the function name, its arguments and its return value.
3. Write a `make_accumulator()` closure: `acc(10)` → 10, `acc(5)` → 15.
