# 4.9 Ecosystem map

## What you'll learn

- The go-to libraries for each kind of Python work
- How to check whether a library is installed **without importing it**
  (`importlib.util.find_spec`), and read its version (`importlib.metadata`)
- That the pip name and the import name can differ

## Explanation

### The map

| Area | Libraries | What they're for |
|---|---|---|
| Web | **Django**, **Flask**, **FastAPI** | Django: batteries-included framework (ORM, admin, auth). Flask: small and flexible. FastAPI: modern async APIs driven by type hints, automatic docs. |
| HTTP | **requests**, **httpx**, **aiohttp** | requests: the classic sync client. httpx: requests-like API with sync *and* async + HTTP/2. aiohttp: async client and server. |
| Data | **NumPy**, **pandas**, **polars** | NumPy: fast arrays and maths. pandas: DataFrames for tabular data. polars: a newer, very fast DataFrame library (Rust, lazy queries). |
| ML / AI | **scikit-learn**, **PyTorch**, **Transformers** | scikit-learn: classic ML (regression, trees, clustering). PyTorch: deep learning. Transformers (Hugging Face): pretrained language/vision models. |
| Databases | **SQLAlchemy**, **sqlite3**, **psycopg**, **Alembic** | SQLAlchemy: SQL toolkit + ORM. sqlite3: built-in file database. psycopg: PostgreSQL driver. Alembic: schema migrations for SQLAlchemy. |
| CLI | **argparse**, **click**, **typer** | argparse: in the stdlib. click: decorator-based CLIs. typer: CLIs built from type hints (on top of click). |
| Background jobs | **Celery**, **RQ**, **APScheduler** | Celery: distributed task queue. RQ: simple Redis queue. APScheduler: cron-like scheduling inside your app. |
| Scraping / automation | **BeautifulSoup**, **Playwright**, **Selenium** | BeautifulSoup: parse HTML. Playwright / Selenium: drive a real browser (JS-heavy sites, end-to-end tests). |

### Choosing

- Start with the **standard library** (`sqlite3`, `argparse`, `json`, `csv`,
  `urllib`) - zero dependencies.
- Add a library when it saves real work, and pin it (lesson 4.3).
- Prefer well-maintained, widely used projects; check release dates and
  `pip-audit` (lesson 4.8).

### Checking what's installed

```python
import importlib.util, importlib.metadata

importlib.util.find_spec("numpy")          # ModuleSpec or None - does not import
importlib.metadata.version("numpy")        # '2.1.0' (uses the PIP name)
```

`find_spec` only *locates* the module, so it's fast and can't fail because of
the library's own import errors. Note that the import name and pip name can
differ: `pip install scikit-learn` -> `import sklearn`,
`pip install beautifulsoup4` -> `import bs4`.

From the command line:

```bash
pip list                 # everything installed
pip show httpx           # details for one package
```

## Common mistakes

- `pip install sklearn` / `pip install bs4` - use the real package names.
- Installing into one Python and running another (`python -m pip install ...`
  avoids this).
- Pulling in pandas for something `csv` handles in five lines.
- Using Selenium/Playwright when the site offers an API or plain HTML.

## How to run

```bash
cd lessons/04_professional/09_ecosystem_map
python example.py
```

It prints a table of every library above, marked `installed` or `missing`,
with the pip command for missing ones. Nothing is installed or imported.

## Try it yourself

1. Add a "Testing" row with pytest, hypothesis and tox.
2. Add a `--missing-only` flag (with `argparse`) that hides installed rows.
3. In a venv, `pip install httpx` and run the script again - watch the version appear.
