"""Syntax at a glance, part 1: literals, escapes and the format-spec mini-language.

A literal is a value written directly in code: 42, 0xFF, 3.14, 'text', b'abc'.
This file shows every literal and escape sequence from the cheatsheet, then
walks through each row of the format-spec table used by f'{value:spec}' and
format(value, spec), so you can see exactly what each spec produces.
"""

from datetime import datetime


# --- 1. Integer literals: binary, octal, hex, underscores ---
def demo_int_literals():
    print(0b101, 0o17, 0xFF)              # -> 5 15 255   prefixes 0b / 0o / 0x
    print(1_000_000)                      # -> 1000000    underscores are just for readability
    print(0b1111_0000)                    # -> 240        they work in any base


# --- 2. Float and complex literals ---
def demo_float_complex():
    print(1e3, 3.14, 2.5e-3)              # -> 1000.0 3.14 0.0025   e = "times 10 to the"
    z = 3 + 4j                            # j marks the imaginary part
    print(z, z.real, z.imag, abs(z))      # -> (3+4j) 3.0 4.0 5.0
    print(0.1 + 0.2)                      # -> 0.30000000000000004  floats are binary approximations


# --- 3. String literals: raw, bytes, f-string, triple-quoted ---
def demo_string_literals():
    print(r"\d+")                         # -> \d+    raw: backslashes are kept as-is (regex, Windows paths)
    print(len(r"\n"), len("\n"))          # -> 2 1    raw "\n" is two chars; normal "\n" is one
    print(b"abc", type(b"abc").__name__)  # -> b'abc' bytes
    x = 42
    print(f"{x}")                         # -> 42     f-string: expressions inside {} are evaluated
    print(f"{x * 2 = }")                  # -> x * 2 = 84
    text = '''line one
line two'''
    print(text)                           # -> line one / line two  (triple quotes span lines)


# --- 4. Escape sequences ---
def demo_escapes():
    print("a\nb")                         # -> a / b       \n newline
    print("a\tb")                         # -> a<TAB>b     \t tab
    print("back\\slash")                  # -> back\slash  \\ one literal backslash
    print('it\'s')                        # -> it's        \' quote inside same-quote string
    print("café")                    # -> café        é Unicode escape (4 hex digits)


# --- 5. Ellipsis and the singleton constants ---
def placeholder():
    ...                                   # Ellipsis as a "to do" body, like pass


def demo_constants():
    print(...)                            # -> Ellipsis
    print(... is Ellipsis)                # -> True
    print(placeholder())                  # -> None
    # NumPy uses ... in slicing: arr[..., 0] means "all leading dimensions".
    print(None, True, False)              # -> None True False  only one of each exists
    print(type(None).__name__)            # -> NoneType


# --- 6. Format spec: f'{value:spec}' or format(value, spec) ---
def demo_format_spec():
    pi = 3.14159
    print(f"{pi:.2f}")                    # -> 3.14        .2f = 2 decimals, fixed point
    print(format(pi, ".2f"))              # -> 3.14        same spec via format()

    # Alignment inside a width of 8 (brackets show the padding):
    print(f"[{'hi':>8}]")                 # -> [      hi]  > right
    print(f"[{'hi':<8}]")                 # -> [hi      ]  < left
    print(f"[{'hi':^8}]")                 # -> [   hi   ]  ^ centre

    print(f"{pi:08.3f}")                  # -> 0003.142    0 = zero-pad, total width 8, 3 decimals
    print(f"{1234:,}")                    # -> 1,234       thousands separator
    print(f"{1234567.891:,.2f}")          # -> 1,234,567.89  combine with decimals
    print(f"{0.125:.1%}")                 # -> 12.5%       multiply by 100 and add %
    print(f"{10:b} {255:x} {8:o}")        # -> 1010 ff 10  binary / hex / octal
    print(f"{255:#x} {10:#b}")            # -> 0xff 0b1010 # adds the prefix
    print(f"{12345.678:e}")               # -> 1.234568e+04  scientific notation

    word = "hi"
    print(f"{word!r}")                    # -> 'hi'        !r uses repr() of the value
    x = 5
    print(f"{x=}")                        # -> x=5         debug print: name and value

    print(f"{'title':*^20}")              # -> *******title********  fill char * + centre, width 20

    when = datetime(2024, 3, 9, 14, 30)
    print(f"{when:%Y-%m-%d}")             # -> 2024-03-09  datetime format codes
    print(f"{when:%H:%M}")                # -> 14:30

    w = 10
    print(f"[{'id':>{w}}]")               # -> [        id]  nested width taken from a variable
    for name, price in [("tea", 2.5), ("cake", 12)]:
        print(f"{name:<6}{price:>{w}.2f}")   # -> neat aligned columns


if __name__ == "__main__":
    print("--- 1. int literals ---");        demo_int_literals()
    print("--- 2. float/complex ---");       demo_float_complex()
    print("--- 3. string literals ---");     demo_string_literals()
    print("--- 4. escapes ---");             demo_escapes()
    print("--- 5. constants ---");           demo_constants()
    print("--- 6. format spec ---");         demo_format_spec()
