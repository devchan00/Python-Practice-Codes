"""Lesson 2.7 - Exceptions in depth.

Beyond basic try/except, Python lets you raise your own errors, chain a new
error to the original cause with `raise ... from ...`, catch several types in
one clause, design a custom exception hierarchy for your application, handle
several errors at once with ExceptionGroup and `except*` (Python 3.11+), and
deliberately ignore an expected error with contextlib.suppress. Good error
handling catches only what you can handle and keeps the original cause visible.
"""

import traceback
from contextlib import suppress


# --- 1. raise ---
def withdraw(balance, amount):
    if amount <= 0:
        raise ValueError(f"amount must be positive, got {amount}")
    if amount > balance:
        raise ValueError("insufficient funds")
    return balance - amount


def raising():
    print("--- 1. raise ---")
    print(withdraw(100, 30))            # -> 70
    try:
        withdraw(100, -5)
    except ValueError as e:
        print("ValueError:", e)         # -> ValueError: amount must be positive, got -5
        print(e.args)                   # -> ('amount must be positive, got -5',)

    # A bare `raise` inside except re-raises the SAME exception (after e.g. logging).
    try:
        try:
            1 / 0
        except ZeroDivisionError:
            print("logging it, then re-raising")   # -> logging it, then re-raising
            raise
    except ZeroDivisionError as e:
        print("outer caught:", e)       # -> outer caught: division by zero


# --- 2. Custom exception hierarchy ---
class AppError(Exception):
    """Base class for every error this application raises."""


class ConfigError(AppError):
    """Problem with configuration."""


class ValidationError(AppError):
    """Bad user data. Carries extra information as attributes."""

    def __init__(self, field, message):
        super().__init__(f"{field}: {message}")
        self.field = field


def custom_hierarchy():
    print("\n--- 2. custom exception hierarchy ---")
    for exc in (ConfigError("missing key 'port'"), ValidationError("age", "must be >= 0")):
        try:
            raise exc
        except ValidationError as e:    # most specific first
            print("validation problem in field", e.field, "->", e)
        except AppError as e:           # catches ANY of our errors
            print(type(e).__name__, "->", e)
    # -> ConfigError -> missing key 'port'
    # -> validation problem in field age -> age: must be >= 0

    # WHY: callers can catch AppError to handle "anything from this app"
    # without accidentally swallowing unrelated bugs like TypeError.
    print(issubclass(ConfigError, AppError), issubclass(AppError, Exception))  # -> True True


# --- 3. raise ... from ... (exception chaining) ---
def load_port(settings):
    try:
        return int(settings["port"])
    except KeyError as e:
        raise ConfigError("no port configured") from e
    except ValueError as e:
        raise ConfigError(f"port is not a number: {settings['port']!r}") from e


def chaining():
    print("\n--- 3. raise ... from ... ---")
    print(load_port({"port": "8080"}))  # -> 8080
    try:
        load_port({"port": "eighty"})
    except ConfigError as e:
        print("ConfigError:", e)        # -> ConfigError: port is not a number: 'eighty'
        print("cause:", repr(e.__cause__))
        # -> cause: ValueError("invalid literal for int() with base 10: 'eighty'")

    # The traceback shows BOTH errors, joined by
    # "The above exception was the direct cause of the following exception".
    try:
        load_port({})
    except ConfigError:
        lines = traceback.format_exc().splitlines()
        print([ln for ln in lines if "direct cause" in ln][0])
        # -> The above exception was the direct cause of the following exception:

    # `from None` hides the original when it adds nothing useful.
    try:
        try:
            {}["x"]
        except KeyError:
            raise AppError("lookup failed") from None
    except AppError as e:
        print(e.__cause__, e.__suppress_context__)   # -> None True


# --- 4. Catching several types ---
def parse(value):
    try:
        return 100 / int(value)
    except (ValueError, ZeroDivisionError) as e:      # a tuple of types
        return f"bad input ({type(e).__name__})"
    except TypeError:
        return "wrong type"
    else:
        print("never reached: 'return' already left the try")
    finally:
        pass                                          # always runs (cleanup goes here)


def multi_except():
    print("\n--- 4. except (A, B) as e ---")
    print(parse("4"))                   # -> 25.0
    print(parse("abc"))                 # -> bad input (ValueError)
    print(parse("0"))                   # -> bad input (ZeroDivisionError)
    print(parse(None))                  # -> wrong type


# --- 5. ExceptionGroup and except* (Python 3.11+) ---
def validate_all(records):
    """Check every record and report ALL the problems at once, not just the first."""
    errors = []
    for i, r in enumerate(records):
        if "name" not in r:
            errors.append(KeyError(f"record {i}: missing name"))
        if not isinstance(r.get("age"), int):
            errors.append(TypeError(f"record {i}: age must be int"))
    if errors:
        raise ExceptionGroup("invalid records", errors)


def exception_groups():
    print("\n--- 5. ExceptionGroup / except* ---")
    records = [{"name": "ann", "age": 3}, {"age": "x"}, {"name": "cy", "age": None}]
    try:
        validate_all(records)
    except* KeyError as eg:             # receives a sub-group of just the KeyErrors
        print("key errors:", [str(e) for e in eg.exceptions])
    except* TypeError as eg:            # unlike plain except, SEVERAL except* can run
        print("type errors:", len(eg.exceptions))
    # -> key errors: ["'record 1: missing name'"]   (str() of a KeyError adds quotes)
    # -> type errors: 2

    # You can also inspect a group directly.
    eg = ExceptionGroup("demo", [ValueError(1), OSError(2), ValueError(3)])
    match, rest = eg.split(ValueError)
    print(len(match.exceptions), len(rest.exceptions))   # -> 2 1
    # WHY: concurrent code (asyncio.TaskGroup) and batch validation can fail in
    # several ways at once; a group keeps every error instead of losing all but one.


# --- 6. contextlib.suppress ---
def suppressing():
    print("\n--- 6. contextlib.suppress ---")
    cache = {"a": 1}

    # Equivalent to try: ... except KeyError: pass  - but clearer intent.
    with suppress(KeyError):
        del cache["missing"]            # would raise KeyError
        print("not printed")            # rest of the block is skipped after the error
    print("carried on:", cache)         # -> carried on: {'a': 1}

    with suppress(FileNotFoundError, PermissionError):   # several types are fine
        open("this_file_does_not_exist.txt", encoding="utf-8")
    print("missing file ignored")       # -> missing file ignored
    # Only suppress errors you EXPECT and truly don't care about.


if __name__ == "__main__":
    raising()
    custom_hierarchy()
    chaining()
    multi_except()
    exception_groups()
    suppressing()
