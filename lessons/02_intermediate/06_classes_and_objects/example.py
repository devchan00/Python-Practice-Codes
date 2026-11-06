"""Lesson 2.6 - Classes & objects.

A class bundles data (attributes) and behaviour (methods) into a new type;
each object created from it is an instance. This lesson covers __init__ and
self, class vs instance attributes, inheritance and super(), __repr__ for
readable debugging output, @property for computed or validated attributes,
@classmethod for alternative constructors, @staticmethod for helpers, the
_x / __x naming conventions, and multiple inheritance with the MRO.
"""


# --- 1. A basic class, __init__ and self ---
class Animal:
    kingdom = "animalia"                # class attribute: shared by ALL instances

    def __init__(self, name):           # constructor: runs when Animal(...) is called
        self.name = name                # instance attribute: one per object

    def speak(self):
        return f"{self.name} makes a sound"


def basics():
    print("--- 1. class, __init__, self ---")
    a = Animal("Generic")
    print(a.speak())                    # -> Generic makes a sound
    # a.speak() is shorthand for Animal.speak(a): 'self' is the instance.
    print(Animal.speak(a))              # -> Generic makes a sound
    print(isinstance(a, Animal))        # -> True


# --- 2. Class vs instance attributes ---
def class_vs_instance():
    print("\n--- 2. class vs instance attributes ---")
    a, b = Animal("a"), Animal("b")
    print(a.kingdom, b.kingdom)         # -> animalia animalia  (looked up on the class)

    a.kingdom = "custom"                # creates an INSTANCE attribute that hides the class one
    print(a.kingdom, b.kingdom)         # -> custom animalia
    Animal.kingdom = "changed"          # changing the class affects instances without their own
    print(a.kingdom, b.kingdom)         # -> custom changed
    Animal.kingdom = "animalia"         # restore for the rest of the demo

    print(a.__dict__)                   # -> {'name': 'a', 'kingdom': 'custom'}

    # Gotcha: a MUTABLE class attribute is shared by every instance.
    class Bad:
        tricks = []                     # one list for all Bad objects!
    x, y = Bad(), Bad()
    x.tricks.append("roll")
    print(y.tricks)                     # -> ['roll']   put mutable state in __init__ instead


# --- 3. Inheritance, super() and __repr__ ---
class Dog(Animal):                      # Dog IS-A Animal
    species = "canis"

    def __init__(self, name, breed="mutt"):
        super().__init__(name)          # let the parent set up self.name
        self.breed = breed

    def speak(self):                    # override the parent's method
        return f"{self.name}: woof"

    def __repr__(self):                 # unambiguous, developer-facing text
        return f"Dog({self.name!r}, breed={self.breed!r})"


class Puppy(Dog):
    def speak(self):
        # super() calls the next class's version, then we extend it.
        return super().speak() + " (squeaky)"


def inheritance():
    print("\n--- 3. inheritance, super(), __repr__ ---")
    d = Dog("Rex", "lab")
    print(d.speak())                    # -> Rex: woof
    print(d.kingdom, d.species)         # -> animalia canis  (inherited + own class attr)
    print(d)                            # -> Dog('Rex', breed='lab')   print uses __repr__ when no __str__
    print([d])                          # -> [Dog('Rex', breed='lab')]  containers always use __repr__
    print(Animal("x"))                  # -> <__main__.Animal object at 0x...>  (default repr)
    print(Puppy("Bit").speak())         # -> Bit: woof (squeaky)
    print(isinstance(d, Animal), issubclass(Puppy, Animal))   # -> True True


# --- 4. @property ---
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius          # goes through the setter below (validation!)

    @property
    def celsius(self):                  # getter: t.celsius
        return self._celsius

    @celsius.setter
    def celsius(self, value):           # setter: t.celsius = value
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self):               # read-only computed attribute
        return self._celsius * 9 / 5 + 32


def properties():
    print("\n--- 4. @property ---")
    t = Temperature(25)
    print(t.celsius, t.fahrenheit)      # -> 25 77.0   (no parentheses: looks like an attribute)
    t.celsius = 100
    print(t.fahrenheit)                 # -> 212.0
    try:
        t.celsius = -300
    except ValueError as e:
        print("ValueError:", e)         # -> ValueError: below absolute zero
    try:
        t.fahrenheit = 0                # no setter defined
    except AttributeError:
        print("fahrenheit is read-only")   # -> fahrenheit is read-only
    # WHY: start with plain attributes; switch to a property later if you
    # need validation, and callers' code doesn't have to change.


# --- 5. @classmethod and @staticmethod ---
class Date:
    def __init__(self, year, month, day):
        self.year, self.month, self.day = year, month, day

    @classmethod
    def from_string(cls, text):         # receives the CLASS: an alternative constructor
        y, m, d = map(int, text.split("-"))
        return cls(y, m, d)             # cls (not Date) so subclasses get their own type

    @staticmethod
    def is_leap(year):                  # receives nothing: a helper grouped with the class
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def __repr__(self):
        return f"{type(self).__name__}({self.year}, {self.month}, {self.day})"


class FancyDate(Date):
    pass


def class_and_static():
    print("\n--- 5. @classmethod / @staticmethod ---")
    print(Date.from_string("2024-03-15"))        # -> Date(2024, 3, 15)
    print(FancyDate.from_string("2000-01-01"))   # -> FancyDate(2000, 1, 1)
    print(Date.is_leap(2024), Date.is_leap(1900))   # -> True False


# --- 6. _x (internal) and __x (name-mangled) ---
class Account:
    def __init__(self, owner, balance):
        self.owner = owner              # public
        self._balance = balance         # "internal, please don't touch" (convention only)
        self.__pin = "1234"             # name-mangled to _Account__pin

    def check_pin(self, pin):
        return pin == self.__pin        # inside the class the short name works


def private_names():
    print("\n--- 6. _x and __x ---")
    acct = Account("ann", 100)
    print(acct._balance)                # -> 100   (allowed, but a signal you shouldn't)
    try:
        print(acct.__pin)
    except AttributeError:
        print("no attribute __pin from outside")   # -> no attribute __pin from outside
    print(acct._Account__pin)           # -> 1234  (mangling is not real security)
    print(acct.check_pin("1234"))       # -> True
    # WHY __x exists: to stop SUBCLASSES accidentally overwriting a parent's
    # attribute with the same name, not to hide secrets.


# --- 7. Multiple inheritance and the MRO ---
class Walker:
    def move(self):
        return "walk"

    def describe(self):
        return "Walker"


class Swimmer:
    def move(self):
        return "swim"

    def describe(self):
        return "Swimmer"


class Duck(Walker, Swimmer):            # order matters: Walker is searched first
    def describe(self):
        # super() follows the MRO, so this calls Walker.describe
        return "Duck < " + super().describe()


def multiple_inheritance():
    print("\n--- 7. multiple inheritance & __mro__ ---")
    d = Duck()
    print(d.move())                     # -> walk   (Walker comes before Swimmer)
    print(d.describe())                 # -> Duck < Walker
    print([c.__name__ for c in Duck.__mro__])
    # -> ['Duck', 'Walker', 'Swimmer', 'object']  (Method Resolution Order)
    print(Swimmer.move(d))              # -> swim   (call a specific parent explicitly)


if __name__ == "__main__":
    basics()
    class_vs_instance()
    inheritance()
    properties()
    class_and_static()
    private_names()
    multiple_inheritance()
