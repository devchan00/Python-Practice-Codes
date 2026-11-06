"""Tests for crawler.py - run with:  python -m unittest -v

unittest.IsolatedAsyncioTestCase runs each `async def test_*` in its own
event loop, so we can `await` the crawler directly.
"""

import logging
import unittest

from crawler import Crawler, FakeSite, PageNotFound

# A small graph made just for tests: fast and fully predictable.
SITE = {
    "/": ("Home", ["/a", "/b"]),
    "/a": ("A", ["/", "/c"]),
    "/b": ("B", ["/c", "/gone"]),
    "/c": ("C", ["/deep"]),
    "/deep": ("Deep", []),
}


def make_site(**kwargs) -> FakeSite:
    return FakeSite(pages=SITE, latency=(0.001, 0.003), slow_urls={}, **kwargs)


class CrawlerTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        logging.disable(logging.CRITICAL)  # keep test output clean

    def tearDown(self) -> None:
        logging.disable(logging.NOTSET)

    async def test_visits_every_reachable_page_once(self) -> None:
        result = await Crawler(make_site()).crawl("/")
        self.assertEqual(set(result.pages), {"/", "/a", "/b", "/c", "/deep"})

    async def test_records_404(self) -> None:
        result = await Crawler(make_site()).crawl("/")
        self.assertEqual(result.errors, {"/gone": "not found"})

    async def test_respects_concurrency_limit(self) -> None:
        site = make_site()
        await Crawler(site, max_concurrency=1).crawl("/")
        self.assertEqual(site.peak, 1)

    async def test_concurrency_actually_happens(self) -> None:
        site = make_site()
        await Crawler(site, max_concurrency=5).crawl("/")
        self.assertGreater(site.peak, 1)

    async def test_timeout(self) -> None:
        site = FakeSite(pages=SITE, latency=(0.001, 0.002), slow_urls={"/c": 1.0})
        result = await Crawler(site, timeout=0.05).crawl("/")
        self.assertEqual(result.errors.get("/c"), "timeout")
        self.assertNotIn("/deep", result.pages)  # only reachable through /c

    async def test_max_depth(self) -> None:
        result = await Crawler(make_site(), max_depth=1).crawl("/")
        self.assertEqual(set(result.pages), {"/", "/a", "/b"})

    async def test_fake_site_raises_for_unknown(self) -> None:
        with self.assertRaises(PageNotFound):
            await make_site().fetch("/nope")


if __name__ == "__main__":
    unittest.main()
