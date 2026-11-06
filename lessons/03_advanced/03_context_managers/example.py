"""Lesson 3.3 - Context managers.

A context manager is any object used with ``with``. It runs setup code on the
way in (``__enter__``) and is *guaranteed* to run cleanup code on the way out
(``__exit__``), even if the block raises an exception or returns early. That
is why files, locks, database transactions and temporary directories are all
used with ``with``. You can write one as a class or, more briefly, as a
generator decorated with ``@contextlib.contextmanager``.
"""

import contextlib
import os
import tempfile
import time


# --- 1. The built-in example: files ----------------------------------------
def demo_files():
    print("--- 1. with open(...) ---")
    with tempfile.TemporaryDirectory() as tmp:     # also a context manager!
        path = os.path.join(tmp, "note.txt")
        with open(path, "w") as f:
            f.write("hello")
        print(f.closed)                # -> True  (closed automatically)
        with open(path) as f:
            print(f.read())            # -> hello
    print(os.path.exists(tmp))         # -> False (temp dir deleted on exit)


# --- 2. @contextmanager: the cd() example ----------------------------------
@contextlib.contextmanager
def cd(path):
    """Temporarily change directory, and always change back."""
    old = os.getcwd()
    os.chdir(path)                     # code before yield  == __enter__
    try:
        yield path                     # value bound by `as`; the with-block runs here
    finally:
        os.chdir(old)                  # code after yield == __exit__ (always runs)


def demo_cd():
    print("\n--- 2. @contextmanager cd() ---")
    start = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        with cd(tmp):
            open("inside.txt", "w").close()        # relative path -> inside tmp
            print(os.listdir("."))                 # -> ['inside.txt']
            print(os.path.samefile(os.getcwd(), tmp))  # -> True
        print(os.getcwd() == start)    # -> True (we are back)

        # Even if the block blows up, the finally clause restores the cwd:
        try:
            with cd(tmp):
                raise RuntimeError("boom")
        except RuntimeError:
            pass
        print(os.getcwd() == start)    # -> True
        # NB: we must leave tmp before TemporaryDirectory deletes it (Windows
        # refuses to delete the current directory) - cd() guarantees that.


# --- 3. Class form: __enter__ / __exit__ -----------------------------------
class Timer:
    """Measure how long a block takes."""

    def __enter__(self):
        self.start = time.perf_counter()
        return self                    # this is what `as t` receives

    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - self.start
        print(f"block took {self.elapsed:.3f}s")
        return False                   # False/None: don't swallow exceptions


def demo_class_form():
    print("\n--- 3. Class-based context manager ---")
    with Timer() as t:
        time.sleep(0.02)
    print(t.elapsed > 0.01)            # -> True (t is still usable afterwards)


# --- 4. Exception handling in __exit__ -------------------------------------
class Suppress:
    """Swallow the listed exception types (like contextlib.suppress).
    __exit__ receives (type, value, traceback) or (None, None, None).
    Returning True tells Python 'handled - don't re-raise'."""

    def __init__(self, *types):
        self.types = types

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            print("  no exception")
            return False
        if issubclass(exc_type, self.types):
            print(f"  suppressed {exc_type.__name__}: {exc}")
            return True                # swallow it
        print(f"  letting {exc_type.__name__} propagate")
        return False                   # re-raise


def demo_exit_exceptions():
    print("\n--- 4. Exceptions in __exit__ ---")
    with Suppress(KeyError):
        pass                           # ->   no exception
    with Suppress(KeyError):
        {}["missing"]                  # ->   suppressed KeyError: 'missing'
    print("still running")             # -> still running
    try:
        with Suppress(KeyError):
            1 / 0                      # ->   letting ZeroDivisionError propagate
    except ZeroDivisionError:
        print("caught outside")        # -> caught outside


# --- 5. Handy contextlib helpers -------------------------------------------
@contextlib.contextmanager
def tag(name):
    print(f"<{name}>")
    yield
    print(f"</{name}>")


def demo_contextlib_helpers():
    print("\n--- 5. contextlib helpers ---")
    with contextlib.suppress(FileNotFoundError):   # built-in Suppress
        os.remove("this-file-does-not-exist.xyz")
    print("suppress ok")               # -> suppress ok

    with tag("ul"), tag("li"):         # several managers on one line
        print("item")                  # -> <ul> <li> item </li> </ul>

    with contextlib.ExitStack() as stack:   # a dynamic number of managers
        dirs = [stack.enter_context(tempfile.TemporaryDirectory()) for _ in range(3)]
        print(len(dirs), all(os.path.isdir(d) for d in dirs))  # -> 3 True
    print(any(os.path.exists(d) for d in dirs))  # -> False (all cleaned up)


if __name__ == "__main__":
    demo_files()
    demo_cd()
    demo_class_form()
    demo_exit_exceptions()
    demo_contextlib_helpers()
