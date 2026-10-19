#!/usr/bin/env python3
"""Full-information secretary problem: exact first-stage rule for n=2 or 3.

Observations are iid Uniform(0,1). At the first observation x, compare
accepting (all future observations are smaller) versus rejecting and
then using the optimal policy for the remaining horizon.
"""
import argparse
from fractions import Fraction
from math import sqrt


def stop_value(n: int, x: Fraction) -> Fraction:
    if n not in (2,3) or not 0 <= x <= 1:
        raise ValueError("Require n in {2,3} and x in [0,1]")
    return x ** (n-1)


def continuation(n: int, x: Fraction) -> Fraction:
    if n not in (2,3) or not 0 <= x <= 1:
        raise ValueError("Require n in {2,3} and x in [0,1]")
    if n==2:
        return 1-x
    if x <= Fraction(1,2):
        return Fraction(3,4)-x*x/2
    return Fraction(1,2)+x-Fraction(3,2)*x*x


def threshold(n: int) -> float:
    if n==2:
        return .5
    if n==3:
        return (1+sqrt(6))/5
    raise ValueError("Require n in {2,3}")


def self_test() -> None:
    assert stop_value(2,Fraction(1,2)) == continuation(2,Fraction(1,2))
    assert continuation(3,Fraction(0)) == Fraction(3,4)
    assert continuation(3,Fraction(1,2)) == Fraction(5,8)
    assert continuation(3,Fraction(1)) == 0
    assert stop_value(3,Fraction(1,2)) < continuation(3,Fraction(1,2))
    assert stop_value(3,Fraction(3,4)) > continuation(3,Fraction(3,4))
    assert abs(threshold(3) - (1+sqrt(6))/5) < 1e-14
    print("Full-information analytic checks passed.")


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, choices=(2,3), default=3)
    parser.add_argument("--x", type=str, default="0.70")
    parser.add_argument("--self-test", action="store_true")
    args=parser.parse_args()
    if args.self_test:
        self_test()
    else:
        x=Fraction(args.x)
        stop=stop_value(args.n,x)
        go=continuation(args.n,x)
        print(f"n={args.n}, x={x} ({float(x):.4f})")
        print(f"Accept now: {stop} = {float(stop):.6f}")
        print(f"Continue optimally: {go} = {float(go):.6f}")
        print(f"Critical first-stage value: {threshold(args.n):.7f}")
        print("Accept now" if stop >= go else "Reject and continue")
