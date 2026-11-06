"""Lesson 4.7 - Design and best practices.

Good Python code is readable first. PEP 8 is the style guide and PEP 20 (the
Zen of Python, ``import this``) is the philosophy. This lesson shows EAFP
("easier to ask forgiveness than permission") vs LBYL ("look before you
leap"), composition over inheritance, type hints with docstrings on public
APIs, dependency injection for testable code, and 12-factor configuration read
from environment variables with sensible defaults (never hard-coded secrets).
"""

import contextlib
import io
import os
from dataclasses import dataclass
from collections.abc import Mapping
from typing import Protocol


# --- 1. PEP 20: the Zen of Python ---
def demo_zen() -> None:
    print("\n--- 1. PEP 20: import this ---")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):  # `import this` prints on import
        import this  # noqa: F401
    lines = buf.getvalue().splitlines()
    for line in lines[:8]:
        print(" ", line)
    print(f"  ... ({len(lines)} lines in total)")
    # -> Beautiful is better than ugly. / Explicit is better than implicit. ...

    # PEP 8 in a nutshell: 4-space indents, snake_case functions/variables,
    # PascalCase classes, UPPER_CASE constants, ~79-100 char lines, imports at
    # the top (stdlib, third-party, local). Let ruff/black enforce it for you.
    MAX_RETRIES = 3  # constant
    user_name = "ada"  # variable
    print("PEP 8 names:", MAX_RETRIES, user_name)


# --- 2. EAFP vs LBYL ---
def demo_eafp() -> None:
    print("\n--- 2. EAFP vs LBYL ---")
    config = {"port": "8080"}

    # LBYL: check first. Verbose, and racy for files (it can vanish between
    # the check and the use).
    if "port" in config and config["port"].isdigit():
        port = int(config["port"])
    else:
        port = 80
    print("LBYL port:", port)  # -> 8080

    # EAFP: just try it; handle the specific failure. The Pythonic default.
    try:
        timeout = int(config["timeout"])
    except (KeyError, ValueError):
        timeout = 30
    print("EAFP timeout:", timeout)  # -> 30

    # EAFP with files: no os.path.exists() check needed.
    try:
        with open("definitely-missing-file.txt", encoding="utf-8") as f:
            f.read()
    except FileNotFoundError:
        print("EAFP: file missing, using defaults")


# --- 3. Composition over inheritance ---
class Engine:
    def start(self) -> str:
        return "vroom"


class ElectricMotor:
    def start(self) -> str:
        return "hum"


class Car:
    """A Car HAS an engine (composition) rather than IS an engine (inheritance)."""

    def __init__(self, engine: Engine | ElectricMotor) -> None:
        self.engine = engine

    def drive(self) -> str:
        return f"{self.engine.start()} - driving"


def demo_composition() -> None:
    print("\n--- 3. Composition over inheritance ---")
    print(Car(Engine()).drive())  # -> vroom - driving
    print(Car(ElectricMotor()).drive())  # -> hum - driving
    # Swapping parts is easy; with inheritance we'd need GasCar, ElectricCar,
    # HybridCar... and deep hierarchies that are hard to change.


# --- 4. Type hints + docstrings on public APIs ---
def mean(values: list[float], *, default: float | None = None) -> float:
    """Return the arithmetic mean of ``values``.

    Args:
        values: Numbers to average.
        default: Returned when ``values`` is empty. If None, raise instead.

    Returns:
        The mean as a float.

    Raises:
        ValueError: If ``values`` is empty and no default is given.
    """
    if not values:
        if default is None:
            raise ValueError("mean of empty list")
        return default
    return sum(values) / len(values)


def demo_hints() -> None:
    print("\n--- 4. Type hints + docstrings ---")
    print(mean([1, 2, 3, 4]))  # -> 2.5
    print(mean([], default=0.0))  # -> 0.0
    print("hints:", mean.__annotations__)  # tools (mypy, IDEs) read these
    print("doc first line:", mean.__doc__.splitlines()[0])  # help(mean) shows it
    # Google style shown above; NumPy and reST styles are also common.
    # Hints are NOT checked at runtime: mean(["a"]) would only fail inside sum().
    # pydantic (pip install pydantic) adds runtime validation from hints:
    #   class User(BaseModel):
    #       name: str
    #       age: int
    #   User(name="Ada", age="36")   # -> age coerced to 36
    #   User(name="Ada", age="old")  # -> ValidationError


# --- 5. Dependency injection ---
class Notifier(Protocol):
    def send(self, to: str, msg: str) -> None: ...


class EmailNotifier:
    def send(self, to: str, msg: str) -> None:
        print(f"  [would send a real email to {to}]: {msg}")


class FakeNotifier:
    """A test double: records messages instead of sending them."""

    def __init__(self) -> None:
        self.sent: list[tuple[str, str]] = []

    def send(self, to: str, msg: str) -> None:
        self.sent.append((to, msg))


class SignupService:
    # The collaborator is PASSED IN, not created inside (no EmailNotifier() here).
    def __init__(self, notifier: Notifier) -> None:
        self.notifier = notifier

    def register(self, email: str) -> None:
        self.notifier.send(email, "Welcome!")


def demo_di() -> None:
    print("\n--- 5. Dependency injection ---")
    SignupService(EmailNotifier()).register("ada@example.com")  # production
    fake = FakeNotifier()
    SignupService(fake).register("bob@example.com")  # test: no email sent
    print("fake recorded:", fake.sent)  # -> [('bob@example.com', 'Welcome!')]


# --- 6. 12-factor config: environment variables with defaults ---
@dataclass(frozen=True)
class Settings:
    debug: bool
    port: int
    db_url: str
    api_key: str | None  # secrets come from the environment, never the code


def load_settings(env: Mapping[str, str] = os.environ) -> Settings:
    return Settings(
        debug=env.get("APP_DEBUG", "false").lower() in {"1", "true", "yes"},
        port=int(env.get("APP_PORT", "8000")),
        db_url=env.get("APP_DB_URL", "sqlite:///dev.db"),
        api_key=env.get("APP_API_KEY"),  # None if missing: fail loudly where used
    )


def demo_config() -> None:
    print("\n--- 6. 12-factor config ---")
    print("defaults:", load_settings({}))
    # -> Settings(debug=False, port=8000, db_url='sqlite:///dev.db', api_key=None)
    prod_env = {"APP_DEBUG": "0", "APP_PORT": "443", "APP_API_KEY": "s3cr3t"}
    s = load_settings(prod_env)  # injecting the env dict also makes this testable
    print("prod:", s.port, s.debug, "key set:", s.api_key is not None)  # -> 443 False key set: True
    print("from real os.environ:", load_settings().port)  # -> 8000 unless APP_PORT is set
    # Set in a shell:  APP_PORT=9000 python example.py   (PowerShell: $env:APP_PORT=9000)


def main() -> None:
    demo_zen()
    demo_eafp()
    demo_composition()
    demo_hints()
    demo_di()
    demo_config()


if __name__ == "__main__":
    main()
