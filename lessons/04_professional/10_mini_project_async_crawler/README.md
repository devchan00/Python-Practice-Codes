# 4.10 Mini project: async crawler (offline)

The cheatsheet's professional practice project is an "async crawler". This
version crawls a **fake in-memory website**, so it runs anywhere with no
network, but it has the same structure as a real one.

## What you'll learn

- Structuring a small async program: model, fetcher, crawler, entry point
- `asyncio.TaskGroup` to fetch a whole level of links concurrently
- `asyncio.Semaphore` to cap how many requests are in flight
- `asyncio.timeout` for slow pages, and recording errors instead of crashing
- Breadth-first search with a `seen` set (O(1) de-duplication) and a depth limit
- Logging, type hints, dataclasses and dependency injection working together
- Testing async code with `unittest.IsolatedAsyncioTestCase`

## Files

| File | Role |
|---|---|
| `crawler.py` | `FakeSite` (simulated server), `Page`, `CrawlResult`, `Crawler` |
| `example.py` | Runs the crawl twice (3 concurrent vs 1) and prints a report |
| `test_crawler.py` | 7 unittest tests |

## Explanation

### The fake site

`FakeSite.fetch(url)` awaits `asyncio.sleep(random latency)` - standing in for
the network - then returns a `Page(url, title, links)` or raises
`PageNotFound`. `/missing` is a broken link and `/slow` takes 1 s, longer than
the crawler's timeout. It also tracks `peak`, the most fetches running at once,
so we can *prove* the concurrency limit works.

### The crawl loop (breadth-first)

```python
seen = {start}
frontier = [start]
while frontier and depth <= max_depth:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(self._fetch_one(u, result)) for u in frontier]
    frontier = [link for t in tasks for link in t.result() if link not in seen]  # (+ add to seen)
```

Every URL on a level is fetched concurrently; new links form the next level.

### Limiting concurrency

```python
async with self.semaphore:          # Semaphore(3): at most 3 inside
    async with asyncio.timeout(self.timeout):
        page = await self.site.fetch(url)
```

Without a limit, a real crawler would open hundreds of connections at once and
get blocked (or overload the server). Being polite is part of correctness.

### Errors are data

`_fetch_one` catches `TimeoutError` and `PageNotFound`, logs a warning, and
stores the reason in `result.errors`. One bad page must not stop the crawl -
and since the errors are caught inside each task, the `TaskGroup` never
cancels the others.

### Dependency injection and tests

`Crawler(site, ...)` receives its site, so tests pass a tiny predictable graph
with ~1 ms latency. To crawl the real web you'd write a class with the same
`fetch` method using `httpx.AsyncClient` and an HTML parser.

## Common mistakes

- Forgetting the `seen` set: pages that link to each other loop forever.
- Calling `time.sleep` or `requests.get` inside async code - it blocks every task.
- No timeout: one hung server stalls the whole crawl.
- Letting one exception escape a `TaskGroup` task, which cancels all the others.
- Using `print` for progress instead of logging (can't be silenced or filtered).

## How to run

```bash
cd lessons/04_professional/10_mini_project_async_crawler
python example.py
python -m unittest -v
```

## Try it yourself

1. Add retries: on timeout, try again up to 2 times with a short back-off
   (`await asyncio.sleep(0.05 * attempt)`), and add a test for it.
2. The level-by-level design waits for the slowest page on each level. Rewrite
   `crawl` with an `asyncio.Queue` and N worker tasks so new links start
   immediately. Compare the total time.
3. Add `allowed_prefix="/blog"` so the crawler only follows links under that path.
