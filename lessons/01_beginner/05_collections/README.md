# Lesson 5: Collections (list, tuple, dict, set)

## What you'll learn

- The four built-in collections and when to use each one
- List methods: `append`, `extend`, `insert`, `remove`, `pop`, `sort`, `reverse`
- List slicing (`lst[::2]`) and shallow copying (`lst[:]`)
- Tuples, including the one-item tuple `(1,)`
- Dicts: `d.get(k, default)`, `keys()`/`values()`/`items()`, `update`, `|`,
  `setdefault`, `pop`
- Sets: `add`, `discard`, and the operators `|  &  -  ^`

## Explanation

### Choosing a collection

| Type    | Literal    | Ordered | Mutable | Duplicates | Use it for                       |
|---------|------------|---------|---------|------------|----------------------------------|
| `list`  | `[1, 2, 3]`| yes     | yes     | yes        | a sequence that grows or changes |
| `tuple` | `(1, 2)`   | yes     | no      | yes        | a fixed record, like a point     |
| `dict`  | `{'a': 1}` | insertion order | yes | unique keys | looking things up by key   |
| `set`   | `{1, 2}`   | no      | yes     | no         | uniqueness, fast `in` checks     |

Two traps: `(1)` is just the number 1, so a one-item tuple is `(1,)`. And
`{}` is an empty **dict**. An empty set is `set()`.

### List methods

```python
lst.append(x)      # add one item at the end
lst.extend(it)     # add every item from another iterable
lst.insert(i, x)   # put x at index i
lst.remove(x)      # delete the first item equal to x (ValueError if missing)
lst.pop(i)         # remove and return item i (default: the last one)
lst.sort()         # sort in place
lst.reverse()      # reverse in place
```

`sort()` and `reverse()` change the list and return `None`. Writing
`lst = lst.sort()` throws your list away. Use `sorted(lst)` when you want a
new list instead.

### Slicing and copying

`lst[::2]` takes every second item. `lst[:]` makes a **shallow copy**. This
matters because `alias = lst` does not copy anything. It just gives the same
list a second name, so changes made through one name show up in the other.
"Shallow" means that lists nested inside are still shared between the copies.

### Tuples

A tuple works like a list you can't change. That immutability is useful:
it tells readers the data is fixed, and it allows tuples to be used as dict
keys and set items (lists can't be).

### Dicts

```python
d["apple"]            # KeyError if missing
d.get("apple", 0)     # safe: returns 0 if missing
d.keys(), d.values(), d.items()   # views to loop over
d.update(o)           # merge o into d (changes d)
d | o                 # merge into a NEW dict (Python 3.9+); the right side wins
d.setdefault(k, v)    # insert k with v only if k is missing; returns d[k]
d.pop(k)              # remove k and return its value
```

`for k, v in d.items():` is the standard way to loop over key/value pairs.

### Sets

`s.add(x)` adds an item. `s.discard(x)` removes it without complaining if
it's absent, whereas `s.remove(x)` raises a `KeyError`. Checking `x in s` is
very fast, even for huge sets. Set operators work like Venn diagrams:

| Operator | Name                 | `{1,2,3,4}` op `{3,4,5}` |
|----------|----------------------|--------------------------|
| `a \| b` | union                | `{1, 2, 3, 4, 5}`        |
| `a & b`  | intersection         | `{3, 4}`                 |
| `a - b`  | difference           | `{1, 2}`                 |
| `a ^ b`  | symmetric difference | `{1, 2, 5}`              |

## Common mistakes

- `lst = lst.sort()`, which sets `lst` to `None`.
- `append([5, 6])` when you meant `extend([5, 6])`. The first adds a single
  nested list.
- Thinking `b = a` copies a list. Use `a[:]`, `a.copy()`, or `list(a)`.
- Writing `{}` for an empty set.
- Using `d[key]` for a key that might be missing. Use `d.get(key, default)`.
- Changing a list while looping over it. Loop over a copy instead
  (`for x in lst[:]`).

## How to run

```bash
python example.py
```

## Try it yourself

1. Count how often each word appears in `"the cat and the hat and the bat"`
   using a dict and `d.get(word, 0) + 1`.
2. Given two lists of student names, print who is in both, who is only in the
   first, and everyone combined, using set operators.
3. Start with `[5, 3, 8, 1]`. Insert 10 at the front, remove 8, pop the last
   item, and sort what's left. Predict each step's result before running it.
