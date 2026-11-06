# 4.2 Testing with pytest (and unittest)

## What you'll learn

- Writing tests with **pytest**: plain `assert`, `@pytest.mark.parametrize`,
  `pytest.raises`, and fixtures
- The same ideas with the standard-library **unittest** (works with no installs)
- Isolating dependencies with **unittest.mock** (`Mock`, `patch`, `side_effect`)
- The wider toolbox: pytest-cov, hypothesis, tox/nox

## Files

| File | What it is |
|---|---|
| `calc.py` | The code under test: `add()` and `div()` |
| `test_calc.py` | pytest tests, exactly as on the cheatsheet (needs pytest) |
| `example.py` | The same checks with `unittest` + `unittest.mock` (stdlib only) |

## Explanation

### Why test?

A test is a small program that checks your program. Once written it runs in
milliseconds, forever, so you can change code without fear of breaking it.

### pytest basics

```python
# test_calc.py       run: pytest -q
import pytest
from calc import add, div

def test_add():
    assert add(2, 3) == 5          # plain assert; pytest shows both sides on failure
```

pytest discovers files called `test_*.py` and functions called `test_*`.

### Parametrize: one test, many cases

```python
@pytest.mark.parametrize("a,b,r", [(1, 1, 2), (0, 5, 5)])
def test_many(a, b, r):
    assert add(a, b) == r
```

Each tuple is reported as a separate test, so you see exactly which case failed.

### Expecting an exception

```python
def test_error():
    with pytest.raises(ZeroDivisionError):
        div(1, 0)
```

### Fixtures

```python
@pytest.fixture
def client():
    c = make_client()
    yield c            # the test runs here
    c.close()          # teardown

def test_thing(client):   # pytest passes the fixture in by argument name
    ...
```

Fixtures keep setup code out of tests and give every test a fresh object.

### The unittest equivalents

| pytest | unittest |
|---|---|
| `assert x == y` | `self.assertEqual(x, y)` |
| `@pytest.mark.parametrize` | `for ...: with self.subTest(...):` |
| `pytest.raises(E)` | `self.assertRaises(E)` |
| `@pytest.fixture` | `setUp()` / `tearDown()` |

pytest can run unittest-style tests too, so you can switch later.

### unittest.mock

```python
from unittest import mock
api = mock.Mock()
api.fetch.return_value = {"price": 100.0}     # canned answer
api.fetch.side_effect = ConnectionError()     # or: simulate failure
api.fetch.assert_called_once_with("ACME")     # check how it was used

with mock.patch("module.name", return_value=42):   # temporary replacement
    ...
```

Mocks let you test your logic without the network, a database or the clock.
Patch the name **where it is looked up**, e.g. `mock.patch("myapp.views.requests")`.

### The wider toolbox

```bash
pip install pytest          # the test runner
pytest -q                   # run all tests, quiet output
pytest -k many              # only tests whose name matches "many"
pip install pytest-cov
pytest --cov=calc --cov-report=term-missing   # coverage: which lines never ran
pip install hypothesis      # property-based testing (generates inputs for you)
pip install tox nox         # run the suite across several Python versions/envs
```

A hypothesis test looks like this:

```python
from hypothesis import given, strategies as st

@given(st.integers(), st.integers())
def test_add_commutes(a, b):
    assert add(a, b) == add(b, a)
```

## Common mistakes

- Naming the file `calc_test.py` or the function `check_add` - pytest won't find it.
- Comparing floats with `==` (use `pytest.approx` or `assertAlmostEqual`).
- Tests that depend on each other or on run order; each test should set up its own data.
- Patching the name where it is *defined* instead of where it is *used*.
- Testing only the happy path - also test errors and edge cases (0, empty, None).

## How to run

```bash
cd lessons/04_professional/02_testing_with_pytest

# No installs needed:
python example.py
python -m unittest example -v

# With pytest:
pip install pytest
pytest -q
```

Note: plain `python -m unittest` (auto-discovery) would also try to import
`test_calc.py`, which fails if pytest is not installed. Name the module as above.

## Try it yourself

1. Add a `mul(a, b)` function to `calc.py` and test it with three parametrized cases.
2. Make `div` raise `ValueError("cannot divide by zero")` instead, and update both
   test files. Use `pytest.raises(ValueError, match="zero")`.
3. Write a function `greet(clock)` that returns "Good morning" before 12:00 and
   "Good afternoon" after, where `clock()` returns the hour. Test both branches with a `Mock`.
