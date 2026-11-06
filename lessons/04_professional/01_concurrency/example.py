"""Lesson 4.1 - Concurrency: threads, processes and the GIL.

Python offers three concurrency models. Threads (``threading`` and
``ThreadPoolExecutor``) are great for I/O-bound work such as network calls or
disk reads, because a thread that is waiting gives up the GIL. Processes
(``multiprocessing`` / ``ProcessPoolExecutor``) give true CPU parallelism
because each process has its own interpreter and its own GIL. Shared state
between threads must be protected with ``Lock``, passed through a ``Queue``,
or rate-limited with a ``Semaphore``. The asyncio half of the lesson lives in
``async_example.py``.
"""

import os
import queue
import sys
import threading
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


# --- 1. Threads for I/O-bound work ---
def fake_download(n: int) -> str:
    """Pretend to download something; time.sleep() stands in for network I/O."""
    time.sleep(0.2)  # while sleeping, the GIL is released -> other threads run
    return f"page-{n}"


def demo_threads() -> None:
    print("\n--- 1. Threads for I/O-bound work ---")
    start = time.perf_counter()
    results = [fake_download(i) for i in range(5)]
    seq = time.perf_counter() - start
    print(f"sequential: {results} in {seq:.2f}s")  # -> about 1.0s (5 x 0.2s)

    start = time.perf_counter()
    threads = []
    out: list[str] = [""] * 5

    def worker(i: int) -> None:
        out[i] = fake_download(i)  # each thread writes its own slot: no race

    for i in range(5):
        t = threading.Thread(target=worker, args=(i,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()  # wait for every thread to finish
    print(f"threading.Thread: {out} in {time.perf_counter() - start:.2f}s")
    # -> about 0.2s: all five "downloads" waited at the same time


# --- 2. ThreadPoolExecutor: the easy way to use threads ---
def demo_thread_pool() -> None:
    print("\n--- 2. ThreadPoolExecutor ---")
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=5) as pool:
        # map() keeps the input order, just like the built-in map()
        pages = list(pool.map(fake_download, range(5)))
    print(pages, f"{time.perf_counter() - start:.2f}s")  # -> ['page-0', ...] ~0.2s

    with ThreadPoolExecutor(max_workers=2) as pool:
        future = pool.submit(fake_download, 99)  # submit() returns a Future
        print("future result:", future.result())  # -> future result: page-99


# --- 3. The GIL: why threads do NOT speed up CPU work ---
def cpu_work(n: int) -> int:
    """Pure-Python number crunching: holds the GIL the whole time."""
    total = 0
    for i in range(n):
        total += i * i
    return total


def demo_gil() -> None:
    print("\n--- 3. The GIL ---")
    # The Global Interpreter Lock lets only ONE thread run Python bytecode at a
    # time. So 4 CPU-bound threads take about as long as running them in a row.
    n, jobs = 3_000_000, 4
    start = time.perf_counter()
    for _ in range(jobs):
        cpu_work(n)
    seq = time.perf_counter() - start

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        list(pool.map(cpu_work, [n] * jobs))
    thr = time.perf_counter() - start
    print(f"CPU work sequential {seq:.2f}s vs threads {thr:.2f}s")
    # -> roughly the same: threads don't help CPU-bound code under the GIL
    gil_check = getattr(sys, "_is_gil_enabled", None)
    if gil_check is not None:
        # Python 3.13+ has an optional "free-threaded" build without the GIL.
        print("GIL enabled in this interpreter:", gil_check())  # -> True (normal build)


# --- 4. ProcessPoolExecutor for CPU-bound work ---
def demo_process_pool() -> None:
    print("\n--- 4. ProcessPoolExecutor ---")
    # Each worker is a separate Python process with its own GIL -> real parallelism.
    # On Windows, new processes re-import this file, which is why the code that
    # starts them MUST be under `if __name__ == "__main__":` (see bottom).
    n, jobs = 3_000_000, 4
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=min(jobs, os.cpu_count() or 1)) as pool:
        results = list(pool.map(cpu_work, [n] * jobs))
    print(f"{len(results)} results in {time.perf_counter() - start:.2f}s "
          f"using up to {os.cpu_count()} CPUs")
    # Process start-up costs time, so for tiny jobs processes can be SLOWER.
    # They win when each job does a lot of work. Functions passed to a process
    # pool must be defined at module level so they can be pickled.


# --- 5. Lock: protect shared state ---
def demo_lock() -> None:
    print("\n--- 5. Lock ---")
    counter = 0
    lock = threading.Lock()

    def add_many() -> None:
        nonlocal counter
        for _ in range(50_000):
            with lock:  # only one thread at a time may run this block
                counter += 1  # read-modify-write: NOT atomic without a lock

    threads = [threading.Thread(target=add_many) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("counter =", counter)  # -> counter = 200000 (always, thanks to the lock)


# --- 6. Queue: communicate between threads safely ---
def demo_queue() -> None:
    print("\n--- 6. Queue (producer / consumer) ---")
    q: queue.Queue[int | None] = queue.Queue()
    results: list[int] = []

    def producer() -> None:
        for i in range(5):
            q.put(i)  # Queue does its own locking internally
        q.put(None)  # sentinel value: "no more work"

    def consumer() -> None:
        while (item := q.get()) is not None:
            results.append(item * 10)

    p = threading.Thread(target=producer)
    c = threading.Thread(target=consumer)
    p.start(); c.start()
    p.join(); c.join()
    print("consumed:", results)  # -> consumed: [0, 10, 20, 30, 40]


# --- 7. Semaphore: limit how many threads do something at once ---
def demo_semaphore() -> None:
    print("\n--- 7. Semaphore ---")
    sem = threading.Semaphore(2)  # at most 2 holders at a time
    active = 0
    peak = 0
    guard = threading.Lock()

    def limited(i: int) -> None:
        nonlocal active, peak
        with sem:
            with guard:
                active += 1
                peak = max(peak, active)
            time.sleep(0.05)  # e.g. "only 2 connections to the server"
            with guard:
                active -= 1

    with ThreadPoolExecutor(max_workers=6) as pool:
        list(pool.map(limited, range(6)))
    print("max concurrent workers:", peak)  # -> max concurrent workers: 2


def main() -> None:
    demo_threads()
    demo_thread_pool()
    demo_gil()
    demo_process_pool()
    demo_lock()
    demo_queue()
    demo_semaphore()
    print("\nNext: run async_example.py for asyncio.")


# This guard is REQUIRED for ProcessPoolExecutor on Windows (and macOS):
# child processes import this module, and without the guard they would try to
# start their own pools, forever.
if __name__ == "__main__":
    main()
