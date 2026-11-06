"""Built-in functions, part 3: objects, classes, I/O and introspection.

This file covers built-ins for working with objects and the running program:
type, isinstance, issubclass, object, callable, id, dir, vars, getattr /
setattr / hasattr, globals / locals, the class helpers classmethod,
staticmethod, property and super, plus print, open, __import__, and the
"use with care" functions eval / exec. breakpoint(), input() and help() are
interactive, so they are only shown in comments.
"""

import os
import tempfile


# --- 1. type / isinstance / issubclass / object ---
class Animal:
    pass


class Dog(Animal):
    pass


def demo_types():
    d = Dog()
    print(type(d))                          # -> <class '__main__.Dog'>
    print(type(d) is Animal)                # -> False  type() is exact
    print(isinstance(d, Animal))            # -> True   isinstance includes subclasses
    print(isinstance(3, (int, float)))      # -> True   a tuple means "any of these"
    print(issubclass(Dog, Animal))          # -> True
    print(issubclass(Dog, object))          # -> True   object is the base of ALL classes
    sentinel = object()                     # a unique value nothing else equals
    print(sentinel == object())             # -> False

    # type(name, bases, dict) can also BUILD a class on the fly:
    Cat = type("Cat", (Animal,), {"sound": "meow"})
    print(Cat.__name__, Cat().sound)        # -> Cat meow


# --- 2. callable / id ---
def demo_callable_id():
    print(callable(print), callable(42))    # -> True False
    print(callable(Dog))                    # -> True  (calling a class creates an object)
    a = [1]
    b = a
    print(id(a) == id(b))                   # -> True  same object, same identity number
    print(id(a) == id([1]))                 # -> False a different (equal) list


# --- 3. dir / vars / getattr / setattr / hasattr ---
class Config:
    def __init__(self):
        self.debug = False
        self.level = 1


def demo_attributes():
    c = Config()
    print(vars(c))                          # -> {'debug': False, 'level': 1}  (= c.__dict__)
    print([n for n in dir(c) if not n.startswith("_")])   # -> ['debug', 'level']
    # Dynamic access: the attribute NAME is a string decided at runtime.
    print(getattr(c, "level"))              # -> 1
    print(getattr(c, "color", "none"))      # -> none   default if missing
    setattr(c, "level", 5)
    print(c.level)                          # -> 5
    print(hasattr(c, "debug"), hasattr(c, "x"))   # -> True False


# --- 4. globals / locals: namespace dicts ---
GREETING = "hello"


def demo_namespaces():
    x = 10
    print(locals())                         # -> {'x': 10}
    print(globals()["GREETING"])            # -> hello
    print("demo_namespaces" in globals())   # -> True  (functions live there too)


# --- 5. classmethod / staticmethod / property / super ---
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property                               # managed attribute: looks like data, runs code
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._celsius = value

    @classmethod                            # gets the CLASS (cls), handy for alt. constructors
    def from_fahrenheit(cls, f):
        return cls((f - 32) * 5 / 9)

    @staticmethod                           # gets neither self nor cls: a plain helper
    def is_freezing(c):
        return c <= 0


class LoggedTemperature(Temperature):
    def __init__(self, celsius):
        super().__init__(celsius)           # super() calls the PARENT version
        print("  created", celsius)


def demo_class_helpers():
    t = Temperature.from_fahrenheit(212)
    print(t.celsius)                        # -> 100.0
    t.celsius = 25                          # goes through the setter
    print(t.celsius)                        # -> 25
    try:
        t.celsius = -300
    except ValueError as e:
        print("ValueError:", e)             # -> below absolute zero
    print(Temperature.is_freezing(-5))      # -> True
    LoggedTemperature(7)                    # ->   created 7


# --- 6. print / open ---
def demo_print_open():
    print("a", "b", "c", sep="-", end="!\n")   # -> a-b-c!
    print(*[1, 2, 3])                       # -> 1 2 3   (* unpacks the list)

    # open(path, mode): 'r' read, 'w' write (overwrite), 'a' append, 'b' binary.
    with tempfile.TemporaryDirectory() as folder:   # no leftover files
        path = os.path.join(folder, "demo.txt")
        with open(path, "w", encoding="utf-8") as f:
            print("line one", file=f)       # print can write to a file too
        with open(path, "a", encoding="utf-8") as f:
            f.write("line two\n")
        with open(path, encoding="utf-8") as f:
            print(f.read().splitlines())    # -> ['line one', 'line two']


# --- 7. __import__: low-level import ---
def demo_dunder_import():
    m = __import__("math")                  # what the `import` statement uses internally
    print(m.pi)                             # -> 3.141592653589793
    # In real code prefer `import math` or importlib.import_module("math").


# --- 8. eval / exec: run code strings (AVOID!) ---
def demo_eval_exec():
    # WARNING: eval/exec run ANY code. Never pass them text from users, files or
    # the network - that lets someone run arbitrary commands on your machine.
    # For parsing literal data safely use ast.literal_eval or json.loads instead.
    print(eval("2 + 3 * 4"))                # -> 14     eval evaluates ONE expression
    namespace = {}
    exec("def sq(n):\n    return n * n", namespace)   # exec runs statements
    print(namespace["sq"](9))               # -> 81

    import ast
    print(ast.literal_eval("[1, 2, {'a': 3}]"))   # -> [1, 2, {'a': 3}]  the safe way


# --- 9. Interactive built-ins (not run here) ---
def demo_interactive_comments():
    # breakpoint()            -> pauses and opens the pdb debugger at this line
    # name = input("Name: ")  -> waits for the user to type; ALWAYS returns a str,
    #                            so convert: age = int(input("Age: "))
    # help(len)               -> shows built-in documentation (best in the REPL)
    print("breakpoint(), input() and help() are shown in comments only")


if __name__ == "__main__":
    print("--- 1. types ---");            demo_types()
    print("--- 2. callable/id ---");      demo_callable_id()
    print("--- 3. attributes ---");       demo_attributes()
    print("--- 4. namespaces ---");       demo_namespaces()
    print("--- 5. class helpers ---");    demo_class_helpers()
    print("--- 6. print/open ---");       demo_print_open()
    print("--- 7. __import__ ---");       demo_dunder_import()
    print("--- 8. eval/exec ---");        demo_eval_exec()
    print("--- 9. interactive ---");      demo_interactive_comments()
