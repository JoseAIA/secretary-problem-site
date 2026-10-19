#!/usr/bin/env python3
"""Postdoc problem: maximize selecting absolute rank 2, with only relative ranks.

Finite-horizon exact backward induction. Returns rational probabilities.
At a given observation k, the relative rank a is uniform on {1,...,k}.
"""
import argparse
from fractions import Fraction
from itertools import permutations


def stop_reward(n: int, k: int, a: int) -> Fraction:
    """P(absolute rank 2 | observed relative rank a at position k)."""
    if n < 2 or not (1 <= k <= n) or not (1 <= a <= k):
        raise ValueError("Require n>=2, 1<=k<=n, 1<=a<=k")
    if a == 1:
        return Fraction(k * (n-k), n * (n-1))
    if a == 2:
        return Fraction(k * (k-1), n * (n-1))
    return Fraction(0)


def backward_values(n: int) -> list[Fraction]:
    """V[k] before seeing observation k, with V[n+1]=0."""
    if n < 2:
        raise ValueError("n must be at least 2")
    v = [Fraction(0)] * (n+2)
    for k in range(n, 0, -1):
        v[k] = sum(
            (max(stop_reward(n, k, a), v[k+1]) for a in range(1,k+1)),
            Fraction(0)
        ) / k
    return v


def policy_choice(n: int, k: int, a: int, v: list[Fraction]) -> bool:
    """Stop on a positive-value tie; otherwise continue."""
    reward = stop_reward(n,k,a)
    return reward > 0 and reward >= v[k+1]


def brute_force_probability(n: int) -> Fraction:
    """Exhaustive validation using all n! arrival permutations, for n<=7."""
    if n > 7:
        raise ValueError("Brute-force verification is limited to n<=7")
    v = backward_values(n)
    wins = 0
    total = 0
    for perm in permutations(range(1,n+1)):
        total += 1
        seen = []
        for k, absolute in enumerate(perm,1):
            relative = 1 + sum(x < absolute for x in seen)
            seen.append(absolute)
            if policy_choice(n,k,relative,v):
                wins += (absolute == 2)
                break
    return Fraction(wins,total)


def self_test() -> None:
    assert stop_reward(3,1,1) == Fraction(1,3)
    assert stop_reward(3,3,2) == Fraction(1)
    assert stop_reward(3,3,1) == Fraction(0)
    for n in range(2,7):
        values = backward_values(n)
        assert brute_force_probability(n) == values[1], (n, values[1])
    print("Postdoc exact DP and exhaustive enumeration tests passed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--rank", type=int, default=2)
    parser.add_argument("--self-test", action="store_true")
    args=parser.parse_args()
    if args.self_test:
        self_test()
    else:
        values=backward_values(args.n)
        now=stop_reward(args.n,args.k,args.rank)
        future=values[args.k+1]
        print(f"Optimal win probability: {values[1]} = {float(values[1]):.6f}")
        print(f"Position {args.k}, observed relative rank {args.rank}")
        print(f"Select now: {now} = {float(now):.6f}")
        print(f"Continue optimally: {future} = {float(future):.6f}")
        print("Select now" if policy_choice(args.n,args.k,args.rank,values) else "Continue")
