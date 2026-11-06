"""Lesson 4.8 - Security basics.

A few habits prevent most security bugs in Python code: use ``secrets`` (not
``random``) for tokens and passwords; never feed untrusted input to ``eval``,
``exec`` or ``pickle`` (use ``ast.literal_eval`` or ``json`` instead); always
use parameterised SQL queries; and run subprocesses with an argument list
instead of ``shell=True``. Scanning tools such as pip-audit and bandit are
covered in README.md. Everything here is a safe, local demo.
"""

import ast
import hashlib
import hmac
import json
import random
import secrets
import sqlite3
import subprocess
import sys


# --- 1. secrets vs random ---
def demo_secrets() -> None:
    print("\n--- 1. secrets vs random ---")
    # `random` is a Mersenne Twister: fast and fine for games/simulations, but
    # PREDICTABLE - after ~624 outputs an attacker can compute the rest.
    rng = random.Random(42)
    print("random with seed 42:", [rng.randint(0, 9) for _ in range(5)])
    # -> always [1, 0, 4, 3, 3]: reproducible = guessable

    # `secrets` uses the OS's cryptographically secure generator.
    print("token_hex(16):", secrets.token_hex(16))  # 32 hex chars, different each run
    print("token_urlsafe(16):", secrets.token_urlsafe(16))  # for reset links, API keys
    print("choice:", secrets.choice(["rock", "paper", "scissors"]))
    alphabet = "abcdefghijkmnpqrstuvwxyz23456789"
    print("password:", "".join(secrets.choice(alphabet) for _ in range(12)))

    # Compare secrets in constant time, so timing doesn't leak how much matched.
    expected = "s3cr3t-token"
    print("compare_digest:", hmac.compare_digest("s3cr3t-token", expected))  # -> True
    # Store passwords as slow salted hashes, never in plain text:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(b"hunter2", salt=salt, n=2**14, r=8, p=1)
    print("scrypt hash length:", len(digest))  # -> 64 (or use argon2/bcrypt libs)


# --- 2. Never eval / exec / pickle untrusted input ---
def demo_eval() -> None:
    print("\n--- 2. eval/exec/pickle vs ast.literal_eval ---")
    user_input = "[1, 2, {'a': 3}]"
    # eval(user_input) would work here... but eval runs ANY expression, e.g.
    #   "__import__('os').system('del /s *')"   <- would really run!
    print("literal_eval:", ast.literal_eval(user_input))  # -> [1, 2, {'a': 3}]

    malicious = "__import__('os').getcwd()"  # harmless stand-in for an attack
    try:
        ast.literal_eval(malicious)  # only literals allowed: no calls, no names
    except ValueError as e:
        print("literal_eval refused:", type(e).__name__)  # -> ValueError

    # For data exchange prefer JSON: it can only describe data, not code.
    print("json:", json.loads('{"ok": true, "n": [1, 2]}'))  # -> {'ok': True, 'n': [1, 2]}
    # pickle.loads(data) can execute arbitrary code chosen by whoever made the
    # bytes (via __reduce__). Only unpickle data YOU created and stored safely.
    # Same for yaml.load -> use yaml.safe_load.


# --- 3. SQL injection vs parameterised queries ---
def demo_sql() -> None:
    print("\n--- 3. SQL: injection vs parameters ---")
    with sqlite3.connect(":memory:") as con:  # in-memory DB: nothing on disk
        cur = con.cursor()
        cur.execute("CREATE TABLE users (name TEXT, secret TEXT)")
        cur.executemany("INSERT INTO users VALUES (?, ?)",
                        [("alice", "a-pass"), ("bob", "b-pass")])

        attack = "nobody' OR '1'='1"

        # BAD: building SQL with string formatting
        unsafe_sql = f"SELECT name, secret FROM users WHERE name = '{attack}'"
        print("unsafe SQL:", unsafe_sql)
        print("unsafe result:", cur.execute(unsafe_sql).fetchall())
        # -> [('alice', 'a-pass'), ('bob', 'b-pass')]  everyone's secrets leaked!

        # GOOD: placeholders. The driver sends the value separately from the
        # SQL, so it can never be interpreted as SQL code.
        safe = cur.execute("SELECT name, secret FROM users WHERE name = ?", (attack,))
        print("safe result:", safe.fetchall())  # -> []  (no user has that odd name)
        named = cur.execute("SELECT name FROM users WHERE name = :n", {"n": "bob"})
        print("named param:", named.fetchall())  # -> [('bob',)]
    con.close()  # the `with` block commits/rolls back; close() releases it


# --- 4. subprocess: list of args, check=True, no shell=True ---
def demo_subprocess() -> None:
    print("\n--- 4. subprocess.run ---")
    filename = "report.txt; rm -rf ~"  # imagine this came from a user
    # With shell=True and a string, the shell would split on ';' and run the
    # second command. With a LIST, each item is one argument - nothing is
    # interpreted by a shell.
    result = subprocess.run(
        [sys.executable, "-c", "import sys; print('got arg:', sys.argv[1])", filename],
        capture_output=True, text=True, check=True, timeout=10,
    )
    print(result.stdout.strip())  # -> got arg: report.txt; rm -rf ~  (just a string)

    # check=True turns a non-zero exit code into an exception instead of
    # silently carrying on.
    try:
        subprocess.run([sys.executable, "-c", "raise SystemExit(3)"], check=True)
    except subprocess.CalledProcessError as e:
        print("failed with exit code", e.returncode)  # -> failed with exit code 3
    # sys.executable = the current Python, so we don't depend on PATH.


def main() -> None:
    demo_secrets()
    demo_eval()
    demo_sql()
    demo_subprocess()


if __name__ == "__main__":
    main()
