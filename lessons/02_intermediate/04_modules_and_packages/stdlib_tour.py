"""Lesson 2.4 (part 2) - A brief tour of the standard library.

Python's "batteries included" standard library covers most everyday needs
without installing anything: the OS and interpreter (os, sys, pathlib), data
formats (json, csv, re), dates and numbers (datetime, time, random, math), and
command-line programs (argparse, logging, subprocess). Each function below is
a one-minute taste of one module. Run directly or via example.py.
"""

import argparse
import csv
import datetime
import io
import json
import logging
import math
import os
import pathlib
import random
import re
import subprocess
import sys
import time


def tour_os_sys_pathlib():
    print("\n--- 4. os / sys / pathlib ---")
    # os: talk to the operating system (env vars, cwd, path separators).
    print(os.sep in ("/", "\\"))                # -> True
    print(os.environ.get("NO_SUCH_VAR", "default"))   # -> default
    # sys: the running interpreter.
    print(sys.version_info >= (3, 12))          # -> True
    print(type(sys.argv).__name__)              # -> list  (command-line args)
    # pathlib: object-oriented paths. Path(__file__) is this file.
    here = pathlib.Path(__file__).resolve()
    print(here.name, here.suffix)               # -> stdlib_tour.py .py
    print((here.parent / "mypkg" / "__init__.py").exists())   # -> True  (/ joins paths)


def tour_json_csv_re():
    print("\n--- 5. json / csv / re ---")
    print(json.loads('{"a": [1, 2]}')["a"])     # -> [1, 2]
    # csv works with any file-like object; io.StringIO is an in-memory file.
    buf = io.StringIO("name,age\nann,31\nbob,25\n")
    rows = list(csv.DictReader(buf))
    print(rows[1]["name"], rows[1]["age"])      # -> bob 25   (csv values are strings)
    print(re.findall(r"\d+", "a1 b22 c333"))    # -> ['1', '22', '333']


def tour_dates_numbers():
    print("\n--- 6. datetime / time / random / math ---")
    d = datetime.date(2024, 3, 15)              # fixed date -> deterministic output
    print(d + datetime.timedelta(days=20))      # -> 2024-04-04
    start = time.perf_counter()                 # high-resolution timer for measuring
    sum(range(10_000))
    print(time.perf_counter() - start >= 0)     # -> True
    rng = random.Random(42)                     # seeded -> same "random" numbers every run
    print(rng.randint(1, 100), rng.choice("abc"))   # -> 82 a
    print(math.gcd(12, 18), math.isclose(0.1 + 0.2, 0.3))   # -> 6 True


def tour_argparse():
    print("\n--- 7. argparse ---")
    parser = argparse.ArgumentParser(description="Greet someone")
    parser.add_argument("name")
    parser.add_argument("--times", type=int, default=1)
    parser.add_argument("-v", "--verbose", action="store_true")
    # Normally you call parser.parse_args() to read sys.argv. Passing a list
    # makes the demo deterministic.
    args = parser.parse_args(["Ada", "--times", "2", "-v"])
    print(args)                     # -> Namespace(name='Ada', times=2, verbose=True)
    print(args.times * 2)           # -> 4   (already converted to int)


def tour_logging():
    print("\n--- 8. logging ---")
    # A named logger, sending to stdout so the output appears in order here.
    log = logging.getLogger("tour")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    log.propagate = False
    log.debug("hidden")             # below INFO, not shown
    log.info("started")             # -> INFO:tour:started
    log.warning("disk %d%% full", 91)   # -> WARNING:tour:disk 91% full
    log.removeHandler(handler)
    # WHY not print? Levels can be switched on/off, and output can go to
    # files or services without changing the calling code.


def tour_subprocess():
    print("\n--- 9. subprocess ---")
    # Run another program. Pass a LIST of arguments (no shell=True), so there
    # is no shell-injection risk. sys.executable is the current Python.
    result = subprocess.run(
        [sys.executable, "-c", "print('hi')"],
        capture_output=True, text=True, check=True, timeout=10,
    )
    print(result.returncode, result.stdout.strip())   # -> 0 hi


def run_all():
    tour_os_sys_pathlib()
    tour_json_csv_re()
    tour_dates_numbers()
    tour_argparse()
    tour_logging()
    tour_subprocess()


if __name__ == "__main__":
    run_all()
