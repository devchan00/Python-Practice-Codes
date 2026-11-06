# Bonus 2: Big-O complexity, measured

## What you'll learn

- What Big-O notation means in practice: how cost **grows** with input size
- The cost of common list, dict, set, deque, heapq, bisect and string operations
- How to *measure* growth yourself with `timeit`

## Explanation

### Big-O in one paragraph

Big-O ignores constant factors and asks: if the data gets 100x bigger, how much
slower does this get? O(1) - no slower. O(log n) - a little (each doubling of n
adds one step). O(n) - 100x. O(n log n) - a bit over 100x. O(n^2) - 10,000x.
That growth matters far more than whether one call takes 30 ns or 50 ns.

### The table (from the cheatsheet)

| Operation | Cost | Why |
|---|---|---|
| `list[i]`, `append`, `pop()` | O(1) | A list is an array; the end is cheap to reach |
| `list.insert(0, x)` / `remove` / `x in list` | O(n) | Shifts or scans elements one by one |
| `dict` / `set`: get, set, `in` | O(1) average | Hash the key, jump straight to its slot |
| `sorted` / `list.sort` | O(n log n) | Timsort; stable (equal items keep their order) |
| `deque` append / pop (both ends) | O(1) | A linked list of blocks - no shifting |
| `heapq` push / pop | O(log n) | Sift up/down one branch of a binary tree |
| `bisect` on a sorted list | O(log n) | Binary search halves the range each step |
| `s += x` in a loop | O(n^2) total | Each `+=` may copy the whole string - use `''.join()` |

### How the script measures it

```python
import timeit
lst = list(range(n))
best = min(timeit.repeat(lambda: -1 in lst, number=200, repeat=3)) / 200
```

For each operation it builds data of size n = 1,000, 10,000 and 100,000, times
the operation (undoing any change so the size stays n), and prints
`time(100k) / time(1k)` next to the expected growth. Typical output:

```
operation                    Big-O           n=1,000    n=10,000   n=100,000   growth  expected
x in list                    O(n)             4.4 us     46.9 us    473.9 us   107.0x  ~100x
x in set                     O(1) avg          26 ns       34 ns       49 ns     1.9x  ~1x
heapq push + pop             O(log n)         120 ns      176 ns      194 ns     1.6x  ~1.7x
```

### About `s += x`

CPython has a trick: if a string has only one reference, `s += x` can resize
it in place, so the loop often looks fast. Any second reference (another
variable, a list holding it, or a different Python implementation) breaks the
trick and every `+=` copies the whole string. The demo holds a second
reference on purpose to show the true cost. `''.join(parts)` is O(n) always.

## Common mistakes

- `if x in big_list` inside a loop - O(n) each time, O(n^2) overall. Convert to a set once.
- Using `list.pop(0)` as a queue - use `collections.deque.popleft()`.
- Sorting repeatedly to keep a list ordered - use `bisect.insort` or `heapq`.
- Judging speed from a single tiny run; noise and constant overheads dominate small n.
- Forgetting that "O(1) average" for dicts assumes good hashes.

## How to run

```bash
cd lessons/05_bonus/02_big_o_complexity
python example.py        # takes a few seconds
```

## Try it yourself

1. Add a row for `list.pop(0)` vs `deque.popleft()` and compare them.
2. Add `max(lst)` and `lst.count(x)`. Predict their Big-O first.
3. Time `x in d.keys()` vs `x in d.values()` for a dict. Explain the difference.
