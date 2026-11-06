"""Lesson 2.5 - Files & JSON.

Reading and writing files is done with the built-in open() inside a `with`
block, which guarantees the file is closed even if an error happens. The mode
string decides what you may do: r read, w overwrite, a append, x create-only,
b binary and + read/write. Always pass encoding= for text files so your
program behaves the same on every OS. The json module converts between Python
objects and JSON text. Every file here is created inside a temporary
directory that is deleted at the end, so nothing is left behind.
"""

import json
import tempfile
from pathlib import Path


# --- 1. Writing and reading text ---
def write_and_read(folder):
    print("--- 1. write (w) and read (r) ---")
    path = folder / "out.txt"

    # "w" creates the file, or EMPTIES it if it already exists.
    with open(path, "w", encoding="utf-8") as f:
        f.write("hello\n")              # write() does not add a newline for you
        f.write("world\n")
        print("first line\n", "second line", file=f)  # print can target a file too
    # The file is closed here, even if an exception had been raised.

    # Iterate a file object: lazy, one line at a time (fine for huge files).
    with open(path, encoding="utf-8") as f:      # mode defaults to "r"
        for line in f:
            print(line.rstrip())        # rstrip removes the trailing "\n"
    # -> hello / world / first line / " second line"

    with open(path, encoding="utf-8") as f:
        print(repr(f.read(5)))          # -> 'hello'   read N characters
        print(repr(f.readline()))       # -> '\n'      rest of the current line
        print(len(f.readlines()))       # -> 3         remaining lines as a list

    # pathlib shortcuts for small files (open + read/write + close in one call).
    print(repr(path.read_text(encoding="utf-8")[:11]))   # -> 'hello\nworld'
    return path


# --- 2. Appending ---
def append_mode(path):
    print("\n--- 2. append (a) ---")
    # "a" adds to the end and never erases existing content.
    with open(path, "a", encoding="utf-8") as f:
        f.write("appended\n")
    lines = path.read_text(encoding="utf-8").splitlines()
    print(len(lines), lines[-1])        # -> 5 appended


# --- 3. Exclusive create ---
def exclusive_mode(folder):
    print("\n--- 3. create-only (x) ---")
    path = folder / "new.txt"
    with open(path, "x", encoding="utf-8") as f:   # works: file doesn't exist yet
        f.write("first!")
    try:
        open(path, "x", encoding="utf-8")          # second time: refuses
    except FileExistsError as e:
        print("FileExistsError:", e.strerror)      # -> FileExistsError: File exists
    # WHY: "x" protects against accidentally overwriting existing data,
    # which "w" would do silently.


# --- 4. Binary mode ---
def binary_mode(folder):
    print("\n--- 4. binary (b) ---")
    path = folder / "data.bin"
    # Binary mode reads/writes bytes, not str, and takes no encoding.
    with open(path, "wb") as f:
        f.write(bytes([0, 1, 2, 255]))
        f.write("é".encode("utf-8"))   # text must be encoded to bytes first
    with open(path, "rb") as f:
        data = f.read()
    print(data)                         # -> b'\x00\x01\x02\xff\xc3\xa9'
    print(len(data))                    # -> 6   ('é' is 2 bytes in UTF-8)
    # Use binary for images, archives, or when copying any file byte-for-byte.


# --- 5. Read/write (+) ---
def plus_mode(folder):
    print("\n--- 5. read/write (+) ---")
    path = folder / "counter.txt"
    path.write_text("0000000000", encoding="utf-8")

    # "r+" opens an EXISTING file for both reading and writing, without
    # truncating it. (w+ truncates first, a+ always writes at the end.)
    with open(path, "r+", encoding="utf-8") as f:
        print(f.read())                 # -> 0000000000
        f.seek(0)                       # move back to the start before writing
        f.write("42")                   # overwrites the first two characters
        f.seek(0)
        print(f.read())                 # -> 4200000000

    with open(path, "w+", encoding="utf-8") as f:   # truncates, then read/write
        f.write("fresh")
        f.seek(0)
        print(f.read())                 # -> fresh


# --- 6. Encoding matters ---
def encodings(folder):
    print("\n--- 6. encoding= ---")
    path = folder / "unicode.txt"
    path.write_text("café ☕", encoding="utf-8")
    print(path.read_text(encoding="utf-8"))      # -> café ☕
    # Without encoding= Python uses the OS default (often cp1252 on Windows),
    # so the same code could print garbage or crash on another machine.
    print(len(path.read_bytes()))                # -> 9 bytes for 6 characters


# --- 7. JSON strings ---
def json_strings():
    print("\n--- 7. json.loads / json.dumps ---")
    data = json.loads('{"a": 1, "tags": ["x", "y"], "ok": true, "none": null}')
    print(data)              # -> {'a': 1, 'tags': ['x', 'y'], 'ok': True, 'none': None}
    print(type(data))        # -> <class 'dict'>   (str -> dict)

    text = json.dumps(data, indent=2)        # dict -> str, pretty-printed
    print(text.splitlines()[1])              # -> '  "a": 1,'
    print(json.dumps({"b": 2, "a": 1}, sort_keys=True))   # -> {"a": 1, "b": 2}
    print(json.dumps({"name": "José"}, ensure_ascii=False))  # -> {"name": "José"}

    # Only basic types convert: dict, list, str, int, float, bool, None.
    # Tuples become lists; sets and custom objects raise TypeError.
    print(json.loads(json.dumps((1, 2))))    # -> [1, 2]
    try:
        json.dumps({1, 2})
    except TypeError as e:
        print("TypeError:", e)               # -> TypeError: Object of type set is not JSON serializable


# --- 8. JSON files ---
def json_files(folder):
    print("\n--- 8. json.dump / json.load (files) ---")
    path = folder / "settings.json"
    settings = {"theme": "dark", "volume": 7, "recent": ["a.txt", "b.txt"]}

    # dump/load (no "s") work directly with file objects.
    with open(path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)
    with open(path, encoding="utf-8") as f:
        loaded = json.load(f)
    print(loaded == settings)                # -> True  (round trip)
    print(loaded["recent"][-1])              # -> b.txt

    # Bad JSON raises json.JSONDecodeError (a subclass of ValueError).
    try:
        json.loads("{'single': 'quotes'}")   # JSON requires double quotes
    except json.JSONDecodeError as e:
        print("JSONDecodeError:", e.msg)     # -> JSONDecodeError: Expecting property name enclosed in double quotes


# --- 9. Missing files ---
def missing_file(folder):
    print("\n--- 9. handling missing files ---")
    try:
        with open(folder / "nope.txt", encoding="utf-8") as f:
            f.read()
    except FileNotFoundError:
        print("no such file - using defaults")   # -> no such file - using defaults
    print((folder / "nope.txt").exists())        # -> False


def main():
    # TemporaryDirectory deletes the folder and everything in it on exit.
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        path = write_and_read(folder)
        append_mode(path)
        exclusive_mode(folder)
        binary_mode(folder)
        plus_mode(folder)
        encodings(folder)
        json_strings()
        json_files(folder)
        missing_file(folder)
        print("\nfiles created:", sorted(p.name for p in folder.iterdir()))
    print("temp folder still exists?", folder.exists())   # -> False


if __name__ == "__main__":
    main()
