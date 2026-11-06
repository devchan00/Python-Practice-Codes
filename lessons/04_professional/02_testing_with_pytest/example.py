"""Lesson 4.2 - Testing: the same checks with stdlib unittest + unittest.mock.

``test_calc.py`` shows the pytest style from the cheatsheet, but pytest is a
third-party package. This file runs the same checks using only the standard
library: ``unittest.TestCase`` methods replace plain asserts, ``subTest``
replaces ``parametrize``, ``assertRaises`` replaces ``pytest.raises`` and
``setUp``/``tearDown`` replace a fixture. It also shows ``unittest.mock`` for
isolating code from slow or unreliable dependencies.
"""

import unittest
from unittest import mock

from calc import add, div


# --- 1. Plain checks (pytest: `assert add(2, 3) == 5`) ---
class TestAdd(unittest.TestCase):
    def test_add(self) -> None:
        self.assertEqual(add(2, 3), 5)

    # --- 2. Many cases (pytest: @pytest.mark.parametrize) ---
    def test_many(self) -> None:
        for a, b, r in [(1, 1, 2), (0, 5, 5)]:
            with self.subTest(a=a, b=b):  # a failure reports WHICH case failed
                self.assertEqual(add(a, b), r)


# --- 3. Expected exceptions (pytest: `with pytest.raises(...)`) ---
class TestDiv(unittest.TestCase):
    def test_error(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            div(1, 0)

    def test_float(self) -> None:
        # Floats: compare with a tolerance, never with ==
        self.assertAlmostEqual(div(1, 3), 0.3333333, places=6)


# --- 4. Fixtures (pytest: @pytest.fixture) -> setUp / tearDown ---
class TestWithFixture(unittest.TestCase):
    def setUp(self) -> None:  # runs before EVERY test method
        self.client = {"user": "ada", "balance": 10}

    def tearDown(self) -> None:  # runs after every test, even failing ones
        self.client.clear()

    def test_client(self) -> None:
        self.assertEqual(self.client["user"], "ada")
        self.assertEqual(div(self.client["balance"], 2), 5)


# --- 5. unittest.mock: isolate dependencies ---
def get_price(api, symbol: str) -> float:
    """Code under test: depends on a (slow, networked) API object."""
    data = api.fetch(symbol)
    return round(data["price"] * 1.1, 2)


class TestMock(unittest.TestCase):
    def test_with_mock_object(self) -> None:
        fake_api = mock.Mock()
        fake_api.fetch.return_value = {"price": 100.0}  # canned answer
        self.assertEqual(get_price(fake_api, "ACME"), 110.0)
        # Mocks record how they were called, so we can check the interaction:
        fake_api.fetch.assert_called_once_with("ACME")

    def test_patch(self) -> None:
        # patch() temporarily replaces a name, and restores it afterwards.
        with mock.patch("calc.add", return_value=42) as fake_add:
            import calc
            self.assertEqual(calc.add(1, 1), 42)
            fake_add.assert_called_once()
        self.assertEqual(add(1, 1), 2)  # the real function is back

    def test_side_effect(self) -> None:
        fake_api = mock.Mock()
        fake_api.fetch.side_effect = ConnectionError("down")  # simulate failure
        with self.assertRaises(ConnectionError):
            get_price(fake_api, "ACME")


def main() -> None:
    # verbosity=2 prints one line per test, e.g. "test_add ... ok"
    suite = unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print("all passed:", result.wasSuccessful())  # -> all passed: True


if __name__ == "__main__":
    main()
