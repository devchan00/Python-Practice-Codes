"""Lesson 3.4 - Special (dunder) methods, part 1: the everyday protocol.

"Dunder" (double-underscore) methods such as ``__repr__`` or ``__add__`` are
hooks that Python calls for you: ``len(x)`` calls ``x.__len__()``, ``a + b``
calls ``a.__add__(b)``, ``x[i]`` calls ``x.__getitem__(i)`` and so on.
Implementing them makes your own classes behave like built-in types. This
file covers creation/representation, comparison/hashing, arithmetic
(including the reflected ``__radd__``), containers, callables, truthiness and
attribute access. ``example_advanced.py`` covers ``__slots__``, descriptors,
``__init_subclass__`` and ``__new__``.
"""

import functools


# --- 1. __init__, __repr__, __str__, __format__ ----------------------------
class Money:
    def __init__(self, amount, currency="EUR"):    # initialise a new instance
        self.amount = amount
        self.currency = currency

    def __repr__(self):            # unambiguous, for developers (REPL, lists)
        return f"Money({self.amount!r}, {self.currency!r})"

    def __str__(self):             # friendly, for users (print, str())
        return f"{self.amount:.2f} {self.currency}"

    def __format__(self, spec):    # f"{m:short}" calls __format__("short")
        if spec == "short":
            return f"{self.amount:g}{self.currency[0]}"
        return format(str(self), spec)

    # --- 3. Arithmetic: __add__, __radd__, __iadd__, __mul__, __neg__ ------
    def __add__(self, other):      # self + other
        if isinstance(other, Money):
            return Money(self.amount + other.amount, self.currency)
        if isinstance(other, (int, float)):
            return Money(self.amount + other, self.currency)
        return NotImplemented      # let Python try other.__radd__(self)

    def __radd__(self, other):     # other + self, when other doesn't know us
        return self.__add__(other) # addition is symmetric here

    def __iadd__(self, other):     # self += other (may mutate in place)
        result = self + other
        self.amount = result.amount
        return self

    def __mul__(self, factor):     # self * factor
        return Money(self.amount * factor, self.currency)

    __rmul__ = __mul__             # factor * self

    def __neg__(self):             # -self
        return Money(-self.amount, self.currency)

    def __bool__(self):            # truthiness: if money: ...
        return self.amount != 0


def demo_repr_str():
    print("--- 1. __init__ / __repr__ / __str__ / __format__ ---")
    m = Money(9.5)
    print(repr(m))             # -> Money(9.5, 'EUR')
    print(str(m))              # -> 9.50 EUR
    print([m])                 # -> [Money(9.5, 'EUR')]  (containers use repr)
    print(f"{m:short}")        # -> 9.5E
    print(f"[{m:>12}]")        # -> [    9.50 EUR]


def demo_arithmetic():
    print("\n--- 3. Arithmetic & __radd__ ---")
    a, b = Money(10), Money(2.5)
    print(a + b)               # -> 12.50 EUR
    print(a + 1)               # -> 11.00 EUR   (__add__ with an int)
    print(1 + a)               # -> 11.00 EUR   (int.__add__ fails -> __radd__)
    # sum() starts from 0, so 0 + Money(...) needs __radd__ to work:
    print(sum([a, b, Money(1)]))   # -> 13.50 EUR
    print(a * 3, 3 * a)        # -> 30.00 EUR 30.00 EUR
    print(-a)                  # -> -10.00 EUR
    a += 5
    print(a)                   # -> 15.00 EUR
    print(bool(Money(0)), bool(a))  # -> False True


# --- 2. Comparison & hashing: __eq__, __lt__, __hash__ ---------------------
@functools.total_ordering          # fills in <=, >, >= from __eq__ and __lt__
class Version:
    def __init__(self, text):
        self.parts = tuple(int(p) for p in text.split("."))

    def __repr__(self):
        return "Version(" + ".".join(map(str, self.parts)) + ")"

    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self.parts == other.parts

    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self.parts < other.parts

    def __hash__(self):            # equal objects MUST have equal hashes
        return hash(self.parts)    # defining __eq__ alone sets __hash__ = None


def demo_comparison():
    print("\n--- 2. __eq__ / __lt__ / __hash__ ---")
    v1, v2 = Version("3.9"), Version("3.12")
    print(v1 < v2, v1 >= v2)   # -> True False   (numeric, not string order)
    print(sorted([v2, v1]))    # -> [Version(3.9), Version(3.12)]
    print(Version("1.0") == Version("1.0"))   # -> True
    print(len({Version("1.0"), Version("1.0")}))  # -> 1  (hashable, deduped)


# --- 4. Container protocol --------------------------------------------------
class Playlist:
    def __init__(self, *songs):
        self._songs = list(songs)

    def __len__(self):                 # len(p)
        return len(self._songs)

    def __getitem__(self, index):      # p[0], p[1:3], and makes p iterable
        return self._songs[index]

    def __setitem__(self, index, value):   # p[0] = "x"
        self._songs[index] = value

    def __delitem__(self, index):      # del p[0]
        del self._songs[index]

    def __contains__(self, song):      # "x" in p
        return song.lower() in (s.lower() for s in self._songs)

    def __iter__(self):                # for s in p
        return iter(self._songs)

    def __reversed__(self):            # reversed(p)
        return reversed(self._songs)


class Countdown:
    """An iterator: __iter__ returns self, __next__ hands out one value."""

    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):                # next(c); `for` calls this for you
        if self.current <= 0:
            raise StopIteration        # tells `for` the iterator is used up
        self.current -= 1
        return self.current + 1


def demo_container():
    print("\n--- 4. Container protocol ---")
    p = Playlist("Intro", "Song A", "Song B", "Outro")
    print(len(p), p[0], p[1:3])    # -> 4 Intro ['Song A', 'Song B']
    p[0] = "Overture"
    del p[-1]
    print(list(p))                 # -> ['Overture', 'Song A', 'Song B']
    print("song a" in p)           # -> True (our case-insensitive __contains__)
    print(list(reversed(p)))       # -> ['Song B', 'Song A', 'Overture']
    c = Countdown(3)
    print(next(c))                 # -> 3   (__next__ called directly)
    print(list(c))                 # -> [2, 1]  (continues where it left off)


# --- 5. __call__: instances that behave like functions ---------------------
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, x):         # m(5) calls m.__call__(5)
        return x * self.factor


def demo_call():
    print("\n--- 5. __call__ ---")
    triple = Multiplier(3)
    print(triple(5), callable(triple))      # -> 15 True
    print(list(map(triple, [1, 2])))        # -> [3, 6]


# --- 6. Attribute hooks: __getattr__, __setattr__ --------------------------
class Config:
    def __init__(self, **values):
        # bypass our own __setattr__ to avoid infinite recursion
        object.__setattr__(self, "_values", dict(values))

    def __getattr__(self, name):   # only called when normal lookup FAILS
        try:
            return self._values[name]
        except KeyError:
            raise AttributeError(name) from None

    def __setattr__(self, name, value):     # called for EVERY assignment
        if not name.isidentifier() or name.startswith("_"):
            raise AttributeError(f"cannot set {name}")
        self._values[name] = value


def demo_attribute_hooks():
    print("\n--- 6. __getattr__ / __setattr__ ---")
    c = Config(debug=True)
    c.level = 3
    print(c.debug, c.level)        # -> True 3
    print(getattr(c, "missing", "default"))  # -> default


# --- 7. __enter__ / __exit__ (see lesson 03) and __del__ -------------------
class Resource:
    def __enter__(self):
        print("open")
        return self

    def __exit__(self, *exc):
        print("close")
        return False


def demo_enter_exit():
    print("\n--- 7. __enter__ / __exit__ ---")
    with Resource():
        print("using")             # -> open / using / close
    # __del__ also exists (called when an object is garbage-collected) but
    # *when* it runs is not guaranteed - prefer context managers for cleanup.


if __name__ == "__main__":
    demo_repr_str()
    demo_comparison()
    demo_arithmetic()
    demo_container()
    demo_call()
    demo_attribute_hooks()
    demo_enter_exit()
