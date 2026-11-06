# test_calc.py       run: pytest -q
# Needs pytest:  pip install pytest
# pytest finds files named test_*.py and functions named test_*, and rewrites
# plain `assert` statements so a failure shows both sides of the comparison.
import pytest

from calc import add, div


def test_add():
    assert add(2, 3) == 5


# One test function, many cases: each tuple becomes its own test.
@pytest.mark.parametrize("a,b,r", [(1, 1, 2), (0, 5, 5)])
def test_many(a, b, r):
    assert add(a, b) == r


def test_error():
    # Passes only if the block raises ZeroDivisionError.
    with pytest.raises(ZeroDivisionError):
        div(1, 0)


# A fixture builds something a test needs. pytest injects it by matching the
# argument name, and runs a fresh one for every test.
@pytest.fixture
def client():
    data = {"user": "ada", "balance": 10}
    yield data          # code after `yield` is teardown
    data.clear()


def test_client_fixture(client):
    assert client["user"] == "ada"
    assert div(client["balance"], 2) == 5
