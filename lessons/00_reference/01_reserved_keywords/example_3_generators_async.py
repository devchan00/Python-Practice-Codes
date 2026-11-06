"""Reserved keywords, part 3: generators (yield) and async code (async / await).

The last group of keywords is about producing and waiting for values lazily.
`yield` turns a function into a generator that hands out items one at a time,
and `yield from` delegates to another iterable. `async def` declares a
coroutine, `await` pauses it until another awaitable finishes, and
`async with` / `async for` are the asynchronous versions of with/for. We use
asyncio with tiny sleeps so everything finishes in well under a second.
"""

import asyncio


# --- 1. Generators: yield ---
def count_up_to(n):
    i = 1
    while i <= n:
        yield i                           # pause here, hand out i, resume on next request
        i += 1


def demo_yield():
    gen = count_up_to(3)
    print(gen)                            # -> <generator object count_up_to at 0x...>
    print(next(gen))                      # -> 1   (runs until the first yield)
    print(next(gen))                      # -> 2
    print(list(gen))                      # -> [3] (the rest)
    # WHY: a generator produces items lazily, so it can represent huge or even
    # infinite sequences without storing them all in memory.
    print(sum(x * x for x in range(1_000_000)))   # -> 333332833333500000


# --- 2. yield from: delegate to another iterable ---
def chain(*iterables):
    for it in iterables:
        yield from it                     # same as: for item in it: yield item


def demo_yield_from():
    print(list(chain([1, 2], "ab", range(2))))    # -> [1, 2, 'a', 'b', 0, 1]


# --- 3. async / await: coroutines ---
async def fetch(name, delay):
    await asyncio.sleep(delay)            # await = "pause me, let other tasks run"
    return f"{name} done"


async def demo_async_await():
    data = await fetch("one", 0.01)
    print(data)                           # -> one done
    # gather runs several coroutines concurrently: total time ~ the slowest one.
    results = await asyncio.gather(fetch("a", 0.02), fetch("b", 0.01))
    print(results)                        # -> ['a done', 'b done']


# --- 4. async with: asynchronous context manager ---
class Connection:
    async def __aenter__(self):
        print("  open connection")
        await asyncio.sleep(0)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        print("  close connection")       # cleanup is guaranteed, like normal `with`
        return False


async def demo_async_with():
    async with Connection() as conn:
        print("  using", type(conn).__name__)
    # ->   open connection / using Connection / close connection


# --- 5. async for: asynchronous iteration ---
async def ticker(n):
    for i in range(n):
        await asyncio.sleep(0)
        yield i                           # `yield` inside `async def` = async generator


async def demo_async_for():
    async for t in ticker(3):
        print("  tick", t)                # -> tick 0 / tick 1 / tick 2


async def main_async():
    await demo_async_await()
    await demo_async_with()
    await demo_async_for()


if __name__ == "__main__":
    print("--- 1. yield ---");        demo_yield()
    print("--- 2. yield from ---");   demo_yield_from()
    print("--- 3-5. async ---")
    asyncio.run(main_async())             # asyncio.run starts the event loop
