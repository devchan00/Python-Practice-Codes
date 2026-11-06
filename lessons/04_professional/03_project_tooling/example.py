"""Lesson 4.3 - Project tooling: pyproject.toml, packages and requirements.

A modern Python project keeps its metadata, dependencies and tool settings in
one ``pyproject.toml`` file, its code in a ``src/<package>/`` folder, and its
pinned dependencies in ``requirements.txt`` (or a lock file). This script reads
the sample ``pyproject.toml`` with the stdlib ``tomllib`` (3.11+), lists the
skeleton, parses ``requirements.txt`` and runs the sample package with
``python -m myapp``. The tool commands (venv, pip, uv, ruff, mypy, build...)
are explained in README.md - they are shown, not executed.
"""

import os
import subprocess
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent  # works no matter what the cwd is


# --- 1. Read pyproject.toml with tomllib ---
def show_pyproject() -> dict:
    print("\n--- 1. pyproject.toml ---")
    # tomllib needs a BINARY file handle ("rb") - TOML is defined as UTF-8.
    with open(HERE / "pyproject.toml", "rb") as f:
        config = tomllib.load(f)  # -> plain dicts / lists / strings
    project = config["project"]
    print("name:", project["name"])  # -> name: myapp
    print("version:", project["version"])  # -> version: 0.1.0
    print("requires-python:", project["requires-python"])  # -> >=3.11
    print("dependencies:", project["dependencies"])  # -> ['httpx>=0.27']
    print("scripts:", project.get("scripts"))  # -> {'myapp': 'myapp.__main__:main'}
    print("tool sections:", list(config["tool"]))  # -> ['setuptools', 'ruff', 'pytest', 'mypy']
    print("ruff line-length:", config["tool"]["ruff"]["line-length"])  # -> 100
    print("pytest addopts:", config["tool"]["pytest"]["ini_options"]["addopts"])  # -> -q
    return config


def print_tree(config: dict) -> None:
    # --- 2. Pretty-print the whole file as a tree ---
    print("\n--- 2. Full contents as a tree ---")

    def walk(node: object, indent: int = 0) -> None:
        pad = "  " * indent
        if isinstance(node, dict):
            for key, value in node.items():
                if isinstance(value, dict):
                    print(f"{pad}[{key}]")
                    walk(value, indent + 1)
                else:
                    print(f"{pad}{key} = {value!r}")

    walk(config)


# --- 3. The project skeleton ---
def show_layout() -> None:
    print("\n--- 3. Project layout ---")
    for path in sorted(HERE.rglob("*")):
        if "__pycache__" in path.parts:
            continue
        rel = path.relative_to(HERE)
        print("  " * (len(rel.parts) - 1) + rel.name + ("/" if path.is_dir() else ""))
    # The "src layout" means tests import the INSTALLED package, not a stray
    # folder that happens to be next to them - it catches packaging mistakes.


# --- 4. requirements.txt: pinned versions ---
def show_requirements() -> None:
    print("\n--- 4. requirements.txt ---")
    pins = {}
    for line in (HERE / "requirements.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, _, version = line.partition("==")
        pins[name] = version
    print(pins)  # -> {'httpx': '0.27.2', 'anyio': '4.6.2', ...}
    # pyproject's `dependencies` says what you NEED (httpx>=0.27);
    # requirements.txt / a lock file says exactly what you TESTED with.


# --- 5. Run the package: python -m myapp ---
def run_package() -> None:
    print("\n--- 5. python -m myapp ---")
    # Normally you'd `pip install -e .` first. Here we just point PYTHONPATH at
    # src/ for the child process (our own environment is not changed).
    env = {**os.environ, "PYTHONPATH": str(HERE / "src"), "PYTHONDONTWRITEBYTECODE": "1"}
    result = subprocess.run(
        [sys.executable, "-m", "myapp", "Ada"],
        capture_output=True, text=True, env=env, check=True,
    )
    print(result.stdout.strip())  # -> Hello, Ada! (myapp 0.1.0)
    # `python -m pkg` runs pkg/__main__.py. After `pip install .`, the
    # [project.scripts] entry also gives you a plain `myapp` command.


def main() -> None:
    config = show_pyproject()
    print_tree(config)
    show_layout()
    show_requirements()
    run_package()


if __name__ == "__main__":
    main()
