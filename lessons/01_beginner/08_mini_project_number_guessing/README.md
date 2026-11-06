# Mini-project: Number-Guessing Game

The cheatsheet's first beginner practice project. The computer picks a secret
number from 1 to 100, and the player guesses until they find it, getting a
"too low" or "too high" hint after each guess.

## What you'll learn

- How to combine the beginner lessons into one small, complete program
- Binary search: why "guess the middle" finds any number from 1 to 100 in at
  most 7 guesses
- How a fixed random seed makes a "random" program repeatable
- How to read a command-line flag with `sys.argv`

## Explanation

By default the script **plays itself**, so it runs without any typing:

1. `random.Random(42)` creates a random generator with a fixed seed, so the
   secret number is the same on every run (82).
2. The computer player always guesses the middle of the range that's still
   possible: `(low + high) // 2`.
3. After "too low", the bottom of the range moves up to `guess + 1`. After
   "too high", the top moves down to `guess - 1`. Each guess halves the
   remaining range, and since 2⁷ = 128 ≥ 100, seven guesses always suffice.
4. A self-test tries all 100 possible secrets and confirms that the worst
   case is 7 guesses.

With `--play`, a human plays instead. Each guess is read with `input()` and
checked inside `try` / `except ValueError`, so typing `abc` doesn't crash
the game.

### Where each lesson shows up

| Lesson | Used for |
|--------|----------|
| 01 Variables and types | `LOW`, `HIGH`, `SEED` constants; `int(text)` conversion |
| 02 Operators | `(low + high) // 2`, the chained check `LOW <= number <= HIGH`, `"--play" in sys.argv` |
| 03 Strings | f-string with `{guess:>3}`, `", ".join(...)`, `.strip()`, `!r` |
| 04 Control flow | `while True` with `break` and `continue`, `if`/`elif`/`else`, a ternary for the hint |
| 05 Collections | a list holds the guess history; a dict holds the search range and maps results to hint text |
| 06 Functions | `check_guess`, `read_int`, and `computer_player`, which returns two functions |
| 07 I/O and errors | `input()`, `print()`, `range()`, `try`/`except` for bad input and Ctrl+C |

## Common mistakes

- Using `/` instead of `//` for the middle, which gives a float such as `50.5`.
- Updating the range to `guess` instead of `guess + 1` or `guess - 1`. The
  search can then get stuck guessing the same number forever.
- Forgetting to convert `input()` to `int`. Then `"50" < 82` raises a
  `TypeError`.
- Calling `random.seed()` in interactive mode. The human player would face
  the same secret every game.

## How to run

```bash
python example.py          # the computer plays itself (no input needed)
python example.py --play   # you play: type guesses, Ctrl+C to quit
```

## Try it yourself

1. Add a difficulty setting: easy (1–10), normal (1–100), and hard
   (1–1000). How many guesses does binary search need in the worst case
   for each?
2. In `--play` mode, limit the player to 7 tries and print "You lose" if
   they run out.
3. Write a "dumb" computer player that guesses randomly within the remaining
   range. Compare its average number of guesses over all 100 secrets with
   binary search.
