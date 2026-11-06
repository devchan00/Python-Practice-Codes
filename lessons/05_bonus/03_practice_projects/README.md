# Bonus 3: Practice projects by level

Reading code teaches you syntax; **building things** teaches you programming.
Pick one project per level, give yourself a deadline, and only look at the
hints when you're stuck. Each level has a finished mini-project in this course
you can study or extend.

## What you'll learn

- How to turn a vague idea into a small, finishable spec
- Which concepts from each level each project exercises
- Where the worked example for each level lives

## Explanation: how to approach any project

1. Write the spec in 3-5 bullet points: inputs, outputs, what "done" means.
2. Build the smallest version that works end to end, then add features.
3. Put logic in functions (or classes) that don't `print` or `input`, so you
   can test them.
4. Commit to git after each working step.

---

## Beginner

Concepts: variables, strings, `if`/loops, lists/dicts, functions, `input()`, `try/except`.
Worked example: [`lessons/01_beginner/08_mini_project_number_guessing`](../../01_beginner/08_mini_project_number_guessing)

### Number-guessing game
- **Spec:** the computer picks 1-100; the player guesses; print "higher"/"lower"
  until correct; show the number of attempts; offer to play again.
- **Hints:** `random.randint(1, 100)`; a `while True` loop with `break`; wrap
  `int(input())` in `try/except ValueError`.

### Unit converter
- **Spec:** convert between km/miles, kg/lb and C/F; menu-driven; reject bad input.
- **Hints:** a dict mapping `("km", "mi")` to a factor or function; note C<->F
  needs a formula, not a factor; round output with `f"{x:.2f}"`.

### CLI to-do list
- **Spec:** `add`, `list`, `done N`, `remove N`, `quit`; numbered output.
- **Hints:** a list of dicts `{"text": ..., "done": False}`; `str.split(maxsplit=1)`
  to separate the command from its argument; `enumerate(todos, start=1)`.

### Text adventure
- **Spec:** 4-5 rooms, move with `north/south/...`, pick up items, one locked
  door that needs a key, a win condition.
- **Hints:** rooms as a dict `{"hall": {"desc": ..., "exits": {"north": "kitchen"}, "items": [...]}}`;
  inventory as a set.

---

## Intermediate

Concepts: comprehensions, modules, files & JSON, classes, exceptions, regex, dates.
Worked example: [`lessons/02_intermediate/09_mini_project_quiz_app`](../../02_intermediate/09_mini_project_quiz_app)

### File organiser
- **Spec:** given a folder, move files into subfolders by extension
  (`images/`, `docs/`, ...); `--dry-run` prints the plan without moving anything.
- **Hints:** `pathlib.Path.iterdir()`, `path.suffix.lower()`, `shutil.move`;
  test it on a `tempfile.TemporaryDirectory()` you fill with dummy files.

### CSV/JSON report generator
- **Spec:** read sales from a CSV; output totals per month and per product as
  JSON and as a printed table.
- **Hints:** `csv.DictReader`, `datetime.strptime`, `collections.defaultdict(float)`,
  `json.dump(..., indent=2)`.

### Web scraper
- **Spec:** extract titles and links from a page; save to CSV.
- **Hints:** start from a saved local `.html` file to avoid hammering a site;
  `html.parser.HTMLParser` (stdlib) or BeautifulSoup; respect `robots.txt`.

### Quiz app with classes
- **Spec:** load questions from JSON; ask in random order; score; save high scores.
- **Hints:** `Question` and `Quiz` classes; keep I/O out of the scoring logic.

---

## Advanced

Concepts: generators, decorators, context managers, dunder methods, dataclasses, typing.
Worked example: [`lessons/03_advanced/08_mini_project_generator_pipeline`](../../03_advanced/08_mini_project_generator_pipeline)

### Plugin system with decorators
- **Spec:** `@register("csv")` adds a function to a registry; the app picks a
  plugin by name at runtime; unknown names give a helpful error.
- **Hints:** a module-level `dict[str, Callable]`; the decorator returns the
  function unchanged; `importlib.import_module` to load plugin modules.

### LRU cache
- **Spec:** `LRUCache(capacity)` with `get`/`put`, evicting the least recently
  used item; then a `@lru(maxsize)` decorator using it.
- **Hints:** `collections.OrderedDict` with `move_to_end` and
  `popitem(last=False)`; compare against `functools.lru_cache`.

### Pipeline of generators
- **Spec:** read a large log file lazily -> parse -> filter errors -> count by
  type, using constant memory.
- **Hints:** each stage is a generator taking an iterable; chain with
  `itertools`; `yield from`.

### Typed library
- **Spec:** a small library (e.g. a money/units type) with full type hints,
  dataclasses and `__eq__`/`__add__`/`__repr__`; passes `mypy --strict`.
- **Hints:** `@dataclass(frozen=True, slots=True)`; return `NotImplemented` for
  unsupported operand types.

---

## Professional

Concepts: concurrency, testing, tooling, logging, performance, security, packaging.
Worked example: [`lessons/04_professional/10_mini_project_async_crawler`](../../04_professional/10_mini_project_async_crawler)

### FastAPI service with tests, CI, Docker
- **Spec:** a CRUD API for to-do items backed by SQLite; pytest tests using
  `TestClient`; GitHub Actions running ruff + mypy + pytest; a `Dockerfile`.
- **Hints:** pydantic models for request/response; inject the DB session as a
  dependency so tests can use an in-memory DB; config from env vars.

### Async crawler
- **Spec:** crawl a site up to depth N with at most K concurrent requests;
  timeouts; skip external links; save results as JSON.
- **Hints:** start from the offline crawler in lesson 4.10; swap `FakeSite` for
  `httpx.AsyncClient`; `urllib.parse.urljoin` for relative links; be polite (rate limit).

### Packaged CLI on PyPI
- **Spec:** a useful CLI (e.g. the file organiser) installable with `pipx install yourtool`.
- **Hints:** `src/` layout + `pyproject.toml` with `[project.scripts]` (lesson 4.3);
  `python -m build`; upload to **TestPyPI** first with `twine upload -r testpypi dist/*`.

---

## Common mistakes

- Picking a project too big to finish - scope down until it fits a weekend.
- Mixing `input()`/`print()` into core logic, which makes it untestable.
- Never reading other people's code - compare your solution with the worked examples.
- Skipping tests "because it's just practice" - practice testing too.

## How to run

This folder is README-only. Run the worked examples from their folders, e.g.:

```bash
cd lessons/04_professional/10_mini_project_async_crawler
python example.py
```

## Try it yourself

1. Pick one Beginner project and finish it today, in under 100 lines.
2. Take your Beginner project and "level it up": add classes and JSON save
   files (Intermediate), then type hints and tests (Advanced/Professional).
3. Extend the async crawler worked example with one of its README exercises.
