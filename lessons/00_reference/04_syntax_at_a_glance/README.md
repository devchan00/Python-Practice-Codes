# Syntax at a Glance: Literals, Format Specs, Operator Precedence

This lesson is a tour of the small pieces of syntax you meet everywhere: how to
write values directly in code (literals and escapes), how to format values into
neat text (the format-spec mini-language), and in what order Python evaluates
operators (precedence).

## What you'll learn

- Integer literals in binary/octal/hex (`0b101 0o17 0xFF`) and `1_000_000`
- Float, scientific and complex literals (`1e3 3.14 3+4j`)
- Raw strings, bytes, f-strings and triple-quoted strings
- Escape sequences `\n \t \\ \' \u00e9`
- `...` (Ellipsis) and the singletons `None True False`
- Every format spec: `.2f`, `>8 <8 ^8`, `08.3f`, `,`, `.1%`, `b x o`, `e`, `!r`, `=`, `*^20`, `%Y-%m-%d`, `>{w}`
- The full operator precedence table, from `(...)` down to `:=`

## Files

| File | Content |
|------|---------|
| `example_1_literals_and_format.py` | literals, escapes, constants, format-spec table |
| `example_2_operator_precedence.py` | one section per precedence row |

## Explanation

### Literals
```python
0b101, 0o17, 0xFF   # 5, 15, 255
1_000_000           # underscores only help humans read it
1e3, 3.14, 3+4j     # 1000.0, a float, a complex number
r'\d+'              # raw string: backslashes are kept (regex!)
b'abc'              # bytes, not str
f'{x}'              # f-string: evaluates x
'''text'''          # multi-line string
```

### Escapes
`\n` newline, `\t` tab, `\\` a backslash, `\'` a quote, `\u00e9` the Unicode
character `é`. In a raw string `r'...'` escapes are **not** processed.

### Ellipsis and singletons
`...` is the `Ellipsis` object: a placeholder body (`def f(): ...`) and used by
NumPy for slicing (`arr[..., 0]`). `None`, `True`, `False` exist only once each.

### Format spec: `f'{value:spec}'` or `format(value, spec)`
| Spec | Meaning | Example result |
|------|---------|----------------|
| `:.2f` | 2 decimals | `3.14` |
| `:>8` `:<8` `:^8` | right / left / centre in width 8 | `'      hi'` |
| `:08.3f` | zero-padded, width 8, 3 decimals | `0003.142` |
| `:,` | thousands separator | `1,234` |
| `:.1%` | percent | `12.5%` |
| `:b` `:x` `:o` | binary / hex / octal | `1010 ff 10` |
| `:e` | scientific notation | `1.234568e+04` |
| `{x!r}` | use `repr()` | `'hi'` |
| `{x=}` | debug print | `x=5` |
| `:*^20` | fill char `*`, centred, width 20 | `*******title********` |
| `:%Y-%m-%d` | datetime format | `2024-03-09` |
| `:>{w}` | width from a variable | `'        id'` |

### Operator precedence (highest to lowest)
| Level | Operators |
|-------|-----------|
| 1 | `(...)` grouping |
| 2 | `x[i]` `x.attr` `f()` |
| 3 | `**` (right-associative) |
| 4 | `+x` `-x` `~x` |
| 5 | `*` `/` `//` `%` `@` |
| 6 | `+` `-` |
| 7 | `<<` `>>` |
| 8 | `&`, then `^`, then `\|` |
| 9 | `==` `!=` `<` `>` `in` `is` (and `not in`, `is not`, `<=`, `>=`) |
| 10 | `not` |
| 11 | `and` |
| 12 | `or` |
| 13 | `x if c else y` |
| 14 | `:=` (lowest) |

Examples: `2 + 3 * 4` is `14`; `2 ** 3 ** 2` is `512`; `-2 ** 2` is `-4`;
`True or True and False` is `True` because `and` binds tighter than `or`.
Comparisons chain: `1 < x < 10` means `1 < x and x < 10`.

## Common mistakes

- `-2 ** 2` is `-4`, not `4` - write `(-2) ** 2`.
- Writing `if (n := len(data) > 3)` - `n` becomes `True`, not the length. Use `(n := len(data)) > 3`.
- `x == 1 or 2` is always truthy; write `x in (1, 2)`.
- Forgetting the `f` prefix: `'{x}'` prints `{x}` literally.
- Windows paths in normal strings: `"C:\new"` contains a newline! Use `r"C:\new"` or `/`.
- Comparing floats with `==`: `0.1 + 0.2 == 0.3` is `False`; use `math.isclose`.
- `7 // 2` is `3` but `-7 // 2` is `-4` (floor, not truncate).

## How to run

```
python example_1_literals_and_format.py
python example_2_operator_precedence.py
```

## Try it yourself

1. Print a table of three products and prices where names are left-aligned in 10 characters and prices right-aligned with 2 decimals and a thousands separator.
2. Predict, then check: `not 1 + 1 == 2 or 3`, `2 * 3 ** 2`, `1 << 1 + 1`.
3. Print the number 2024 in binary, octal and hex, both with and without prefixes (hint: `#`).
