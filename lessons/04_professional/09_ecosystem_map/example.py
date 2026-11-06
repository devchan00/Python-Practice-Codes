"""Lesson 4.9 - Ecosystem map: which libraries do you have?

Python's power comes from its ecosystem. This script walks the cheatsheet's
ecosystem map (web, HTTP, data, ML, databases, CLI, background jobs,
scraping) and uses ``importlib.util.find_spec`` to check which libraries are
installed - WITHOUT importing them, which keeps it fast and side-effect free.
It prints a table, and ``importlib.metadata`` supplies the version when found.
"""

import importlib.metadata
import importlib.util

# --- 1. The map: category -> [(display name, import name, pip name)] ---
# The import name often differs from the pip name (e.g. scikit-learn -> sklearn).
ECOSYSTEM: dict[str, list[tuple[str, str, str]]] = {
    "Web": [("Django", "django", "django"), ("Flask", "flask", "flask"),
            ("FastAPI", "fastapi", "fastapi")],
    "HTTP": [("requests", "requests", "requests"), ("httpx", "httpx", "httpx"),
             ("aiohttp", "aiohttp", "aiohttp")],
    "Data": [("NumPy", "numpy", "numpy"), ("pandas", "pandas", "pandas"),
             ("polars", "polars", "polars")],
    "ML / AI": [("scikit-learn", "sklearn", "scikit-learn"), ("PyTorch", "torch", "torch"),
                ("Transformers", "transformers", "transformers")],
    "Databases": [("SQLAlchemy", "sqlalchemy", "sqlalchemy"), ("sqlite3", "sqlite3", "(stdlib)"),
                  ("psycopg", "psycopg", "psycopg"), ("Alembic", "alembic", "alembic")],
    "CLI": [("argparse", "argparse", "(stdlib)"), ("click", "click", "click"),
            ("typer", "typer", "typer")],
    "Background jobs": [("Celery", "celery", "celery"), ("RQ", "rq", "rq"),
                        ("APScheduler", "apscheduler", "apscheduler")],
    "Scraping / automation": [("BeautifulSoup", "bs4", "beautifulsoup4"),
                              ("Playwright", "playwright", "playwright"),
                              ("Selenium", "selenium", "selenium")],
}


# --- 2. Check without importing ---
def check(import_name: str, pip_name: str) -> tuple[bool, str]:
    """Return (installed?, version-or-note)."""
    # find_spec looks the module up on sys.path but does NOT run it.
    # It returns None when the module can't be found.
    if importlib.util.find_spec(import_name) is None:
        return False, ""
    if pip_name == "(stdlib)":
        return True, "stdlib"
    try:
        return True, importlib.metadata.version(pip_name)  # from the installed metadata
    except importlib.metadata.PackageNotFoundError:
        return True, "?"


# --- 3. Print the table ---
def main() -> None:
    print(f"{'Category':<22} {'Library':<14} {'Status':<10} {'Version':<10} Install with")
    print("-" * 78)
    found = total = 0
    for category, libs in ECOSYSTEM.items():
        for i, (display, import_name, pip_name) in enumerate(libs):
            ok, version = check(import_name, pip_name)
            total += 1
            found += ok
            cat = category if i == 0 else ""  # show the category once per group
            status = "installed" if ok else "missing"
            hint = "" if ok or pip_name == "(stdlib)" else f"pip install {pip_name}"
            print(f"{cat:<22} {display:<14} {status:<10} {version:<10} {hint}")
    print("-" * 78)
    print(f"{found}/{total} installed")  # -> at least 2/25 (sqlite3, argparse are stdlib)


if __name__ == "__main__":
    main()
