"""Entry point: `python -m myapp [name]` runs main()."""

import sys

from myapp import __version__, greet


def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else "world"
    print(greet(name), f"(myapp {__version__})")


if __name__ == "__main__":
    main()
