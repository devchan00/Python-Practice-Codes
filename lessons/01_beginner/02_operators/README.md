# Lesson 2: Operators

## What you'll learn

- Arithmetic: `+ - * / // % **`
- Comparisons: `== != < > <= >=`, including chains like `0 < x < 10`
- Boolean logic: `and or not`, and what short-circuiting means
- Membership (`in`, `not in`) and identity (`is`, `is not`)
- Augmented assignment: `+= -= *= //=`
- The walrus operator `:=`
- Bitwise operators: `& | ^ ~ << >>`
- Truthy and falsy values

## Explanation

### Arithmetic

| Operator | Meaning        | Example   | Result |
|----------|----------------|-----------|--------|
| `+`      | add            | `7 + 2`   | `9`    |
| `-`      | subtract       | `7 - 2`   | `5`    |
| `*`      | multiply       | `7 * 2`   | `14`   |
| `/`      | true divide    | `7 / 2`   | `3.5`  |
| `//`     | floor divide   | `7 // 2`  | `3`    |
| `%`      | modulo (remainder) | `7 % 2` | `1`  |
| `**`     | power          | `7 ** 2`  | `49`   |

`/` always gives a float, even for `6 / 2` (`3.0`). `//` rounds *down*, toward
minus infinity, so `-7 // 2` is `-4`, not `-3`. `%` gives the remainder, which
is useful for "is this even?" (`n % 2 == 0`) and for wrap-around maths like
clock hours.

### Comparisons

Comparisons give back `True` or `False`. `==` compares and `=` assigns, so
don't mix them up. You can chain comparisons the way you would in maths:

```python
0 < x < 10     # same as (0 < x) and (x < 10)
```

### Boolean logic and short-circuiting

- `a and b` is true only when both are true.
- `a or b` is true when at least one is true.
- `not a` flips the value.

Python stops evaluating as soon as it knows the answer. This is called
*short-circuiting*, and it lets you guard a risky expression:

```python
divisor != 0 and 10 / divisor > 1   # the division never runs when divisor is 0
name or "Anonymous"                 # gives the first truthy value: a default
```

### Membership and identity

- `in` asks "is this inside?": `'a' in 'cat'`, `3 in [1, 2, 3]`,
  `'key' in some_dict` (which checks the dict's keys).
- `is` asks "is this *the same object*?", which is different from "equal".
  Two separate lists `[1, 2]` are `==` but not `is`. Use `is` mainly for `None`.

### Augmented assignment

`score += 5` is shorthand for `score = score + 5`. The same pattern works
for `-=`, `*=`, `//=`, `/=`, `%=`, `**=` and others.

### Walrus `:=`

`:=` assigns a value *and* returns it, so you can assign inside an `if` or
`while` condition:

```python
if (n := len(a)) > 3:
    print(f"List is long ({n} items)")
```

Keep the brackets. Without them, `n := len(a) > 3` stores the result of the
comparison (`True`) in `n`.

### Bitwise operators

These work on the binary digits of integers:
`&` AND, `|` OR, `^` XOR, `~` NOT (which equals `-(x + 1)`), `<<` shift left
(multiply by a power of 2), and `>>` shift right. A common use is packing
on/off flags into a single number: `perms = READ | WRITE`, then
`perms & WRITE` checks whether the WRITE flag is on.

### Truthy and falsy

In an `if` or `while`, these values count as false:
`0  0.0  ''  []  {}  set()  None  False`. **Everything else is truthy**,
including `"False"` (a non-empty string), `[0]`, and `-1`. That's why
`if items:` is the normal way to check that a list isn't empty.

## Common mistakes

- Using `=` (assignment) where you meant `==` (comparison).
- Expecting `/` to give an int. Use `//` when you want whole-number division.
- Using `is` to compare numbers or strings. Use `==`. `is` checks identity
  and can give confusing results.
- Writing `if x == 1 or 2:`. This is always true, because `2` on its own is
  truthy. Write `if x == 1 or x == 2:` or `if x in (1, 2):`.
- Forgetting the brackets around a walrus expression.
- Treating `^` as "power". It is XOR. Power is `**`.

## How to run

```bash
python example.py
```

## Try it yourself

1. Given `total_minutes = 135`, use `//` and `%` to print `2 h 15 min`.
2. Write one chained comparison that checks whether `temp` is between 18 and
   25 inclusive. Test it with several values.
3. With flags `READ, WRITE, EXECUTE = 1, 2, 4`, build `perms` with all three,
   then remove WRITE using `perms & ~WRITE`. Check which flags remain.
