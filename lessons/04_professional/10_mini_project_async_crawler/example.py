"""Lesson 4.10 - Mini project: an async crawler (no network).

This brings the professional level together: ``asyncio`` with ``TaskGroup``,
a ``Semaphore`` concurrency limit and ``asyncio.timeout``; logging instead of
print for progress; type hints and dataclasses; dependency injection (the
crawler is given its site, so tests can pass a fake); and a ``unittest`` test
file. The "website" is an in-memory graph with simulated latency, a broken
link and a page that is too slow, so you can see error handling at work.
"""

import asyncio
import logging
import sys
import time

from crawler import Crawler, FakeSite


# --- 1. Configure logging once, at the entry point ---
def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(relativeCreated)6.0fms %(levelname)-7s %(message)s",
        stream=sys.stdout,
    )


# --- 2. Crawl the fake site ---
async def run_crawl(max_concurrency: int) -> None:
    site = FakeSite(seed=1)
    crawler = Crawler(site, max_concurrency=max_concurrency, timeout=0.3)
    start = time.perf_counter()
    result = await crawler.crawl("/")
    elapsed = time.perf_counter() - start

    # --- 3. Report ---
    print(f"\ncrawled {len(result.pages)} pages, {len(result.errors)} errors "
          f"in {elapsed:.2f}s (max_concurrency={max_concurrency}, "
          f"peak in flight={site.peak})")
    # -> crawled 9 pages, 2 errors ... peak in flight=3
    for url, page in sorted(result.pages.items()):
        print(f"  {url:<16} {page.title}")
    for url, reason in sorted(result.errors.items()):
        print(f"  {url:<16} ERROR: {reason}")  # -> /missing not found, /slow timeout


async def main() -> None:
    print("--- Crawl with 3 concurrent requests ---")
    await run_crawl(max_concurrency=3)
    print("\n--- Same crawl, one request at a time (slower) ---")
    logging.getLogger("crawler").setLevel(logging.WARNING)  # less noise this time
    await run_crawl(max_concurrency=1)


if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())
