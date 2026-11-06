# Python Practice Codes

A self-paced Python course that goes from **beginner to professional**. It is built
around [`python_cheatsheet.pdf`](python_cheatsheet.pdf): every section of the
cheatsheet has a lesson folder with runnable code and a plain-language explanation.

## What's inside

```
.
├── python_cheatsheet.pdf   # the cheatsheet the course follows
└── lessons/
    ├── README.md           # how to use the lessons + suggested order
    ├── 00_reference/       # lookup tables: keywords, built-ins, syntax
    ├── 01_beginner/        # the basics
    ├── 02_intermediate/    # writing real programs
    ├── 03_advanced/        # deeper language features
    ├── 04_professional/    # tools and practices for production code
    └── 05_bonus/           # gotchas, Big-O, practice project ideas
```

Each lesson folder contains:

- **`README.md`**: what the lesson covers, the explanation, common mistakes and exercises
- **`example.py`**: runnable sample code, with comments showing the expected output
  (longer lessons split it into `example_1_...py`, `example_2_...py`, and so on)

### Topics by level

| Level | Topics |
|---|---|
| **00 Reference** | Reserved keywords · Soft keywords · Built-in functions · Syntax at a glance (literals, formatting, operator precedence) |
| **01 Beginner** | Variables & types · Operators · Strings · Control flow · Collections · Functions · Input/output, loops & errors · *Mini-project: number-guessing game* |
| **02 Intermediate** | Comprehensions · Functional helpers · Arguments & scope · Modules & packages · Files & JSON · Classes & objects · Exceptions · Regex & dates · *Mini-project: quiz app* |
| **03 Advanced** | Iterators & generators · Decorators & closures · Context managers · Dunder methods · Dataclasses & type hints · Pattern matching · Stdlib power tools · *Mini-project: generator pipeline* |
| **04 Professional** | Concurrency (threads & asyncio) · Testing with pytest · Project tooling (`pyproject.toml`, pre-commit) · Logging · Performance · Internals · Design best practices · Security basics · Ecosystem map · *Mini-project: async web crawler* |
| **05 Bonus** | Common gotchas · Big-O complexity · Practice projects for each level |

## Getting started

You need **Python 3.12 or newer**. The examples use only the standard library,
so there is nothing to install.

```bash
git clone <this-repo-url>
cd "Python Practice Codes/lessons/01_beginner/01_variables_and_types"
python example.py
```

Two lessons come with tests:

```bash
# 04_professional/02_testing_with_pytest (needs pytest)
pip install pytest
pytest

# 04_professional/10_mini_project_async_crawler (standard library only)
python -m unittest -v
```

## Suggested path

1. Start with `lessons/01_beginner/` and work through the folders in order.
2. Read each lesson's `README.md`, run its example, then try the exercises.
3. Finish each level by building its mini-project.
4. Use `lessons/00_reference/` and the cheatsheet PDF as a lookup whenever you need them.

See [`lessons/README.md`](lessons/README.md) for more detail.
