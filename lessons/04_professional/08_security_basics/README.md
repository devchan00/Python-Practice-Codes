# 4.8 Security basics

## What you'll learn

- `secrets` for tokens and passwords - and why `random` is unsafe for them
- Why `eval`, `exec` and `pickle` must never touch untrusted input
  (and the safe alternatives `ast.literal_eval` and `json`)
- SQL injection, and how parameterised queries prevent it
- Running commands safely with `subprocess.run([...], check=True)`
- Scanning tools: `pip-audit` and `bandit`

## Explanation

### secrets, not random

```python
import secrets
secrets.token_hex(16)        # '5465a4a5...' - API keys, session ids
secrets.token_urlsafe(16)    # password-reset links
secrets.choice(alphabet)     # random password characters
hmac.compare_digest(a, b)    # compare tokens in constant time
```

`random` is designed to be fast and reproducible, which also makes it
predictable. Use it for games and simulations only. Store passwords as slow
salted hashes (`hashlib.scrypt`, or the `argon2-cffi` / `bcrypt` packages).

### eval, exec, pickle

`eval("...")` and `exec("...")` run *any* Python code - including
`__import__('os').system(...)`. `pickle.loads` can also run code chosen by
whoever created the bytes. Never use them on data from users, files you didn't
write, or the network.

```python
import ast, json
ast.literal_eval("[1, 2, {'a': 3}]")   # only literals: strings, numbers, lists, dicts...
json.loads('{"ok": true}')              # data-only format
```

### Parameterised SQL

```python
# BAD - user input becomes part of the SQL text
cur.execute(f"SELECT * FROM users WHERE name = '{name}'")
# name = "x' OR '1'='1"  -> returns every row

# GOOD - placeholders; the value is sent separately and never parsed as SQL
cur.execute("SELECT * FROM users WHERE name = ?", (name,))
cur.execute("SELECT * FROM users WHERE name = :n", {"n": name})
```

(`?` is sqlite3's style; psycopg uses `%s`. Either way, never use f-strings.)

### subprocess

```python
subprocess.run(["git", "log", "-n", "5"], check=True)       # good
subprocess.run(f"git log {user_arg}", shell=True)           # bad: shell injection
```

A list passes each item as one argument with no shell parsing, so `;`, `&&`
and `|` are just characters. `check=True` raises `CalledProcessError` on a
non-zero exit code instead of failing silently. Add `timeout=` for safety.

### Scanning tools

```bash
pip install pip-audit bandit
pip-audit                 # checks installed packages against known CVEs
pip-audit -r requirements.txt
bandit -r src/            # static analysis: finds eval, shell=True, weak hashes...
```

Run them in CI (and pre-commit) so problems are caught automatically.

## Common mistakes

- `random.choice` for passwords or tokens.
- f-strings or `%` formatting to build SQL.
- `shell=True` with any user-controlled text.
- Unpickling uploaded files or cached data from shared locations.
- Comparing tokens with `==` (timing leak) - use `hmac.compare_digest`.
- Logging or committing secrets; keep them in environment variables (lesson 4.7).

## How to run

```bash
cd lessons/04_professional/08_security_basics
python example.py
```

## Try it yourself

1. Write `make_password(length=16)` using `secrets` that always includes at least
   one digit and one letter.
2. Add a `search_users(cur, prefix)` function that uses `LIKE` safely
   (hint: `"... WHERE name LIKE ?", (prefix + "%",)`).
3. Write `safe_calc(expr)` that evaluates `"2 + 3 * 4"` by walking `ast.parse`
   nodes and allowing only numbers and `+ - * /`.
