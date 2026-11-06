"""Mini-project 3 - A log-processing pipeline of generators with plugins.

Fake web-server log lines are generated in code. They flow lazily through a
chain of generator *stages* (parse, filter, enrich...). Stages are plugins:
each one registers itself in a registry with the ``@stage("name")``
decorator, so the pipeline can be assembled from a list of names (e.g. from
a config file) without touching the pipeline code. The final report uses
Counter, defaultdict, dataclasses, pattern matching and a context manager.
"""

import functools
import random
import time
from collections import Counter, defaultdict
from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import StrEnum
from itertools import islice


# --- 1. Data model (lesson 05: dataclasses, StrEnum from lesson 07) --------
class Level(StrEnum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass(slots=True)
class LogRecord:
    timestamp: int
    level: Level
    method: str
    path: str
    status: int
    ms: int
    tags: list[str] = field(default_factory=list)


# --- 2. Sample data: an infinite generator (lesson 01) ----------------------
def generate_log_lines(seed: int = 42) -> Iterator[str]:
    """Yield an endless stream of realistic-looking log lines (plus some junk).
    A fixed seed makes the output reproducible."""
    rng = random.Random(seed)
    paths = ["/", "/login", "/api/items", "/api/items/7", "/static/app.js", "/admin"]
    t = 1_700_000_000
    while True:
        t += rng.randint(1, 5)
        if rng.random() < 0.05:
            yield "### corrupted line ###"         # the parser must survive this
            continue
        status = rng.choices([200, 201, 304, 404, 500], weights=[70, 5, 10, 10, 5])[0]
        level = "ERROR" if status >= 500 else "WARNING" if status >= 400 else "INFO"
        method = "POST" if rng.random() < 0.2 else "GET"
        yield f"{t} {level} {method} {rng.choice(paths)} {status} {rng.randint(5, 900)}ms"


# --- 3. The plugin registry (lesson 02: decorators with arguments) --------
Stage = Callable[[Iterable], Iterator]
STAGES: dict[str, Stage] = {}


def stage(name: str):
    """Decorator factory: @stage("parse") registers the generator function."""
    def decorator(func: Stage) -> Stage:
        if name in STAGES:
            raise ValueError(f"duplicate stage {name!r}")

        @functools.wraps(func)
        def wrapper(items, *args, **kwargs):
            return func(items, *args, **kwargs)
        STAGES[name] = wrapper
        return wrapper
    return decorator


# --- 4. Stages: each one is a generator that consumes a generator ----------
@stage("parse")
def parse(lines: Iterable[str]) -> Iterator[LogRecord]:
    """Turn text into LogRecords. Pattern matching (lesson 06) validates shape."""
    for line in lines:
        match line.split():
            case [ts, ("INFO" | "WARNING" | "ERROR") as lvl, method, path, status, ms] \
                    if ts.isdigit() and ms.endswith("ms"):
                yield LogRecord(int(ts), Level(lvl), method, path, int(status), int(ms[:-2]))
            case _:
                continue          # skip malformed lines instead of crashing


@stage("skip_static")
def skip_static(records: Iterable[LogRecord]) -> Iterator[LogRecord]:
    yield from (r for r in records if not r.path.startswith("/static"))


@stage("tag_slow")
def tag_slow(records: Iterable[LogRecord], threshold_ms: int = 500) -> Iterator[LogRecord]:
    for r in records:
        if r.ms > threshold_ms:
            r.tags.append("slow")
        yield r


@stage("tag_security")
def tag_security(records: Iterable[LogRecord]) -> Iterator[LogRecord]:
    for r in records:
        match r:                                   # class pattern on a dataclass
            case LogRecord(path="/admin" | "/login", status=401 | 403 | 404):
                r.tags.append("suspicious")
            case LogRecord(method="POST", path="/admin"):
                r.tags.append("admin-write")
        yield r


# --- 5. Building & running the pipeline ------------------------------------
def build_pipeline(source: Iterable, stage_names: list[str]) -> Iterator:
    """Wrap the source in each named stage. Nothing runs yet - it's all lazy."""
    stream = source
    for name in stage_names:
        stream = STAGES[name](stream)
    return stream


@contextmanager
def timed(label: str):
    """Lesson 03: a context manager that reports elapsed time."""
    start = time.perf_counter()
    try:
        yield
    finally:
        print(f"[{label}] {time.perf_counter() - start:.3f}s")


@dataclass
class Report:
    total: int = 0
    by_level: Counter = field(default_factory=Counter)
    by_status: Counter = field(default_factory=Counter)
    slowest: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    tagged: Counter = field(default_factory=Counter)

    def add(self, r: LogRecord) -> None:
        self.total += 1
        self.by_level[str(r.level)] += 1
        self.by_status[r.status] += 1
        self.slowest[r.path] = max(self.slowest[r.path], r.ms)
        self.tagged.update(r.tags)

    def print(self) -> None:
        print(f"records processed : {self.total}")
        print(f"by level          : {dict(sorted(self.by_level.items()))}")
        print(f"top statuses      : {self.by_status.most_common(3)}")
        print(f"tags              : {dict(sorted(self.tagged.items()))}")
        worst = max(self.slowest.items(), key=lambda kv: kv[1])
        print(f"slowest path      : {worst[0]} ({worst[1]}ms)")


def main() -> None:
    print("Registered stages:", list(STAGES))
    # -> Registered stages: ['parse', 'skip_static', 'tag_slow', 'tag_security']

    config = ["parse", "skip_static", "tag_slow", "tag_security"]   # plugin order
    # islice limits an INFINITE source; only 5,000 lines are ever created.
    source = islice(generate_log_lines(), 5_000)
    pipeline = build_pipeline(source, config)

    report = Report()
    print("\nFirst 3 records out of the pipeline:")
    for record in islice(pipeline, 3):
        print(" ", record)
        report.add(record)

    with timed("pipeline"):
        for record in pipeline:        # continues where islice stopped
            report.add(record)
    print()
    report.print()


if __name__ == "__main__":
    main()
