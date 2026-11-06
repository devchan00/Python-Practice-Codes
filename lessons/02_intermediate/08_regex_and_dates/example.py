"""Lesson 2.8 - Regex & dates.

The re module finds text by pattern: search for the first match, findall for
every match, sub to replace, compile to reuse a pattern, and groups (numbered
or named) to pull out parts of a match. The datetime module represents dates
and times: now() for the current moment, strftime to format a date as text,
strptime to parse text into a date, and timedelta for date arithmetic. Fixed
dates are used throughout so the output is the same every time you run it.
"""

import re
from datetime import date, datetime, timedelta, timezone


# --- 1. re.search: first match or None ---
def searching():
    print("--- 1. re.search ---")
    s = "Order 66 shipped in 3 boxes"
    m = re.search(r"\d+", s)            # r"..." raw string: backslashes stay literal
    print(m.group(), m.start(), m.end())   # -> 66 6 8
    print(re.search(r"\d+", "no digits"))  # -> None
    # Always check for None before using the match:
    if (m := re.search(r"(\d+) boxes", s)):
        print(m.group(1))               # -> 3

    # search finds a match ANYWHERE; match only at the start; fullmatch the whole string.
    print(bool(re.match(r"\d+", s)), bool(re.fullmatch(r"\d+", "123")))   # -> False True


# --- 2. findall, sub, compile ---
def findall_sub_compile():
    print("\n--- 2. re.findall / re.sub / re.compile ---")
    text = "Call 555-1234 or 555-9876. Office: 555-0000."
    print(re.findall(r"\d{3}-\d{4}", text))
    # -> ['555-1234', '555-9876', '555-0000']

    # sub replaces every match. Here: hide the last four digits.
    print(re.sub(r"(\d{3})-\d{4}", r"\1-****", text))
    # -> Call 555-**** or 555-****. Office: 555-****.

    # A function can compute the replacement.
    print(re.sub(r"\d+", lambda m: str(int(m.group()) * 2), "1 apple, 20 pears"))
    # -> 2 apple, 40 pears

    # compile once, reuse many times (clearer, and avoids re-parsing the pattern).
    word = re.compile(r"\b[a-z]+\b", re.IGNORECASE)
    print(word.findall("Hello, World! 42 times"))   # -> ['Hello', 'World', 'times']
    print(re.split(r"[,;]\s*", "a, b;c,  d"))       # -> ['a', 'b', 'c', 'd']


# --- 3. Groups: numbered and named ---
def groups():
    print("\n--- 3. groups ---")
    m = re.search(r"(\w+)@(\w+)\.com", "contact: ada@example.com")
    print(m.group(0))                   # -> ada@example.com  (whole match)
    print(m.group(1), m.group(2))       # -> ada example
    print(m.groups())                   # -> ('ada', 'example')

    # Named groups (?P<name>...) are self-documenting.
    pattern = re.compile(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})")
    m = pattern.search("Released on 2024-03-15.")
    print(m.group("year"), m["month"])  # -> 2024 03
    print(m.groupdict())                # -> {'year': '2024', 'month': '03', 'day': '15'}

    # With groups, findall returns tuples of the groups.
    print(re.findall(r"(\w)=(\d)", "a=1 b=2"))   # -> [('a', '1'), ('b', '2')]

    # Regex quantifiers are GREEDY by default; add ? for the shortest match.
    html = "<b>bold</b><i>it</i>"
    print(re.findall(r"<.+>", html))    # -> ['<b>bold</b><i>it</i>']
    print(re.findall(r"<.+?>", html))   # -> ['<b>', '</b>', '<i>', '</i>']


# --- 4. datetime.now() ---
def now_demo():
    print("\n--- 4. datetime.now() ---")
    now = datetime.now()                # current LOCAL date-time (changes every run)
    print(type(now).__name__)           # -> datetime
    print(now.year >= 2024)             # -> True
    # For timestamps you store or compare across machines, use an aware UTC time.
    utc_now = datetime.now(timezone.utc)
    print(utc_now.tzinfo)               # -> UTC


# --- 5. strftime: date -> str ---
def formatting():
    print("\n--- 5. strftime ---")
    dt = datetime(2024, 3, 15, 14, 30, 5)   # fixed moment -> same output every run
    print(dt.strftime("%Y-%m-%d"))          # -> 2024-03-15
    print(dt.strftime("%d/%m/%Y %H:%M"))    # -> 15/03/2024 14:30
    print(dt.strftime("%A, %B %d"))         # -> Friday, March 15
    print(dt.isoformat())                   # -> 2024-03-15T14:30:05
    print(f"{dt:%H:%M:%S}")                 # -> 14:30:05   (format spec in f-strings)


# --- 6. strptime: str -> date ---
def parsing():
    print("\n--- 6. strptime ---")
    dt = datetime.strptime("15/03/2024 09:05", "%d/%m/%Y %H:%M")
    print(dt)                           # -> 2024-03-15 09:05:00
    print(repr(dt.date()))              # -> datetime.date(2024, 3, 15)
    print(datetime.fromisoformat("2024-12-25T18:00"))   # -> 2024-12-25 18:00:00
    try:
        datetime.strptime("2024-13-01", "%Y-%m-%d")     # month 13
    except ValueError as e:
        print("ValueError:", e)         # -> ValueError: time data '2024-13-01' does not match format '%Y-%m-%d'


# --- 7. timedelta: date arithmetic ---
def arithmetic():
    print("\n--- 7. timedelta ---")
    d = date(2024, 2, 28)
    print(d + timedelta(days=1))        # -> 2024-02-29   (leap year handled for you)
    print(d + timedelta(days=2))        # -> 2024-03-01
    print(d - timedelta(weeks=1))       # -> 2024-02-21

    start = datetime(2024, 3, 15, 9, 0)
    end = datetime(2024, 3, 16, 17, 30)
    gap = end - start                   # subtracting datetimes gives a timedelta
    print(gap)                          # -> 1 day, 8:30:00
    print(gap.total_seconds() / 3600)   # -> 32.5   hours
    print((date(2024, 12, 25) - date(2024, 3, 15)).days)   # -> 285 days until Christmas
    print(date(2024, 3, 15).weekday())  # -> 4   (Monday is 0, so 4 = Friday)


# --- 8. Combining regex and dates ---
def combined():
    print("\n--- 8. regex + dates ---")
    log = "2024-03-15 ERROR disk full\n2024-03-18 INFO ok\n2024-03-20 ERROR timeout"
    pattern = re.compile(r"^(?P<day>\d{4}-\d{2}-\d{2}) ERROR (?P<msg>.+)$", re.MULTILINE)
    for m in pattern.finditer(log):
        day = datetime.strptime(m["day"], "%Y-%m-%d").date()
        print(day.strftime("%a %d %b"), "-", m["msg"])
    # -> Fri 15 Mar - disk full
    # -> Wed 20 Mar - timeout


if __name__ == "__main__":
    searching()
    findall_sub_compile()
    groups()
    now_demo()
    formatting()
    parsing()
    arithmetic()
    combined()
