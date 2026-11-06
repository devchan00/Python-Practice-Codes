"""Built-in functions, part 1: numbers, conversions, text and binary data.

Built-ins are available everywhere without an import. This file covers the ones
that create or convert values: abs, bin/hex/oct, bool, int/float/str, chr/ord,
divmod, pow, round, format, repr, hash, and the binary types bytes, bytearray
and memoryview. Each demo prints its result with the expected output beside it.
"""


# --- 1. abs: absolute value ---
def demo_abs():
    print(abs(-7), abs(3.5), abs(3 + 4j))   # -> 7 3.5 5.0  (for complex: distance from 0)


# --- 2. bin / hex / oct: number as a base-2 / 16 / 8 string ---
def demo_bases():
    print(bin(5), hex(255), oct(15))        # -> 0b101 0xff 0o17
    # They return STRINGS. To go back, use int() with a base:
    print(int("ff", 16), int("0b101", 0))   # -> 255 5   (base 0 = read the prefix)


# --- 3. bool / int / float / str: type conversion ---
def demo_conversions():
    print(bool(0), bool(""), bool("0"))     # -> False False True  ("0" is a non-empty str!)
    print(int("42") + 1)                    # -> 43
    print(int(3.99))                        # -> 3     (int() truncates toward zero)
    print(float("2.5") * 2)                 # -> 5.0
    print(str(10) + "px")                   # -> 10px  (you can't add str + int directly)
    try:
        int("4.5")
    except ValueError as e:
        print("ValueError:", e)             # -> invalid literal for int() with base 10: '4.5'


# --- 4. chr / ord: code point <-> character ---
def demo_chr_ord():
    print(ord("A"), chr(65))                # -> 65 A
    print(chr(233), ord("é"))               # -> é 233
    # Shift a letter: chr(ord('a') + 1)
    print(chr(ord("a") + 1))                # -> b


# --- 5. divmod / pow / round ---
def demo_math():
    print(divmod(17, 5))                    # -> (3, 2)   quotient and remainder at once
    minutes, seconds = divmod(125, 60)
    print(f"{minutes}m {seconds}s")         # -> 2m 5s

    print(pow(2, 10))                       # -> 1024     same as 2 ** 10
    print(pow(2, 10, 1000))                 # -> 24       (2**10) % 1000, but computed fast
    print(pow(3, -1, 7))                    # -> 5        modular inverse: 3*5 % 7 == 1

    print(round(3.14159, 2))                # -> 3.14
    # "Banker's rounding": exact halves go to the nearest EVEN number.
    print(round(0.5), round(1.5), round(2.5))   # -> 0 2 2
    print(round(1234, -2))                  # -> 1200   negative n rounds to tens/hundreds


# --- 6. format / repr: turning values into strings ---
def demo_format_repr():
    print(format(3.14159, ".2f"))           # -> 3.14     same mini-language as f-strings
    print(format(1234567, ","))             # -> 1,234,567
    print(format(255, "x"))                 # -> ff

    s = "hi\n"
    print(str(s))                           # -> hi   (plus a newline: for humans)
    print(repr(s))                          # -> 'hi\n'   for developers: shows quotes/escapes
    # WHY: repr is what you want in logs and debugging - it shows the exact value.


# --- 7. hash: hash value ---
def demo_hash():
    print(hash(42))                         # -> 42  (small ints hash to themselves)
    print(hash("abc") == hash("abc"))       # -> True  (equal objects -> equal hashes)
    # Hashes let dicts and sets find keys quickly. Mutable objects can't be hashed:
    try:
        hash([1, 2])
    except TypeError as e:
        print("TypeError:", e)              # -> unhashable type: 'list'
    # Note: str hashes change between runs (randomised for security).


# --- 8. bytes / bytearray / memoryview: binary data ---
def demo_binary():
    b = bytes([72, 105])                    # immutable sequence of numbers 0-255
    print(b, b"abc"[0])                     # -> b'Hi' 97   (indexing gives an int)
    print("café".encode("utf-8"))           # -> b'caf\xc3\xa9'  str -> bytes
    print(b"caf\xc3\xa9".decode("utf-8"))   # -> café         bytes -> str

    ba = bytearray(b"hello")                # MUTABLE version of bytes
    ba[0] = ord("J")
    print(ba)                               # -> bytearray(b'Jello')

    # memoryview: a zero-copy window onto a buffer. Slicing it does NOT copy data,
    # and writes go straight through to the original - useful for big buffers.
    data = bytearray(b"abcdef")
    view = memoryview(data)[2:4]
    view[0] = ord("X")
    print(data, view.tobytes())             # -> bytearray(b'abXdef') b'Xd'


if __name__ == "__main__":
    print("--- 1. abs ---");               demo_abs()
    print("--- 2. bin/hex/oct ---");       demo_bases()
    print("--- 3. conversions ---");       demo_conversions()
    print("--- 4. chr/ord ---");           demo_chr_ord()
    print("--- 5. divmod/pow/round ---");  demo_math()
    print("--- 6. format/repr ---");       demo_format_repr()
    print("--- 7. hash ---");              demo_hash()
    print("--- 8. binary data ---");       demo_binary()
