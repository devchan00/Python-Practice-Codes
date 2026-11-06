"""Lesson 3.7 - Standard-library power tools, part 1: data structures.

The standard library includes specialised containers that remove whole
categories of boilerplate: ``Counter`` (tallying), ``defaultdict`` (auto-
created values), ``deque`` (fast queues), ``namedtuple`` (lightweight records),
``ChainMap`` (layered lookups), ``heapq`` (priority queues), ``bisect`` (binary
search in sorted lists) and ``copy`` / ``deepcopy``.

See also ``example_functional.py`` (itertools and functools) and
``example_types.py`` (pathlib, Enum, ABC).
"""

import bisect
import copy
import heapq
from collections import ChainMap, Counter, defaultdict, deque, namedtuple


# --- 1. Counter: tally things ----------------------------------------------
def demo_counter():
    print("--- 1. Counter ---")
    words = "the cat and the hat and the bat".split()
    c = Counter(words)
    print(c.most_common(2))        # -> [('the', 3), ('and', 2)]
    print(c["dog"])                # -> 0   (missing keys count as 0, no KeyError)
    c.update(["cat", "cat"])
    print(c["cat"])                # -> 3
    print(Counter("aab") + Counter("bc"))   # -> Counter({'a': 2, 'b': 2, 'c': 1})


# --- 2. defaultdict: no more "if key not in d" ------------------------------
def demo_defaultdict():
    print("\n--- 2. defaultdict ---")
    groups = defaultdict(list)     # missing key -> list() is created for you
    for name in ["ann", "bob", "amy", "ben", "cy"]:
        groups[name[0]].append(name)
    print(dict(groups))            # -> {'a': ['ann', 'amy'], 'b': ['bob', 'ben'], 'c': ['cy']}
    counts = defaultdict(int)      # int() == 0
    for ch in "hello":
        counts[ch] += 1
    print(counts["l"], counts["z"])  # -> 2 0  (note: reading "z" INSERTED it)


# --- 3. deque: fast at both ends -------------------------------------------
def demo_deque():
    print("\n--- 3. deque ---")
    q = deque([1, 2, 3])
    q.appendleft(0)                # O(1); list.insert(0, x) is O(n)
    q.append(4)
    print(q.popleft(), q.pop(), q)  # -> 0 4 deque([1, 2, 3])
    q.rotate(1)
    print(q)                       # -> deque([3, 1, 2])
    recent = deque(maxlen=3)       # keeps only the last 3 items
    for i in range(6):
        recent.append(i)
    print(list(recent))            # -> [3, 4, 5]


# --- 4. namedtuple: a tuple with field names -------------------------------
Point = namedtuple("Point", ["x", "y"])


def demo_namedtuple():
    print("\n--- 4. namedtuple ---")
    p = Point(3, 4)
    print(p, p.x, p[1])            # -> Point(x=3, y=4) 3 4
    x, y = p                       # still unpacks like a tuple
    print(p._replace(x=0), p._asdict())  # -> Point(x=0, y=4) {'x': 3, 'y': 4}
    # Immutable and memory-light. For more features use @dataclass (lesson 05)
    # or typing.NamedTuple for a class-style syntax with type hints.


# --- 5. ChainMap: layered lookups ------------------------------------------
def demo_chainmap():
    print("\n--- 5. ChainMap ---")
    defaults = {"color": "blue", "size": "M", "debug": False}
    user = {"size": "L"}
    cli = {"debug": True}
    settings = ChainMap(cli, user, defaults)   # searched left to right
    print(settings["size"], settings["debug"], settings["color"])  # -> L True blue
    settings["color"] = "red"      # writes go to the FIRST mapping only
    print(cli, defaults["color"])  # -> {'debug': True, 'color': 'red'} blue


# --- 6. heapq: priority queue / smallest-N ---------------------------------
def demo_heapq():
    print("\n--- 6. heapq ---")
    tasks = []
    heapq.heappush(tasks, (3, "write tests"))   # (priority, item)
    heapq.heappush(tasks, (1, "fix bug"))
    heapq.heappush(tasks, (2, "review PR"))
    print(heapq.heappop(tasks))    # -> (1, 'fix bug')  smallest first, O(log n)
    nums = [5, 1, 8, 3, 9, 2]
    print(heapq.nsmallest(2, nums), heapq.nlargest(2, nums))  # -> [1, 2] [9, 8]
    heapq.heapify(nums)            # turn a list into a heap in place, O(n)
    print(nums[0])                 # -> 1  (heap[0] is always the minimum)


# --- 7. bisect: binary search on sorted lists ------------------------------
def grade(score, breakpoints=(60, 70, 80, 90), grades="FDCBA"):
    return grades[bisect.bisect(breakpoints, score)]


def demo_bisect():
    print("\n--- 7. bisect ---")
    data = [10, 20, 30, 40]
    print(bisect.bisect_left(data, 25))   # -> 2   index where 25 would go (O(log n))
    bisect.insort(data, 25)               # insert keeping the list sorted
    print(data)                           # -> [10, 20, 25, 30, 40]
    print([grade(s) for s in (55, 70, 89, 95)])   # -> ['F', 'C', 'B', 'A']


# --- 8. copy vs deepcopy ----------------------------------------------------
def demo_copy():
    print("\n--- 8. copy / deepcopy ---")
    original = {"name": "ann", "tags": ["a", "b"]}
    shallow = copy.copy(original)      # new dict, SAME inner list
    deep = copy.deepcopy(original)     # new dict AND new inner list
    original["tags"].append("c")
    print(shallow["tags"])             # -> ['a', 'b', 'c']  (shared!)
    print(deep["tags"])                # -> ['a', 'b']       (independent)
    print(shallow is original, shallow["tags"] is original["tags"])  # -> False True


if __name__ == "__main__":
    demo_counter()
    demo_defaultdict()
    demo_deque()
    demo_namedtuple()
    demo_chainmap()
    demo_heapq()
    demo_bisect()
    demo_copy()
