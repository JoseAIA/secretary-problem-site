#!/usr/bin/env python3
"""Bruss's sum-the-odds theorem: exact last-success stopping probabilities.

The independent Bernoulli probabilities satisfy 0 <= p_k < 1.
All calculations use Fraction, including decimal command-line inputs.
"""
import argparse
from fractions import Fraction


def probabilities(values: list[str]) -> list[Fraction]:
    p = [Fraction(value) for value in values]
    if not p or any(value < 0 or value >= 1 for value in p):
        raise ValueError("Supply at least one probability in [0, 1)")
    return p


def odds_threshold(p: list[Fraction]) -> int:
    """One-based optimal start index; choose 1 if the total odds are below 1."""
    if not p or any(value < 0 or value >= 1 for value in p):
        raise ValueError("Probabilities must be in [0,1)")
    tail = Fraction(0)
    for k in range(len(p) - 1, -1, -1):
        tail += p[k] / (1 - p[k])
        if tail >= 1:
            return k + 1
    return 1


def success_probability(p: list[Fraction], start: int) -> Fraction:
    """Probability of exactly one success in positions start,...,n."""
    if not 1 <= start <= len(p):
        raise ValueError("Start index out of range")
    tail = p[start-1:]
    return sum(
        (tail[k] *
         _product(1 - tail[j] for j in range(k)) *
         _product(1 - tail[j] for j in range(k + 1, len(tail)))
         for k in range(len(tail))),
        Fraction(0),
    )


def _product(items):
    value = Fraction(1)
    for item in items:
        value *= item
    return value


def self_test() -> None:
    p = probabilities(["0.2", "0.5", "0.3", "0.4"])
    s = odds_threshold(p)
    scores = [success_probability(p, j) for j in range(1, len(p)+1)]
    assert scores[s-1] == max(scores)
    assert odds_threshold(probabilities(["0", "0.2"])) == 1
    assert odds_threshold(probabilities(["0.5"])) == 1
    assert success_probability(probabilities(["0.5"]), 1) == Fraction(1, 2)
    print("All odds-theorem tests passed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probabilities", nargs="+", default=["0.2", "0.5", "0.3", "0.4"])
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        p = probabilities(args.probabilities)
        s = odds_threshold(p)
        scores = [success_probability(p, j) for j in range(1, len(p) + 1)]
        print(f"Optimal start index: {s} (one-based)")
        print(f"Optimal success probability: {scores[s-1]} = {float(scores[s-1]):.6f}")
        for j, score in enumerate(scores, 1):
            print(f"Start at {j}: {score} = {float(score):.6f}")
