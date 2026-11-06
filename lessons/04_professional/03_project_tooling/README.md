# 4.3 Project tooling

## What you'll learn

- Virtual environments (`python -m venv`) and why every project needs one
- `pip install`, `pip install -r requirements.txt`, `pip freeze`
- Modern managers: **uv**, **poetry**, **pipx**
- `pyproject.toml`: one file for metadata, dependencies and tool settings
- Linters / formatters: **ruff**, **black**, **isort**
- Type checkers: **mypy**, **pyright**
- **pre-commit** hooks
- Building and publishing: `python -m build`, `twine upload`

## Files in this folder

```
03_project_tooling/
  pyproject.toml            project metadata + tool config (matches the cheatsheet)
  requirements.txt          pinned dependency versions
  .pre-commit-config.yaml   hooks that run before each commit
  src/myapp/__init__.py     the package
  src/myapp/__main__.py     lets you run `python -m myapp`
  example.py                reads pyproject.toml with tomllib and prints it
```

## Explanation

The commands below are for reading and trying in your own project. `example.py`
does **not** run them (they would install things or touch the network).

### Virtual environments

```bash
python -m venv .venv               # create an isolated environment
.venv\Scripts\activate             # Windows (PowerShell / cmd)
source .venv/bin/activate          # macOS / Linux / Git Bash: source .venv/Scripts/activate
deactivate                         # leave it
```

Each project gets its own folder of installed packages, so project A can use
`httpx 0.27` while project B uses `httpx 0.24`. Never commit `.venv/`.

### pip

```bash
pip install httpx                  # install one package
pip install -r requirements.txt    # install a pinned list
pip freeze > requirements.txt      # record exactly what is installed now
pip install -e .                   # install YOUR project in editable mode
pip install -e ".[dev]"            # ...plus the optional "dev" extras
```

`pyproject.toml` lists what you *need* (`httpx>=0.27`); `requirements.txt`
(or a lock file) records exactly what you *tested with* (`httpx==0.27.2`).

### uv, poetry, pipx

```bash
uv venv && uv pip install -r requirements.txt   # very fast pip/venv replacement
uv add httpx          # add a dependency to pyproject.toml + uv.lock
uv run pytest         # run inside the project env
poetry new myapp ; poetry add httpx ; poetry install   # all-in-one project manager
pipx install ruff     # install a CLI TOOL globally, each in its own venv
```

### pyproject.toml

```toml
[project]
name = "myapp"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["httpx>=0.27"]

[tool.ruff]
line-length = 100

[tool.pytest.ini_options]
addopts = "-q"
```

Tools read their own `[tool.<name>]` table, so you don't need `setup.cfg`,
`.isort.cfg`, `pytest.ini` and friends. Read it in Python with:

```python
import tomllib
with open("pyproject.toml", "rb") as f:
    config = tomllib.load(f)
```

### Lint and format

```bash
ruff check .          # find bugs and style problems (fast; replaces flake8 + isort)
ruff check --fix .    # auto-fix what it can
ruff format .         # format code (black-compatible)
black .               # the classic formatter
isort .               # sort imports
```

Automatic formatting ends style arguments in code review.

### Type checking

```bash
mypy src              # check type hints statically
pyright src           # Microsoft's checker (also powers VS Code's Pylance)
```

Hints are **not** enforced when the program runs; these tools check them
before it runs, ideally in CI.

### pre-commit

```bash
pip install pre-commit
pre-commit install            # hook into git
pre-commit run --all-files    # run every hook now
```

Then each `git commit` runs ruff / mypy etc. first, and stops the commit if
they fail.

### Build and publish

```bash
pip install build twine
python -m build               # makes dist/myapp-0.1.0.tar.gz and .whl
twine upload dist/*           # publish to PyPI (try --repository testpypi first)
```

### src layout and `python -m`

Putting code in `src/myapp/` means tests run against the *installed* package,
which catches packaging mistakes. `__main__.py` makes `python -m myapp` work,
and `[project.scripts]` gives a `myapp` command after installing.

## Common mistakes

- Installing packages globally instead of in a venv (`pip` from the wrong Python).
  Use `python -m pip ...` to be sure it matches `python`.
- Committing `.venv/` or `dist/` to git.
- Hand-editing `requirements.txt` and forgetting to re-freeze.
- Opening the TOML file in text mode: `tomllib.load` needs `"rb"`.
- Thinking type hints are checked at runtime - run mypy/pyright.

## How to run

```bash
cd lessons/04_professional/03_project_tooling
python example.py
```

## Try it yourself

1. Add a `[tool.black]` table with `line-length = 100` and make `example.py` print it.
2. Create a venv in a scratch folder, `pip install -e .` this project there,
   and run the `myapp` command.
3. Add a `farewell(name)` function to `myapp` and a `--bye` flag to `__main__.py`.
