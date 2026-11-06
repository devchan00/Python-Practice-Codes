"""mypkg - a tiny example package.

A folder becomes a *package* when it contains an __init__.py file. This file
runs the first time anything from the package is imported, so it is a good
place to expose the package's public names.
"""

# Re-export so users can write `from mypkg import greet` instead of
# `from mypkg.greetings import greet`. The leading dot means "this package".
from .greetings import greet, shout

__all__ = ["greet", "shout"]   # names exported by `from mypkg import *`
__version__ = "1.0.0"
