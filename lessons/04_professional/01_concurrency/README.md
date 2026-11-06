# 4.1 Concurrency: threads, processes and asyncio

## What you'll learn

- When to use **threads**, **processes** or **asyncio**
- `threading.Thread` and `ThreadPoolExecutor` for I/O-bound work
- What the **GIL** is and why it stops threads from speeding up CPU work
- `ProcessPoolExecutor` for CPU-bound work, and why Windows needs the `if __name__ == "__main__":` guard
- `Lock`, `Queue` and `Semaphore` for safe sharing between threads
- asyncio: `asyncio.run`, `gather`, `TaskGroup`, `to_thread`, `timeout`, `async for`, `async with`

## Explanation

### Picking a model

| Work type | Tool | Why |
|---|---|---|
| Waiting on network / disk (I/O-bound) | `threading`, `ThreadPoolExecutor` | Waiting threads release the GIL |
| Heavy computation (CPU-bound) | `multiprocessing`, `ProcessPoolExecutor` | Each process has its own GIL |
| Thousands of concurrent I/O tasks | `asyncio` | One thread, cheap tasks, cooperative switching |

### Threads for I/O

```python
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=5) as pool:
    pages = list(pool.map(download, urls))   # results in input order
```

Five downloads that each wait 0.2 s finish in about 0.2 s total, because the
threads wait at the same time. `pool.submit(fn, arg)` returns a `Future`; call
`.result()` to get the value (or the exception).

### The GIL

The Global Interpreter Lock lets only one thread execute Python bytecode at a
time. Threads still help with I/O, because a thread blocked in `sleep`, `recv`
or `read` releases the GIL. For pure-Python number crunching, four threads take
as long as doing the work in a row. Since 3.13 there is an optional
"free-threaded" build (`python3.13t`) without the GIL; `sys._is_gil_enabled()`
tells you which one you are running.

### Processes for CPU work

```python
from concurrent.futures import ProcessPoolExecutor

def crunch(n): ...          # must be at module level (it gets pickled)

if __name__ == "__main__":  # REQUIRED on Windows/macOS
    with ProcessPoolExecutor() as pool:
        print(list(pool.map(crunch, [10**6] * 4)))
```

Windows starts a child process by launching a fresh interpreter that
*imports your file*. Without the guard, every child would start its own pool
again. Starting processes is slow, so only use them for jobs that do real work.

### Lock, Queue, Semaphore

```python
lock = threading.Lock()
with lock:
    counter += 1           # read-modify-write is not atomic without the lock

q = queue.Queue()          # thread-safe FIFO: producer .put(), consumer .get()
sem = threading.Semaphore(2)
with sem: ...              # at most 2 threads in here at once
```

### asyncio

```python
import asyncio

async def fetch(n):
    await asyncio.sleep(1)      # non-blocking wait
    return n

async def main():
    a, b = await asyncio.gather(fetch(1), fetch(2))
    async with asyncio.TaskGroup() as tg:      # 3.11+
        t = tg.create_task(fetch(3))
    print(a, b, t.result())

asyncio.run(main())
```

- Calling `fetch(1)` only creates a coroutine object; `await` runs it.
- `gather` runs coroutines concurrently and returns results in order.
- `TaskGroup` waits for all its tasks and cancels the rest if one fails
  (errors arrive as an `ExceptionGroup`, caught with `except*`).
- `await asyncio.to_thread(blocking_fn)` runs blocking code in a thread so the
  event loop keeps going.
- `async with asyncio.timeout(5):` raises `TimeoutError` if the block is too slow.
- `async for` loops over async iterators (e.g. `async def` generators that
  `yield`); `async with` uses async context managers (`@asynccontextmanager`).
- asyncio has its own `asyncio.Semaphore`, `asyncio.Lock`, `asyncio.Queue`.

## Common mistakes

- Using threads for CPU-heavy code and wondering why it isn't faster (GIL).
- Forgetting `if __name__ == "__main__":` with process pools on Windows.
- Calling `time.sleep()` or `requests.get()` inside `async def`: it blocks the
  whole event loop. Use `await asyncio.sleep()` or `asyncio.to_thread()`.
- Calling a coroutine without `await` (Python warns "coroutine was never awaited").
- Updating shared counters from several threads without a `Lock`.
- Passing lambdas or nested functions to `ProcessPoolExecutor` (they can't be pickled).

## How to run

```bash
cd lessons/04_professional/01_concurrency
python example.py         # threads, processes, GIL, Lock/Queue/Semaphore
python async_example.py   # asyncio
```

## Try it yourself

1. Change `max_workers` in section 2 to `1`, then `2`. Predict the total time first.
2. Remove the `with lock:` in section 5 and run it a few times. Does the
   counter always reach 200000? (On some builds it still does - the race is
   real, but rare in short loops. Try more threads.)
3. Write an async function that downloads 20 fake pages with
   `asyncio.sleep(0.1)` each, at most 5 at a time, using `asyncio.Semaphore`.
   How long should it take?
