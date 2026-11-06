# Lesson 3: Strings

## What you'll learn

- Indexing and slicing: `s[0]`, `s[-1]`, `s[1:4]`, `s[::-1]`
- Why strings are *immutable*, and what that means for methods
- f-strings with format specs: `f'{name}: {n:>8.2f}'`
- Case: `.upper()`, `.lower()`, `.title()`
- Trimming: `.strip()`, `.lstrip()`, `.rstrip()`
- Splitting and joining: `s.split(',')`, `','.join(lst)`
- Replacing: `s.replace(a, b)`
- Searching: `s.find(x)` versus `s.index(x)`
- Prefix and suffix tests: `.startswith(p)`, `.endswith(p)`
- Character checks: `.isdigit()`, `.isalpha()`
- Length: `len(s)`

## Explanation

### Indexing and slicing

Every character has a position, starting at **0**. Negative positions count
back from the end, so `-1` is the last character.

```
  P  y  t  h  o  n
  0  1  2  3  4  5
 -6 -5 -4 -3 -2 -1
```

```python
s = "Python"
s[0]     # 'P'
s[-1]    # 'n'
s[1:4]   # 'yth': start is included, end is excluded
s[::-1]  # 'nohtyP': a step of -1 walks backwards
```

A slice is `[start:stop:step]`, and any part can be left out. A slice that
goes past the end is safe (`s[2:100]` gives `'thon'`), but a single index
that is out of range raises an `IndexError`.

### Immutable

You can't change a string in place: `s[0] = "b"` raises a `TypeError`. Every
method returns a **new** string. That's why you must keep the result:

```python
word.upper()          # does nothing useful: the result is thrown away
word = word.upper()   # correct
```

### f-strings

Put `f` before the quote, and anything inside `{}` is evaluated. After a
colon you can add a *format spec*:

| Spec        | Meaning                           | Example output |
|-------------|-----------------------------------|----------------|
| `{n:>8.2f}` | right-align, width 8, 2 decimals  | `'    3.14'`   |
| `{s:<8}`    | left-align, width 8               | `'left    '`   |
| `{s:^8}`    | centre, width 8                   | `'  mid   '`   |
| `{n:,.2f}`  | thousands separator               | `1,234,567.89` |
| `{n:.1%}`   | percentage                        | `25.6%`        |
| `{n:05d}`   | pad with zeros to width 5         | `00042`        |
| `{x = }`    | show the expression and its value | `x = 5`        |

### Case and trimming

`.upper()`, `.lower()`, and `.title()` change case. To compare text without
caring about case, lowercase both sides. `.strip()` removes whitespace from
both ends, while `.lstrip()` and `.rstrip()` remove it from one end only.
Pass characters to strip something else: `"--title--".strip("-")`.

### Split and join

`split` breaks a string into a list. `join` does the opposite. Note that
`join` is called on the **separator**:

```python
"red,green,blue".split(",")   # ['red', 'green', 'blue']
"-".join(["2024", "01", "15"]) # '2024-01-15'
```

`split()` with no argument splits on any run of whitespace. `join` only
accepts strings, so convert numbers first.

### Replace, find, and index

`s.replace(a, b)` replaces **all** occurrences. A third argument limits how
many get replaced. `find` and `index` both return the position of the first
match. The difference shows up when nothing matches: `find` returns `-1`,
while `index` raises a `ValueError`. If you only need a yes/no answer, use `in`.

### startswith, endswith, isdigit, isalpha, len

- `filename.endswith(".pdf")` tests a suffix. Pass a tuple to test several:
  `.endswith((".jpg", ".png"))`.
- `"123".isdigit()` is `True`, but `"12.5".isdigit()` and `"".isdigit()` are `False`.
- `"abc".isalpha()` is `True` only when every character is a letter.
- `len(s)` counts characters.

## Common mistakes

- Calling a method and forgetting to keep the result (`s.strip()` on its own).
- Off-by-one slices: `s[1:4]` stops *before* index 4.
- Writing `lst.join(",")`. It's the other way round: `",".join(lst)`.
- Checking `if s.find(x):`. A match at position 0 returns `0`, which is
  falsy. Use `if x in s:` instead.
- Forgetting the `f` prefix, so `"{name}"` prints literally.
- Joining a list that contains numbers (`TypeError`). Convert them with `str()` first.

## How to run

```bash
python example.py
```

## Try it yourself

1. Write code that checks whether a word is a palindrome, ignoring case
   (`"Level"` should count as one). Hint: `s[::-1]`.
2. Turn `"  alice SMITH  "` into `"Alice Smith"` in a single chained
   expression.
3. Given `prices = [3.5, 12, 7.25]`, print a right-aligned receipt where each
   line looks like `Item 1:     3.50`.
