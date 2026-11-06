# Lesson 2.9 — Mini project: Quiz app with classes

The cheatsheet's intermediate practice project. A multiple-choice quiz built
from two classes, `Question` and `Quiz`, with the questions stored in
`questions.json`.

## What you'll learn

- How to split a program into small classes with clear jobs
- Loading data from a JSON file located next to the script
- Turning low-level errors into your own exceptions
- Making a program testable and non-interactive by default

## Files

| File | Purpose |
|---|---|
| `example.py` | The quiz app |
| `questions.json` | The questions: `prompt`, `choices`, `answer` (index), `topic` |

## Explanation

- **`Question`** stores one question. `from_dict()` is a `@classmethod`
  constructor used when reading JSON; `correct_choice` is a `@property`;
  `letter_to_index()` is a `@staticmethod` that turns `"b"` into `1`.
- **`Quiz`** holds the questions and the results. `Quiz.from_json(path)` loads
  the file; `score` and `percent` are properties computed from `results`;
  `missed_topics()` uses a set comprehension to list topics to review.
- **Players** are just functions that take a `Question` and return a choice
  index. `auto_player(rng)` returns a closure that answers correctly about 75%
  of the time using a seeded `random.Random`, so the demo output never
  changes. `human_player` asks with `input()`.
- **Errors**: `QuizError` is the base class; `QuestionFormatError` signals a bad
  question. File and JSON problems are re-raised as `QuizError ... from e`,
  and `main()` prints a friendly message and returns exit code `1`.

### Which lessons it uses

| Lesson | Used for |
|---|---|
| 01 Comprehensions | rendering choices, `missed_topics()` set comprehension, list of wrong answers |
| 02 Functional helpers | `sum()` over results, `enumerate`, `", ".join` |
| 03 Arguments & scope | `main(argv=None)`, default arguments, `auto_player` closure |
| 04 Modules & stdlib | `argparse`, `json`, `random`, `pathlib`, `sys`, `__main__` guard |
| 05 Files & JSON | `open(..., encoding="utf-8")` + `json.load` |
| 06 Classes & objects | `Question`, `Quiz`, `__repr__`, `__len__`, `@property`, `@classmethod`, `@staticmethod` |
| 07 Exceptions | `QuizError` hierarchy, `raise ... from e`, handling `ValueError` on bad input |
| 08 Regex & dates | `datetime` formatting with `%Y-%m-%d %H:%M` |

## Common mistakes

- Opening `"questions.json"` with a relative path — it breaks when the script
  is run from another folder. Build it from `Path(__file__).parent`.
- Storing the correct answer as text and comparing strings with different
  case/spaces; an index is more reliable.
- Letting `input()` errors crash the program instead of asking again.

## How to run

```bash
python example.py              # auto-answers, deterministic output
python example.py --seed 5     # a different auto run
python example.py --play       # answer the questions yourself (shuffled)
python example.py --file other.json
```

## Try it yourself

1. Add three questions to `questions.json` — including one with only two choices.
2. Add a `--limit N` option that asks only the first N questions.
3. After the quiz, save the result (`score`, `percent`, missed topics, timestamp)
   to a `results.json` file, appending to a list of previous attempts.
