# Lesson 2.8 — Regex & dates

## What you'll learn

- Finding text with `re.search`, `re.match`, `re.fullmatch`
- Getting every match with `re.findall` / `finditer`, replacing with `re.sub`
- Reusing patterns with `re.compile`
- Capture groups: numbered `m.group(1)` and named `(?P<name>...)`
- The current time with `datetime.now()`
- Formatting with `strftime`, parsing with `strptime`
- Date arithmetic with `timedelta`

## Explanation

### Regular expressions

A regex is a tiny language for describing text patterns. Common pieces:
`\d` digit, `\w` word character, `\s` whitespace, `.` any character,
`+` one or more, `*` zero or more, `?` optional, `{3}` exactly three,
`[a-z]` a character class, `^`/`$` start/end, `\b` word boundary.
Always write patterns as raw strings (`r"\d+"`) so Python doesn't treat the
backslashes as escape codes.

```python
m = re.search(r"\d+", "Order 66")       # first match anywhere, or None
m.group()                               # '66'
re.findall(r"\d{3}-\d{4}", text)        # list of all matches
re.sub(r"(\d{3})-\d{4}", r"\1-****", text)   # replace; \1 = group 1
word = re.compile(r"\b[a-z]+\b", re.IGNORECASE)   # reuse
```

`re.match` only matches at the start of the string; `re.fullmatch` requires
the whole string to match (good for validation).

### Groups

Parentheses capture parts of a match:

```python
m = re.search(r"(\w+)@(\w+)\.com", "ada@example.com")
m.group(1), m.group(2)                  # 'ada', 'example'

m = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})", "2024-03")
m["year"], m.groupdict()
```

Quantifiers are greedy (match as much as possible); add `?` (`.+?`) for the
shortest match.

### Dates and times

```python
from datetime import date, datetime, timedelta

datetime.now()                               # current local date-time
dt.strftime("%Y-%m-%d")                      # date -> str
datetime.strptime("15/03/2024", "%d/%m/%Y")  # str -> date
date(2024, 2, 28) + timedelta(days=1)        # 2024-02-29
end - start                                  # a timedelta
```

Useful format codes: `%Y` year, `%m` month, `%d` day, `%H` hour (24h), `%M`
minute, `%S` second, `%A` weekday name, `%B` month name, `%a`/`%b` short names.
`isoformat()` / `fromisoformat()` handle the standard `YYYY-MM-DDTHH:MM:SS` form.
For timestamps shared between machines prefer `datetime.now(timezone.utc)`.

## Common mistakes

- Forgetting the `r` prefix: `"\b"` is a backspace character, `r"\b"` a word boundary.
- Calling `.group()` on `None` when nothing matched — check the result first.
- Using `re.match` when you meant `re.search`.
- Greedy `.*` grabbing far more than intended.
- Mixing up `%m` (month) and `%M` (minute) in format strings.
- Swapping `strftime` (format, "f" for format) and `strptime` ("p" for parse).
- Comparing naive and timezone-aware datetimes (raises `TypeError`).

## How to run

```bash
python example.py
```

## Try it yourself

1. Write a regex that extracts all hashtags (`#python`, `#code`) from a tweet.
2. Validate UK-style dates `DD/MM/YYYY` with `re.fullmatch`, then convert valid
   ones to `YYYY-MM-DD` using `strptime` + `strftime`.
3. Given a birthday as `"1990-07-04"`, compute how many days old the person was
   on `date(2024, 1, 1)`.
