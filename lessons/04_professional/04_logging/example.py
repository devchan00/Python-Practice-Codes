"""Lesson 4.4 - Logging.

``print`` is for the user; ``logging`` is for the developer and operator.
Log records carry a level (DEBUG..CRITICAL), a logger name, a timestamp and
optionally a traceback, and handlers decide where they go (console, file,
network) without changing the code that logs. This lesson covers
``basicConfig``, ``getLogger(__name__)``, lazy %-formatting, ``log.exception``,
levels, logger hierarchy and a ``FileHandler`` writing into a temp directory.
"""

import logging
import sys
import tempfile
from pathlib import Path

# A module-level logger named after the module: "__main__" here, or
# "myapp.db" inside a package. The dotted name forms a hierarchy.
log = logging.getLogger(__name__)


# --- 1. basicConfig: one-time setup of the ROOT logger ---
def setup() -> None:
    print("\n--- 1. basicConfig ---")
    logging.basicConfig(
        level=logging.INFO,  # ignore anything below INFO
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout,  # default is stderr; stdout keeps the demo output in order
        force=True,  # replace any previous config (handy in notebooks/demos)
    )
    log.info("logging configured")  # -> 12:00:00 INFO __main__: logging configured
    # Call basicConfig ONCE, in the program's entry point - never in a library.


# --- 2. Levels ---
def demo_levels() -> None:
    print("\n--- 2. Levels ---")
    log.debug("hidden: DEBUG(10) < INFO(20)")  # not shown
    log.info("normal progress")  # -> INFO
    log.warning("something odd, but we carry on")  # -> WARNING
    log.error("an operation failed")  # -> ERROR
    log.critical("the program may not continue")  # -> CRITICAL
    log.setLevel(logging.DEBUG)
    log.debug("now visible: this logger's level was lowered")  # -> DEBUG
    log.setLevel(logging.NOTSET)  # back to "inherit from parent"
    print("isEnabledFor(DEBUG):", log.isEnabledFor(logging.DEBUG))  # -> False


# --- 3. Lazy %-formatting ---
class Expensive:
    def __str__(self) -> str:
        print("    (Expensive.__str__ was called)")
        return "expensive-object"


def demo_lazy() -> None:
    print("\n--- 3. Lazy %-formatting ---")
    name = "ada"
    log.info("started %s", name)  # GOOD: formatted only if the record is emitted
    # log.info(f"started {name}")   works, but always builds the string first

    print("  debug with args (filtered out, so __str__ never runs):")
    log.debug("value is %s", Expensive())  # -> nothing printed
    print("  debug with f-string (string built even though it's discarded):")
    log.debug(f"value is {Expensive()}")  # -> (Expensive.__str__ was called)


# --- 4. log.exception: include the traceback ---
def demo_exception() -> None:
    print("\n--- 4. log.exception ---")
    try:
        1 / 0
    except ZeroDivisionError:
        # Same as log.error(..., exc_info=True). Only use inside an except block.
        log.exception("failed to compute ratio")
    # -> ERROR __main__: failed to compute ratio
    #    Traceback (most recent call last): ... ZeroDivisionError: division by zero


# --- 5. Logger hierarchy ---
def demo_hierarchy() -> None:
    print("\n--- 5. Hierarchy ---")
    app_log = logging.getLogger("myapp")
    db_log = logging.getLogger("myapp.db")  # child of "myapp" (dotted name)
    http_log = logging.getLogger("myapp.http")
    print("parent of myapp.db:", db_log.parent.name)  # -> myapp
    print("parent of myapp:", app_log.parent.name)  # -> root
    app_log.setLevel(logging.WARNING)  # quiet the whole app subtree...
    db_log.info("hidden")  # inherited WARNING level -> not shown
    http_log.warning("shown")  # -> WARNING myapp.http: shown
    # Typical use: logging.getLogger("urllib3").setLevel(logging.WARNING)
    # to silence a chatty third-party library.


# --- 6. A FileHandler (in a temp dir, so no files are left behind) ---
def demo_file_handler() -> None:
    print("\n--- 6. FileHandler ---")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "app.log"
        handler = logging.FileHandler(path, encoding="utf-8")
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter("%(levelname)s|%(name)s|%(message)s"))

        file_log = logging.getLogger("myapp.file")
        file_log.setLevel(logging.DEBUG)
        file_log.addHandler(handler)
        file_log.propagate = False  # don't ALSO send these to the console handler

        file_log.debug("written to the file only")
        file_log.info("user %s logged in", "ada")

        handler.close()  # flush + release the file (needed on Windows before delete)
        file_log.removeHandler(handler)
        print(path.read_text(encoding="utf-8"), end="")
        # -> DEBUG|myapp.file|written to the file only
        # -> INFO|myapp.file|user ada logged in
    # For long-running apps see logging.handlers.RotatingFileHandler.


def main() -> None:
    setup()
    demo_levels()
    demo_lazy()
    demo_exception()
    demo_hierarchy()
    demo_file_handler()


if __name__ == "__main__":
    main()
