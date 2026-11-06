# Lesson 4: Control Flow

## What you'll learn

- Making decisions with `if` / `elif` / `else`
- Repeating with `for` and `range()`
- Repeating with `while`, and leaving or skipping with `break` and `continue`
- The loop `else` clause
- The one-line conditional expression (the "ternary"): `"yes" if ok else "no"`
- How indentation defines blocks

## Explanation

### if / elif / else

```python
if x > 0:
    print("positive")
elif x == 0:
    print("zero")
else:
    print("negative")
```

Python tests each condition from top to bottom and runs **only the first**
branch that is true. `elif` ("else if") can appear as often as you like.
`else` is optional and catches everything left over. Because the first true
branch wins, put the most specific test first (`score >= 90` before
`score >= 80`).

The colon `:` and the indentation (4 spaces) are required. Indentation is
how Python knows which lines belong inside the block.

### for loops

```python
for i in range(3):     # 0, 1, 2
    print(i)
```

`for` runs the block once for each item of a sequence: a `range`, a list,
a string (one character at a time), a dict (one key at a time), and so on.
`range(3)` stops *before* 3.

### while, break, continue

`while` repeats as long as its condition is true. Something inside the loop
has to eventually make the condition false, or the loop never ends.

```python
while n > 0:
    n -= 1
    if n == 5: break        # leave the loop immediately
    if n % 2: continue      # skip the rest of this round
```

- `break` exits the loop entirely.
- `continue` jumps straight to the next round.

### Loop else

A `for` or `while` loop can have an `else` block. It runs **only if the loop
finished without `break`**. This suits search loops: "if I never found it, do X".

### Ternary (conditional expression)

```python
label = "yes" if ok else "no"
```

Read it as "label is `"yes"` if `ok` is true, otherwise `"no"`". Use it to
choose a **value**. When you need to run different statements, a full
`if`/`else` block is easier to read.

### pass

A block can't be empty. `pass` is a placeholder that does nothing.

## Common mistakes

- Forgetting the colon after `if`, `elif`, `else`, `for`, or `while`.
- Mixing tabs and spaces, or indenting inconsistently (`IndentationError`).
- Writing `else if` instead of `elif`.
- A `while` loop that never changes its condition, so it runs forever.
  Press `Ctrl+C` to stop one.
- Expecting `range(1, 5)` to include 5. It doesn't.
- Putting a broad condition before a specific one in an `elif` chain.

## How to run

```bash
python example.py
```

## Try it yourself

1. FizzBuzz: for numbers 1 to 20, print `Fizz` for multiples of 3, `Buzz`
   for multiples of 5, `FizzBuzz` for both, and the number otherwise.
2. Use a `while` loop to find the first power of 2 that is greater than 1000.
3. Use `for ... else` to check whether 97 is prime. Loop over the possible
   divisors and `break` when you find one.
