"""An asyncio web "crawler" over a fake, in-memory site - no network needed.

The pieces a real crawler needs are all here: a fetcher with latency and
failures, a concurrency limit (``asyncio.Semaphore``), per-request timeouts,
de-duplication of visited URLs, a depth limit, logging and type hints. Swap
``FakeSite.fetch`` for an ``httpx.AsyncClient().get`` call and it would crawl
real pages.
"""

from __future__ import annotations

import asyncio
import logging
import random
from dataclasses import dataclass, field

log = logging.getLogger(__name__)


class PageNotFound(Exception):
    """Raised by the fake site for a URL that doesn't exist (an HTTP 404)."""


@dataclass
class Page:
    url: str
    title: str
    links: list[str]


# A tiny website as a graph: url -> (title, outgoing links)
DEFAULT_SITE: dict[str, tuple[str, list[str]]] = {
    "/": ("Home", ["/about", "/blog", "/shop"]),
    "/about": ("About us", ["/", "/team"]),
    "/team": ("Team", ["/about"]),
    "/blog": ("Blog", ["/blog/1", "/blog/2", "/missing"]),  # /missing -> 404
    "/blog/1": ("Post 1", ["/blog", "/blog/2"]),
    "/blog/2": ("Post 2", ["/blog", "/slow"]),
    "/slow": ("Very slow page", []),  # deliberately slower than the timeout
    "/shop": ("Shop", ["/shop/cart", "/"]),
    "/shop/cart": ("Cart", ["/shop/checkout"]),
    "/shop/checkout": ("Checkout", []),
}


class FakeSite:
    """Pretends to be a web server: async fetch with simulated latency."""

    def __init__(
        self,
        pages: dict[str, tuple[str, list[str]]] | None = None,
        latency: tuple[float, float] = (0.02, 0.06),
        slow_urls: dict[str, float] | None = None,
        seed: int = 0,
    ) -> None:
        self.pages = DEFAULT_SITE if pages is None else pages
        self.latency = latency
        self.slow_urls = {"/slow": 1.0} if slow_urls is None else slow_urls
        self._rng = random.Random(seed)  # seeded: reproducible "network" timing
        self.active = 0  # how many fetches are running right now
        self.peak = 0  # the most that ever ran at once

    async def fetch(self, url: str) -> Page:
        self.active += 1
        self.peak = max(self.peak, self.active)
        try:
            delay = self.slow_urls.get(url, self._rng.uniform(*self.latency))
            await asyncio.sleep(delay)  # the "network round trip"
            if url not in self.pages:
                raise PageNotFound(url)
            title, links = self.pages[url]
            return Page(url, title, list(links))
        finally:
            self.active -= 1


@dataclass
class CrawlResult:
    pages: dict[str, Page] = field(default_factory=dict)
    errors: dict[str, str] = field(default_factory=dict)  # url -> reason


class Crawler:
    """Breadth-first async crawler with a concurrency limit."""

    def __init__(
        self,
        site: FakeSite,
        max_concurrency: int = 3,
        timeout: float = 0.5,
        max_depth: int = 5,
    ) -> None:
        self.site = site  # dependency injection: tests can pass any fake site
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.timeout = timeout
        self.max_depth = max_depth

    async def _fetch_one(self, url: str, result: CrawlResult) -> list[str]:
        """Fetch one page; record it or the error. Return its links."""
        async with self.semaphore:  # at most max_concurrency fetches at once
            log.debug("fetching %s", url)
            try:
                async with asyncio.timeout(self.timeout):
                    page = await self.site.fetch(url)
            except TimeoutError:
                log.warning("timeout: %s", url)
                result.errors[url] = "timeout"
                return []
            except PageNotFound:
                log.warning("404: %s", url)
                result.errors[url] = "not found"
                return []
        log.info("ok %-16s %r (%d links)", url, page.title, len(page.links))
        result.pages[url] = page
        return page.links

    async def crawl(self, start: str = "/") -> CrawlResult:
        result = CrawlResult()
        seen: set[str] = {start}  # set: O(1) "have we queued this already?"
        frontier = [start]
        depth = 0
        while frontier and depth <= self.max_depth:
            log.debug("depth %d: %d url(s)", depth, len(frontier))
            # Fetch the whole level concurrently; the semaphore limits the load.
            async with asyncio.TaskGroup() as tg:
                tasks = [tg.create_task(self._fetch_one(u, result)) for u in frontier]
            next_frontier: list[str] = []
            for task in tasks:
                for link in task.result():
                    if link not in seen:
                        seen.add(link)
                        next_frontier.append(link)
            frontier = next_frontier
            depth += 1
        return result
