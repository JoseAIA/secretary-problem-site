#!/usr/bin/env python3
"""Classical secretary problem: exact probabilities and reproducible simulation.

Standard library only. Absolute rank 1 is best. When no record appears
after the initial rejection phase, no candidate is selected.
"""
import argparse
import random
from fractions import Fraction


def probability(n: int, r: int) -> Fraction:
    """Exact success probability of a threshold rule (smallest ranks are best)."""
    if not (isinstance(n, int) and n >= 2 and isinstance(r, int) and 0 <= r < n):
        raise ValueError("Require integer n >= 2 and 0 <= r < n")
    if r == 0:
        return Fraction(1, n)
    return Fraction(r, n) * sum((Fraction(1, j) for j in range(r, n)), Fraction(0))


def optimal_threshold(n: int) -> tuple[int, Fraction]:
    """Smallest maximizing threshold; ties are resolved toward the smaller r."""
    values = [probability(n, r) for r in range(n)]
    maximum = max(values)
    return values.index(maximum), maximum


def selected_rank(permutation: list[int], r: int) -> int | None:
    """Return accepted absolute rank or None (no new record after rejection)."""
    if not 0 <= r < len(permutation):
        raise ValueError("Threshold out of range")
    if r == 0:
        return permutation[0]
    record = min(permutation[:r])
    for rank in permutation[r:]:
        if rank < record:
            return rank
    return None


def simulate(n: int, r: int, trials: int, seed: int = 123) -> float:
    """Estimate the win probability using a seeded Fisher–Yates shuffle."""
    if trials < 1:
        raise ValueError("trials must be positive")
    probability(n, r)  # validates parameters
    rng = random.Random(seed)
    ranks = list(range(1, n + 1))
    wins = 0
    for _ in range(trials):
        rng.shuffle(ranks)
        wins += selected_rank(ranks, r) == 1
    return wins / trials


def self_test() -> None:
    assert probability(10, 3) == Fraction(3349, 8400)
    assert optimal_threshold(10) == (3, Fraction(3349, 8400))
    assert probability(2, 0) == probability(2, 1) == Fraction(1, 2)
    assert selected_rank([2, 3, 1], 1) == 1
    assert selected_rank([1, 2, 3], 1) is None
    assert selected_rank([2, 1], 0) == 2
    print("All classical secretary tests passed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=30)
    parser.add_argument("--r", type=int, default=11)
    parser.add_argument("--trials", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=123)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        exact = probability(args.n, args.r)
        best_r, best_p = optimal_threshold(args.n)
        observed = simulate(args.n, args.r, args.trials, args.seed)
        print(f"n={args.n}, r={args.r}, trials={args.trials}, seed={args.seed}")
        print(f"Exact success probability: {exact} = {float(exact):.6f}")
        print(f"Smallest optimal threshold: {best_r} (P={float(best_p):.6f})")
        print(f"Monte Carlo success frequency: {observed:.6f}")
