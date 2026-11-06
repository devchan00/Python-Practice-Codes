# Lesson 3.3 — Context Managers

## What you'll learn

- What `with` guarantees, and why that matters
- Writing a context manager as a generator with `@contextlib.contextmanager`
  (a `cd()` helper that changes directory and always changes back)
- Writing one as a class with `__enter__` / `__exit__`
- Handling or suppressing exceptions inside `__exit__`
- Useful helpers: `contextlib.suppress`, `ExitStack`, `tempfile.TemporaryDirectory`

## Explanation

### Why `with`?
```python
with open("data.txt") as f:
    data = f.read()
# f is closed here, even if read() raised
```
`with` calls `__enter__()` at the start and `__exit__()` at the end, however the
block ends: normally, by `return`, or by an exception. It replaces fragile
`try/finally` boilerplate.

### `@contextmanager`
Write a generator that yields exactly once. Code before the `yield` is setup, and the
yielded value is what `as` receives. Code after it is cleanup. Put the cleanup in
`finally` so it also runs when the block raises.

```python
@contextlib.contextmanager
def cd(path):
    old = os.getcwd()
    os.chdir(path)
    try:
        yield path
    finally:
        os.chdir(old)
```

### Class form
```python
class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - self.start
        return False
```
Use a class when the manager has meaningful state or methods, or when you want to reuse it.

### Exceptions in `__exit__`
`__exit__(exc_type, exc, tb)` receives details of any exception raised in the
block, or `None, None, None` if there was none. Return `True` to
**swallow** the exception, or `False`/`None` to let it propagate.
`contextlib.suppress(SomeError)` is the ready-made version.

### `ExitStack`
`ExitStack` manages a number of context managers you only know at runtime (for example, opening
N files). They are all closed in reverse order when the stack exits.

## Common mistakes

- Leaving out `try/finally` around `yield`, so cleanup is skipped when the block raises.
- Yielding more than once in a `@contextmanager` generator, which raises `RuntimeError`.
- Returning `True` from `__exit__` by accident, which hides real bugs.
- Forgetting `return self` in `__enter__`, so `as x` gives `None`.
- Using `os.chdir` without restoring it. This causes confusing bugs later, and on Windows
  it stops a temp directory from being deleted.

## How to run

```bash
python example.py
```

## Try it yourself

1. Write `@contextmanager def env_var(name, value)` that sets `os.environ[name]`
   and restores the old value (or deletes it) on exit.
2. Write a class `Transaction` holding a list. Changes made inside the block are
   rolled back if an exception occurs.
3. Use `ExitStack` to open 3 temp files and write the same line to each.
