# Mini-project 3 — Generator Pipeline with a Plugin System

The cheatsheet's Advanced practice project: a **pipeline of generators** with a
**plugin system built from decorators**.

Fake web-server log lines are generated in code (no files, no network). They
stream through stages, `parse → skip_static → tag_slow → tag_security`, and
then into a summary report. Each stage is a generator function that registers
itself with `@stage("name")`, so the pipeline is assembled from a plain list of
names. You could just as easily read that list from a config file.

## What you'll learn

- How to structure a lazy, memory-flat data pipeline
- How to build a plugin registry with a decorator factory
- How the Level 3 tools fit together in one small program

## Which lessons it uses

| Lesson | Where it appears |
|---|---|
| 01 Iterators & generators | `generate_log_lines` is an infinite generator; every stage is a generator; `yield from`; `islice` limits the source and peeks at the first 3 records |
| 02 Decorators & closures | `@stage("parse")` is a decorator **with arguments** that registers plugins in `STAGES`; `functools.wraps` |
| 03 Context managers | `@contextmanager timed(...)` measures the run |
| 05 Dataclasses & type hints | `LogRecord(slots=True)`, `Report` with `field(default_factory=...)`, `Callable`/`Iterator` hints |
| 06 Pattern matching | `parse` validates line shape with a sequence pattern, OR, `as` and a guard; `tag_security` uses class patterns |
| 07 Stdlib power tools | `Counter`, `defaultdict`, `islice`, `StrEnum`, `random.Random(seed)` |

## Explanation

### Lazy pipeline
```python
stream = source
for name in ["parse", "skip_static", "tag_slow"]:
    stream = STAGES[name](stream)   # wrap, don't run
```
Building the pipeline does no work. Each `for record in stream` pulls **one**
line through every stage, so 5,000 lines or 5 billion use the same small
amount of memory. The source is infinite, and `islice(source, 5_000)` decides how much
of it gets used.

### Plugin registry
```python
STAGES = {}
def stage(name):
    def decorator(func):
        STAGES[name] = func
        return func
    return decorator

@stage("tag_slow")
def tag_slow(records): ...
```
To add a feature you write a new decorated generator and put its name in the config list.
The pipeline code itself never changes.

### Resilient parsing
`match line.split(): case [ts, ("INFO" | ...) as lvl, ...] if ts.isdigit():`
accepts only well-formed lines. `case _: continue` quietly drops corrupted ones.

## Common mistakes

- Consuming the pipeline twice. Generators are single-use, and in this program `islice(pipeline, 3)`
  *uses up* the first three records, which is why the main loop "continues where it stopped".
- Turning a stage into a list (`list(records)`) inside the pipeline. That throws away the laziness.
- Mutating records in one stage and assuming earlier stages can't see the change. They all share the same objects.

## How to run

```bash
python example.py
```

## Try it yourself

1. Add a `@stage("only_errors")` plugin that keeps `status >= 500`, and put it in the config.
2. Give stages parameters from config, for example `("tag_slow", {"threshold_ms": 300})`.
3. Add a `@stage("window")` that yields per-minute request counts. Hint: use `itertools.groupby`
   on `timestamp // 60`.
