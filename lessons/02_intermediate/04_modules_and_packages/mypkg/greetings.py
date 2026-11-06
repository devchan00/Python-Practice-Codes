"""mypkg.greetings - a module inside the mypkg package."""

DEFAULT_GREETING = "Hello"


def greet(name, greeting=DEFAULT_GREETING):
    """Return a friendly greeting."""
    return f"{greeting}, {name}!"


def shout(name):
    """Return the greeting in capitals."""
    return greet(name).upper()


# This block runs only when the file is executed directly, e.g.
#   python mypkg/greetings.py
# and NOT when it is imported by example.py.
if __name__ == "__main__":
    print("greetings.py run directly:", greet("world"))
