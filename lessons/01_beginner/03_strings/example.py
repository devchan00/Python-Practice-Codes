"""Lesson 3: Strings.

A string (str) is an immutable sequence of characters. "Immutable" means a
string can never be changed in place: every method such as upper() or
replace() returns a NEW string and leaves the original alone. This lesson
covers indexing and slicing, f-strings with format specs, changing case,
trimming, splitting and joining, replacing, searching with find() and
index(), prefix/suffix tests, character-class checks, and len().
"""


# --- 1. Indexing and slicing ---
def indexing_and_slicing():
    print("--- 1. Indexing and slicing ---")
    s = "Python"
    #     P  y  t  h  o  n
    #     0  1  2  3  4  5     positive index
    #    -6 -5 -4 -3 -2 -1     negative index counts from the end
    print(s[0])       # -> P       first character
    print(s[-1])      # -> n       last character (no need to know the length)
    print(s[1:4])     # -> yth     from index 1 up to, but NOT including, 4
    print(s[:2])      # -> Py      start omitted = from the beginning
    print(s[2:])      # -> thon    end omitted = to the end
    print(s[::-1])    # -> nohtyP  step -1 walks backwards: a reversed copy
    print(s[::2])     # -> Pto     every 2nd character

    # Slices never raise errors for out-of-range bounds; indexes do.
    print(s[2:100])   # -> thon
    try:
        s[10]
    except IndexError as e:
        print("IndexError:", e)   # -> IndexError: string index out of range


# --- 2. Strings are immutable ---
def immutability():
    print("\n--- 2. Immutability ---")
    s = "cat"
    try:
        s[0] = "b"            # cannot change a character in place
    except TypeError as e:
        print("TypeError:", e)   # -> TypeError: 'str' object does not support item assignment

    # Instead, build a new string and (optionally) rebind the name.
    s = "b" + s[1:]
    print(s)                  # -> bat

    # Methods return new strings; the original is untouched.
    word = "hello"
    word.upper()              # result thrown away!
    print(word)               # -> hello
    word = word.upper()       # keep the result by assigning it
    print(word)               # -> HELLO


# --- 3. f-strings and format specs ---
def f_strings():
    print("\n--- 3. f-strings ---")
    name, n = "Total", 3.14159
    # Put an f before the quote; anything in {} is evaluated.
    print(f"{name}: {n}")             # -> Total: 3.14159
    # After a colon comes a format spec: > right-align, 8 = width,
    # .2f = fixed point with 2 decimals.
    print(f"{name}: {n:>8.2f}")       # -> Total:     3.14
    print(f"[{'left':<8}]")           # -> [left    ]
    print(f"[{'mid':^8}]")            # -> [  mid   ]
    print(f"{1234567.891:,.2f}")      # -> 1,234,567.89  thousands separator
    print(f"{0.256:.1%}")             # -> 25.6%
    print(f"{42:05d}")                # -> 00042   pad with zeros
    print(f"{2 + 3 = }")              # -> 2 + 3 = 5   handy for debugging


# --- 4. Changing case ---
def changing_case():
    print("\n--- 4. Changing case ---")
    s = "hello wORLD"
    print(s.upper())      # -> HELLO WORLD
    print(s.lower())      # -> hello world
    print(s.title())      # -> Hello World
    # Lowercase both sides for a case-insensitive comparison:
    print("YES".lower() == "yes")   # -> True


# --- 5. Trimming: strip, lstrip, rstrip ---
def trimming():
    print("\n--- 5. Trimming ---")
    s = "   padded   "
    print(f"[{s.strip()}]")     # -> [padded]       both ends
    print(f"[{s.lstrip()}]")    # -> [padded   ]    left only
    print(f"[{s.rstrip()}]")    # -> [   padded]    right only
    # You can pass the characters to remove (any of them, from the ends).
    print("--==title==--".strip("-="))   # -> title
    # Real-world use: text from input() or files often has stray spaces
    # or a trailing newline.
    print(repr("line\n".rstrip()))       # -> 'line'


# --- 6. Splitting and joining ---
def split_and_join():
    print("\n--- 6. Split and join ---")
    csv_line = "red,green,blue"
    parts = csv_line.split(",")
    print(parts)                    # -> ['red', 'green', 'blue']
    print("a  b   c".split())       # -> ['a', 'b', 'c']   no arg = any whitespace

    # join is called on the SEPARATOR and takes a list of strings.
    lst = ["2024", "01", "15"]
    print(",".join(lst))            # -> 2024,01,15
    print("-".join(lst))            # -> 2024-01-15
    # join needs strings; convert numbers first.
    print(" + ".join(str(x) for x in [1, 2, 3]))   # -> 1 + 2 + 3


# --- 7. Replacing ---
def replacing():
    print("\n--- 7. Replace ---")
    s = "I like cats. cats are great."
    print(s.replace("cats", "dogs"))      # -> I like dogs. dogs are great.
    print(s.replace("cats", "dogs", 1))   # -> I like dogs. cats are great.  (limit 1)


# --- 8. Searching: find vs index ---
def searching():
    print("\n--- 8. find and index ---")
    s = "banana"
    print(s.find("n"))      # -> 2    position of the FIRST match
    print(s.find("z"))      # -> -1   find returns -1 when not found
    print(s.index("n"))     # -> 2
    try:
        s.index("z")        # index raises instead of returning -1
    except ValueError as e:
        print("ValueError:", e)   # -> ValueError: substring not found
    print(s.count("a"))     # -> 3    bonus: how many times it appears
    # If you only need yes/no, `in` is clearest:
    print("nan" in s)       # -> True


# --- 9. Prefix and suffix tests ---
def prefix_suffix():
    print("\n--- 9. startswith / endswith ---")
    filename = "report_2024.pdf"
    print(filename.startswith("report"))        # -> True
    print(filename.endswith(".pdf"))            # -> True
    print(filename.endswith((".jpg", ".png")))  # -> False  a tuple checks several


# --- 10. Character-class checks ---
def character_checks():
    print("\n--- 10. isdigit / isalpha ---")
    print("12345".isdigit())    # -> True   only digits
    print("12.5".isdigit())     # -> False  the dot is not a digit
    print("hello".isalpha())    # -> True   only letters
    print("hello1".isalpha())   # -> False
    print("".isdigit())         # -> False  empty strings are never "all digits"
    print("abc123".isalnum())   # -> True   bonus: letters or digits
    # Typical use: validate text before converting it.
    text = "42"
    if text.isdigit():
        print(int(text) * 2)    # -> 84


# --- 11. len() ---
def length():
    print("\n--- 11. len ---")
    print(len("Python"))    # -> 6
    print(len(""))          # -> 0
    print(len("héllo"))     # -> 5   counts characters, not bytes


if __name__ == "__main__":
    indexing_and_slicing()
    immutability()
    f_strings()
    changing_case()
    trimming()
    split_and_join()
    replacing()
    searching()
    prefix_suffix()
    character_checks()
    length()
