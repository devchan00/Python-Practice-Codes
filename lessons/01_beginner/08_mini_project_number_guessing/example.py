"""Mini-project: Number-guessing game.

The computer picks a secret number between LOW and HIGH, and a player
guesses until they find it, getting "too low" / "too high" hints. By
default this script plays itself: a computer player uses binary search
(always guess the middle of the remaining range), and a fixed random seed
makes every run identical. Run `python example.py --play` to play it
yourself with input(). The project combines everything from the beginner
lessons: variables, operators, strings, control flow, collections,
functions, input/output and error handling.
"""

import random
import sys

LOW = 1             # UPPER_CASE names: constants (lesson 1)
HIGH = 100
SEED = 42           # fixed seed -> the "random" secret is the same every run


def check_guess(guess, secret):
    """Return 'low', 'high' or 'correct' for a guess."""
    if guess < secret:          # if / elif / else (lesson 4)
        return "low"
    elif guess > secret:
        return "high"
    else:
        return "correct"


def computer_player(low=LOW, high=HIGH):
    """Create a binary-search guesser.

    Returns two functions: one that proposes the next guess and one that
    receives the 'low'/'high' feedback. A dict remembers the range that is
    still possible, so only beginner tools are needed (no classes yet).
    """
    state = {"low": low, "high": high}      # dict (lesson 5)

    def next_guess():
        # The middle of the range halves the possibilities each time,
        # so 1..100 never needs more than 7 guesses (2**7 = 128 >= 100).
        return (state["low"] + state["high"]) // 2      # floor division (lesson 2)

    def give_feedback(guess, result):
        if result == "low":
            state["low"] = guess + 1        # secret is above the guess
        elif result == "high":
            state["high"] = guess - 1       # secret is below the guess

    return next_guess, give_feedback        # return two values (lesson 6)


def play_automatically(seed=SEED):
    """Let the binary-search computer player find the secret number."""
    rng = random.Random(seed)               # own generator, fixed seed
    secret = rng.randint(LOW, HIGH)
    next_guess, give_feedback = computer_player()
    history = []                            # list of guesses (lesson 5)

    print(f"I'm thinking of a number between {LOW} and {HIGH}.")
    print("Computer player, using binary search:\n")

    while True:                             # loop until break (lesson 4)
        guess = next_guess()
        history.append(guess)
        result = check_guess(guess, secret)
        hint = {"low": "too low", "high": "too high", "correct": "correct!"}[result]
        print(f"  Guess #{len(history)}: {guess:>3} -> {hint}")   # f-string spec (lesson 3)
        if result == "correct":
            break
        give_feedback(guess, result)

    print(f"\nFound {secret} in {len(history)} guesses.")
    print("Guesses:", ", ".join(str(g) for g in history))   # join (lesson 3)
    return len(history)


def read_int(prompt):
    """Ask until the user types a whole number in range (lesson 7)."""
    while True:
        text = input(prompt).strip()
        try:
            number = int(text)
        except ValueError:
            print(f"  {text!r} is not a whole number, try again.")
            continue
        if LOW <= number <= HIGH:            # chained comparison (lesson 2)
            return number
        print(f"  Please stay between {LOW} and {HIGH}.")


def play_interactively():
    """A human plays: only used with the --play flag."""
    secret = random.randint(LOW, HIGH)      # truly random for humans
    tries = 0
    print(f"I'm thinking of a number between {LOW} and {HIGH}. Ctrl+C quits.")
    try:
        while True:
            guess = read_int("Your guess: ")
            tries += 1
            result = check_guess(guess, secret)
            if result == "correct":
                print(f"Correct! You needed {tries} tries.")
                break
            print("Too low!" if result == "low" else "Too high!")   # ternary (lesson 4)
    except (KeyboardInterrupt, EOFError):
        print(f"\nBye! The number was {secret}.")


def self_test():
    """Quick sanity check: binary search finds EVERY number in <= 7 guesses."""
    worst = 0
    for secret in range(LOW, HIGH + 1):     # range (lesson 7)
        next_guess, give_feedback = computer_player()
        guesses = 0
        while True:
            guesses += 1
            guess = next_guess()
            result = check_guess(guess, secret)
            if result == "correct":
                break
            give_feedback(guess, result)
        worst = max(worst, guesses)
    print(f"\nSelf-test: worst case over all {HIGH} secrets = {worst} guesses")
    return worst


if __name__ == "__main__":
    # sys.argv is the list of command-line words: ['example.py', '--play']
    if "--play" in sys.argv[1:]:            # membership test (lesson 2)
        play_interactively()
    else:
        play_automatically()                # -> Found 82 in 6 guesses. (with seed 42)
        assert self_test() <= 7             # -> Self-test: worst case ... = 7 guesses
