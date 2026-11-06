"""Lesson 4.1b - Concurrency with asyncio.

asyncio runs many tasks on ONE thread. Each ``await`` is a point where a task
politely pauses so another task can run, which makes it ideal for thousands of
concurrent I/O operations. This file covers ``asyncio.run``, ``gather``,
``TaskGroup`` (3.11+), ``to_thread`` for blocking code, ``asyncio.timeout``
(3.11+), and the ``async for`` / ``async with`` protocols.
"""

import asyncio
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager


# --- 1. Coroutines and asyncio.run ---
async def fetch(n: int, delay: float = 0.2) -> int:
    await asyncio.sleep(delay)  # non-blocking wait: the loop runs other tasks
    return n


async def demo_basics() -> None:
    print("\n--- 1. Coroutines ---")
    coro = fetch(1)  # calling an async def does NOT run it yet...
    print(type(coro).__name__)  # -> coroutine
    print("awaited:", await coro)  # -> awaited: 1  (await actually runs it)


# --- 2. asyncio.gather: run coroutines concurrently ---
async def demo_gather() -> None:
    print("\n--- 2. gather ---")
    start = time.perf_counter()
    a, b, c = await asyncio.gather(fetch(1), fetch(2), fetch(3))
    print(a, b, c, f"in {time.perf_counter() - start:.2f}s")
    # -> 1 2 3 in 0.20s  (not 0.6s: all three waited together)


# --- 3. TaskGroup: structured concurrency (3.11+) ---
async def demo_taskgroup() -> None:
    print("\n--- 3. TaskGroup ---")
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(fetch(10))
        t2 = tg.create_task(fetch(20))
    # Leaving the block waits for ALL tasks. If one fails, the others are
    # cancelled and the errors are raised together as an ExceptionGroup.
    print(t1.result(), t2.result())  # -> 10 20

    async def boom() -> None:
        await asyncio.sleep(0.01)
        raise ValueError("bad task")

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(fetch(1, delay=1.0))  # will be cancelled
            tg.create_task(boom())
    except* ValueError as eg:
        print("caught:", eg.exceptions)  # -> caught: (ValueError('bad task'),)


# --- 4. asyncio.to_thread: run blocking code without freezing the loop ---
def blocking_io() -> str:
    time.sleep(0.2)  # a normal blocking call (e.g. a library with no async API)
    return "blocking done"


async def demo_to_thread() -> None:
    print("\n--- 4. to_thread ---")
    start = time.perf_counter()
    # If we called blocking_io() directly, the WHOLE event loop would stop.
    result, n = await asyncio.gather(asyncio.to_thread(blocking_io), fetch(5))
    print(result, n, f"in {time.perf_counter() - start:.2f}s")  # -> ... in 0.20s


# --- 5. asyncio.timeout: a deadline for a block (3.11+) ---
async def demo_timeout() -> None:
    print("\n--- 5. timeout ---")
    try:
        async with asyncio.timeout(0.1):
            await fetch(1, delay=1.0)  # too slow
    except TimeoutError:
        print("timed out after 0.1s")  # -> timed out after 0.1s
    # Older equivalent: await asyncio.wait_for(fetch(1), timeout=0.1)


# --- 6. async for (async iterators) and async with (async context managers) ---
async def ticker(n: int) -> AsyncIterator[int]:
    """An async generator: may await between yields."""
    for i in range(n):
        await asyncio.sleep(0.01)
        yield i


@asynccontextmanager
async def connection(name: str) -> AsyncIterator[str]:
    print(f"  open {name}")
    await asyncio.sleep(0.01)  # e.g. connect to a database
    try:
        yield name
    finally:
        print(f"  close {name}")  # always runs, even on error


async def demo_async_protocols() -> None:
    print("\n--- 6. async for / async with ---")
    async with connection("db") as conn:
        values = [i async for i in ticker(3)]  # async comprehension
        print(f"  {conn} got {values}")  # -> db got [0, 1, 2]
    async for i in ticker(2):
        print("  tick", i)  # -> tick 0 / tick 1


# --- 7. Semaphore and Queue in asyncio ---
async def demo_async_sync_primitives() -> None:
    print("\n--- 7. asyncio.Semaphore / asyncio.Queue ---")
    sem = asyncio.Semaphore(2)

    async def limited(i: int) -> int:
        async with sem:  # at most 2 coroutines inside at once
            await asyncio.sleep(0.05)
            return i

    start = time.perf_counter()
    print(await asyncio.gather(*(limited(i) for i in range(4))),
          f"{time.perf_counter() - start:.2f}s")  # -> [0, 1, 2, 3] 0.10s (2 batches)

    q: asyncio.Queue[int] = asyncio.Queue()
    for i in range(3):
        q.put_nowait(i)
    got = [await q.get() for _ in range(3)]
    print("queue:", got)  # -> queue: [0, 1, 2]


async def main() -> None:
    await demo_basics()
    await demo_gather()
    await demo_taskgroup()
    await demo_to_thread()
    await demo_timeout()
    await demo_async_protocols()
    await demo_async_sync_primitives()


if __name__ == "__main__":
    asyncio.run(main())  # creates the event loop, runs main(), closes the loop
