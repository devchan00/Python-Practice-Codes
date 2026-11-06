"""Lesson 2.9 - Mini project: a quiz app with classes.

A small multiple-choice quiz that pulls together the intermediate lessons:
Question and Quiz classes (with __repr__, @property, @classmethod and
@staticmethod), questions loaded from questions.json, a custom exception
hierarchy with `raise ... from`, comprehensions and functional helpers for the
results, argparse for options and datetime for a fixed-format timestamp.

By default a seeded "auto player" answers every question so the program runs
without any input. Pass --play to answer the questions yourself:

    python example.py            # automatic demo run
    python example.py --play     # interactive
"""

import argparse
import json
import random
import sys
from datetime import datetime
from pathlib import Path

# The JSON file lives next to this script, so build the path from __file__
# instead of relying on the current working directory.
DEFAULT_FILE = Path(__file__).resolve().parent / "questions.json"
LETTERS = "ABCD"


# --- 1. Custom exceptions (lesson 07) ---
class QuizError(Exception):
    """Base class for every quiz problem."""


class QuestionFormatError(QuizError):
    """A question in the JSON file is malformed."""


# --- 2. The Question class (lesson 06) ---
class Question:
    def __init__(self, prompt, choices, answer, topic="general"):
        if not 0 <= answer < len(choices):
            raise QuestionFormatError(f"answer index {answer} out of range for {prompt!r}")
        self.prompt = prompt
        self.choices = list(choices)
        self.answer = answer            # index of the correct choice
        self.topic = topic

    @classmethod
    def from_dict(cls, data):
        """Alternative constructor: build a Question from a JSON object."""
        try:
            return cls(data["prompt"], data["choices"], data["answer"], data.get("topic", "general"))
        except KeyError as e:
            raise QuestionFormatError(f"question is missing field {e}") from e

    @property
    def correct_choice(self):
        return self.choices[self.answer]

    @staticmethod
    def letter_to_index(letter):
        """'b' -> 1. Raises ValueError for anything that isn't a valid letter."""
        letter = letter.strip().upper()
        if len(letter) != 1 or letter not in LETTERS:
            raise ValueError(f"not a valid choice: {letter!r}")
        return LETTERS.index(letter)

    def is_correct(self, index):
        return index == self.answer

    def render(self, number):
        lines = [f"Q{number}. {self.prompt}"]
        lines += [f"   {LETTERS[i]}) {c}" for i, c in enumerate(self.choices)]   # comprehension
        return "\n".join(lines)

    def __repr__(self):
        return f"Question({self.prompt!r}, topic={self.topic!r})"


# --- 3. The Quiz class ---
class Quiz:
    def __init__(self, title, questions):
        self.title = title
        self.questions = questions
        self.results = []               # list of (question, chosen_index, correct?)

    @classmethod
    def from_json(cls, path):
        """Load a quiz from a JSON file (lesson 05)."""
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError as e:
            raise QuizError(f"question file not found: {path}") from e
        except json.JSONDecodeError as e:
            raise QuizError(f"invalid JSON in {path}: {e.msg}") from e
        questions = [Question.from_dict(q) for q in data["questions"]]
        return cls(data.get("title", "Quiz"), questions)

    def record(self, question, chosen):
        self.results.append((question, chosen, question.is_correct(chosen)))

    @property
    def score(self):
        return sum(ok for _, _, ok in self.results)   # True counts as 1

    @property
    def percent(self):
        return 100 * self.score / len(self.results) if self.results else 0.0

    def missed_topics(self):
        # set comprehension -> unique topics, sorted for stable output
        return sorted({q.topic for q, _, ok in self.results if not ok})

    def __len__(self):
        return len(self.questions)

    def __repr__(self):
        return f"Quiz({self.title!r}, {len(self)} questions)"


# --- 4. Players: auto (default) and human (--play) ---
def auto_player(rng, accuracy=0.75):
    """Return a function that picks answers: mostly right, sometimes wrong."""
    def choose(question):
        if rng.random() < accuracy:
            return question.answer
        wrong = [i for i in range(len(question.choices)) if i != question.answer]
        return rng.choice(wrong)
    return choose                       # a closure over rng and accuracy (lesson 03)


def human_player(question):
    while True:
        reply = input("Your answer (A-D): ")
        try:
            index = Question.letter_to_index(reply)
            if index < len(question.choices):
                return index
        except ValueError:
            pass
        print("Please type one of:", ", ".join(LETTERS[: len(question.choices)]))


# --- 5. Running the quiz ---
def run(quiz, player, shuffle_rng=None, show_choice=True):
    questions = list(quiz.questions)
    if shuffle_rng:
        shuffle_rng.shuffle(questions)
    for n, q in enumerate(questions, start=1):
        print(q.render(n))
        chosen = player(q)
        quiz.record(q, chosen)
        if show_choice:
            print(f"   -> chose {LETTERS[chosen]}")
        print("   Correct!" if q.is_correct(chosen) else f"   Wrong - it was: {q.correct_choice}")
        print()


def report(quiz, finished_at):
    print("=" * 40)
    print(f"{quiz.title} - finished {finished_at:%Y-%m-%d %H:%M}")
    print(f"Score: {quiz.score}/{len(quiz.results)} ({quiz.percent:.0f}%)")
    missed = quiz.missed_topics()
    print("Review these topics:", ", ".join(missed) if missed else "none - well done!")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Multiple-choice quiz")
    parser.add_argument("--play", action="store_true", help="answer the questions yourself")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE, help="questions JSON file")
    parser.add_argument("--seed", type=int, default=1, help="seed for the auto player")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        quiz = Quiz.from_json(args.file)
    except QuizError as e:
        print("Error:", e, file=sys.stderr)
        return 1

    print(quiz)
    print()
    if args.play:
        run(quiz, human_player, shuffle_rng=random.Random(), show_choice=False)
        finished = datetime.now()
    else:
        rng = random.Random(args.seed)  # seeded -> identical demo output every run
        run(quiz, auto_player(rng))
        finished = datetime(2024, 3, 15, 12, 0)   # fixed so the demo is deterministic
    report(quiz, finished)
    return 0


if __name__ == "__main__":
    sys.exit(main())
