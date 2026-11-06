# Lesson 2.5 — Files & JSON

## What you'll learn

- Opening files safely with `with open(...)`
- Every mode: `r`, `w`, `a`, `x`, `b`, `+`
- Reading line by line, `read`, `readline`, `readlines`, and `seek`
- Why you should always pass `encoding="utf-8"`
- Converting with `json.loads` / `json.dumps` and `json.load` / `json.dump`
- Handling `FileNotFoundError`, `FileExistsError`, `JSONDecodeError`

## Explanation

### `with open(...)`

```python
with open("in.txt", encoding="utf-8") as f:
    for line in f:              # lazy, line by line
        print(line.rstrip())
```

The `with` block closes the file automatically, even if an error occurs.
Looping over the file object reads one line at a time, so huge files never have
to fit in memory. Each line keeps its `\n`; `rstrip()` removes it.

### Modes

| Mode | Meaning |
|---|---|
| `r` | Read (default). File must exist. |
| `w` | Write. Creates the file or **erases** an existing one. |
| `a` | Append to the end. Creates the file if needed. |
| `x` | Create-only. Raises `FileExistsError` if the file exists. |
| `b` | Binary — combine with others (`rb`, `wb`); works with `bytes`, no encoding. |
| `+` | Read *and* write — `r+` (no truncate), `w+` (truncate), `a+` (writes at end). |

With `+` modes, use `f.seek(0)` to move back to the start before reading what
you just wrote.

### Encoding

Text files are bytes on disk. `encoding="utf-8"` tells Python how to turn them
into characters. Without it Python uses the platform default (which differs
between Windows, macOS, and Linux), so the same code may break elsewhere.

### pathlib shortcuts

`Path.read_text(encoding=...)`, `Path.write_text(...)`, `read_bytes()`,
`write_bytes()` open, read or write, and close in one call — handy for small files.

### JSON

```python
data = json.loads('{"a": 1}')        # str  -> dict
text = json.dumps(data, indent=2)    # dict -> str
json.dump(obj, f)                    # object -> file
obj = json.load(f)                   # file   -> object
```

JSON supports dicts, lists, strings, numbers, `true/false` (`True/False`) and
`null` (`None`). Tuples become lists; sets and custom objects raise `TypeError`.

### Temporary files

The example writes everything inside `tempfile.TemporaryDirectory()`, which is
deleted on exit — useful for tests and scratch work.

## Common mistakes

- Opening with `"w"` when you meant `"a"` — the file is wiped instantly.
- Forgetting `encoding=` and getting `UnicodeDecodeError` on another machine.
- Writing a `str` to a file opened in `"wb"` (needs `bytes`) or vice versa.
- Mixing up `json.load` (file) and `json.loads` (string).
- Single quotes in JSON text — JSON requires double quotes.
- Reading after writing in `r+`/`w+` without `seek(0)` — you read nothing.

## How to run

```bash
python example.py
```

It leaves no files behind.

## Try it yourself

1. Write a function `count_words(path)` that returns how many words a text file
   contains, reading it line by line.
2. Save a list of three dicts (`name`, `score`) to `scores.json`, load it back,
   and print the highest score.
3. Write `safe_create(path, text)` that uses mode `"x"` and returns `False`
   instead of crashing if the file already exists.
