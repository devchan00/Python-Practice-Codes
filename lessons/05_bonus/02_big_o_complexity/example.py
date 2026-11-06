"""Bonus 2 - Big-O of common operations, measured.

Big-O describes how the cost of an operation GROWS as the data grows. Rather
than take the cheatsheet's table on trust, this script times each operation
class with ``timeit`` at n = 1,000 / 10,000 / 100,000 and prints the growth
factor between the smallest and largest n. If n grows 100x, an O(1) operation
should stay about the same (~1x), O(log n) grows a little (~1.7x), O(n) about
100x, O(n log n) a bit more, and O(n^2) about 10,000x. Absolute times depend
on your machine; the growth pattern is the lesson. Runtime: a few seconds.
"""

import bisect
import heapq
import random
import timeit
from collections import deque
from collections.abc import Callable

SIZES = (1_000, 10_000, 100_000)


# --- 1. A tiny timing helper ---
def per_op(fn: Callable[[], object], number: int) -> float:
    """Best-of-3 time for ONE call of fn, in nanoseconds."""
    best = min(timeit.repeat(fn, number=number, repeat=3))
    return best / number * 1e9


# --- 2. One "case" per row of the cheatsheet table ---
# Each builder takes n, prepares data of size n, and returns (fn, number):
# fn performs the operation once; the data size stays n (we undo changes).
def case_list_index(n):
    lst = list(range(n))
    return (lambda: lst[n // 2]), 200_000


def case_list_append_pop(n):
    lst = list(range(n))
    return (lambda: (lst.append(0), lst.pop())), 200_000


def case_list_insert_front(n):
    lst = list(range(n))  # insert(0) shifts EVERY element one slot right
    return (lambda: (lst.insert(0, 0), lst.pop(0))), 2_000


def case_list_remove(n):
    lst = list(range(n))  # remove() scans from the front to find the value
    return (lambda: (lst.remove(n - 1), lst.append(n - 1))), 200


def case_list_in(n):
    lst = list(range(n))
    return (lambda: -1 in lst), 200  # a miss: checks all n items


def case_dict_ops(n):
    d = {i: i for i in range(n)}
    key = n // 2
    return (lambda: (d.get(key), d.__setitem__(key, 1), key in d)), 200_000


def case_set_in(n):
    s = set(range(n))
    return (lambda: (n // 2) in s), 200_000


def case_sorted(n):
    rng = random.Random(0)
    data = [rng.random() for _ in range(n)]
    return (lambda: sorted(data)), 5  # Timsort: O(n log n), stable


def case_deque_both_ends(n):
    dq = deque(range(n))
    return (lambda: (dq.appendleft(0), dq.popleft(), dq.append(0), dq.pop())), 200_000


def case_heapq(n):
    rng = random.Random(0)
    heap = [rng.random() for _ in range(n)]
    heapq.heapify(heap)  # O(n) once
    return (lambda: heapq.heappop(heap) if heapq.heappush(heap, 0.5) is None else None), 100_000


def case_bisect(n):
    lst = list(range(0, 2 * n, 2))  # must already be sorted
    return (lambda: bisect.bisect_left(lst, n)), 200_000


def case_str_concat_loop(n):
    def build():
        s = ""
        for _ in range(n):
            keep = s  # a 2nd reference defeats CPython's in-place += shortcut,
            s += "x"  # so each += copies the whole string: O(n) each, O(n^2) total
        del keep
        return s
    return build, 1


def case_str_join(n):
    return (lambda: "".join(["x" for _ in range(n)])), 3  # O(n) total


CASES = [
    ("list[i]", "O(1)", case_list_index),
    ("list append + pop()", "O(1)", case_list_append_pop),
    ("list.insert(0) + pop(0)", "O(n)", case_list_insert_front),
    ("list.remove(x)", "O(n)", case_list_remove),
    ("x in list", "O(n)", case_list_in),
    ("dict get / set / in", "O(1) avg", case_dict_ops),
    ("x in set", "O(1) avg", case_set_in),
    ("sorted(list)", "O(n log n)", case_sorted),
    ("deque append/pop both ends", "O(1)", case_deque_both_ends),
    ("heapq push + pop", "O(log n)", case_heapq),
    ("bisect on sorted list", "O(log n)", case_bisect),
    ("s += x in a loop (total)", "O(n^2)", case_str_concat_loop),
    ("''.join(parts) (total)", "O(n)", case_str_join),
]

EXPECTED_GROWTH = {  # for n growing 100x
    "O(1)": "~1x", "O(1) avg": "~1x", "O(log n)": "~1.7x",
    "O(n)": "~100x", "O(n log n)": "~170x", "O(n^2)": "~10000x",
}


def fmt_ns(ns: float) -> str:
    if ns >= 1e6:
        return f"{ns / 1e6:.1f} ms"
    if ns >= 1e3:
        return f"{ns / 1e3:.1f} us"
    return f"{ns:.0f} ns"


# --- 3. Run every case at every size and print the table ---
def main() -> None:
    header = (f"{'operation':<28} {'Big-O':<11}"
              + "".join(f"{'n=' + format(n, ','):>12}" for n in SIZES)
              + f"{'growth':>9}  expected")
    print(header)
    print("-" * len(header))
    for name, big_o, builder in CASES:
        times = []
        for n in SIZES:
            fn, number = builder(n)
            times.append(per_op(fn, number))
        growth = times[-1] / times[0]
        print(f"{name:<28} {big_o:<11}" + "".join(f"{fmt_ns(t):>12}" for t in times)
              + f"{growth:>8.1f}x  {EXPECTED_GROWTH[big_o]}")
    print("\ngrowth = time at n=100,000 / time at n=1,000 (n grew 100x)")
    print("Small-n timings are noisy and include fixed overheads (e.g. CPU caches),")
    print("so measured growth is rarely exact - look for the ORDER of magnitude.")
    print("The s += row grows far faster than 100x even though copying is a fast")
    print("memcpy: at small n the per-loop overhead hides the n^2 term; it wins as n grows.")
    # Takeaways:
    #  * Membership tests: use a set/dict, not a list.
    #  * Need a queue? deque, not list.pop(0).
    #  * Build strings with ''.join, not += in a loop.
    #  * Sorted data + bisect turns O(n) searches into O(log n).


if __name__ == "__main__":
    main()
