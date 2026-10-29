"""Exact rational certificate for the proposed leaf-stripping variant.

This certifies the branching inequalities, not the separate tensor-terminal
algorithm. No numerical optimizer or third-party package is required.
"""

from fractions import Fraction as F
from math import exp


def q(s):
    return F(s)


def weight(values, degree):
    return values[min(degree, len(values) - 1)]


A = tuple(map(q, ("0", "0", ".14213804", ".21320706", ".24168709")))
X = tuple(map(q, ("0", "0", ".13207999", ".21642156", ".25874826", ".27075585", ".27586196")))
Y = tuple(map(q, ("0", "0", ".09903381", ".14587977", ".18044649", ".20049150", ".20447113")))


def delta(values, degree):
    return weight(values, degree) - weight(values, degree - 1)


def exp_minus_upper(value, terms=80):
    """Even Taylor partial sum is an upper bound on exp(-value)."""
    assert value >= 0 and terms % 2 == 0
    total = term = F(1)
    for j in range(1, terms + 1):
        term *= -value / j
        total += term
    return total


def exp_upper(value, terms=60):
    """Positive Taylor series with a geometric upper bound on its tail."""
    assert value >= 0 and value < terms + 2
    total = term = F(1)
    for j in range(1, terms + 1):
        term *= value / j
        total += term
    next_term = term * value / (terms + 1)
    return total + next_term / (1 - value / (terms + 2))


def check():
    for values in (A, X, Y):
        for degree in range(2, 9):
            assert delta(values, degree) >= 0
            assert delta(values, degree) >= delta(values, degree + 1)
    for degree in range(2, 9):
        assert weight(Y, degree) <= weight(X, degree)
    assert 2 * delta(A, 3) <= A[2]
    assert 2 * min(delta(Y, 4), delta(X, 3)) <= Y[2]

    rows = []
    for degree in range(4, 8):
        for neighbor_degree in range(2, degree + 1):
            # Element, all neighboring sets uncolored.
            drop = weight(A, degree) + degree * (weight(X, neighbor_degree) - weight(Y, neighbor_degree - 1))
            rows.append(("element/uncolored", degree, neighbor_degree, drop, drop))
            # Element, all neighboring sets have one fixed color.
            first = weight(A, degree) + degree * (weight(Y, neighbor_degree) + delta(A, degree) * (neighbor_degree - 1))
            second = weight(A, degree) + degree * delta(Y, neighbor_degree)
            rows.append(("element/colored", degree, neighbor_degree, first, second))
        for neighbor_degree in range(2, degree):
            # Colored set: optional and forbidden branches.
            first = weight(Y, degree) + degree * delta(A, neighbor_degree)
            second = weight(Y, degree) + degree * weight(A, neighbor_degree)
            second += min(delta(Y, degree), delta(X, degree - 1)) * degree * (neighbor_degree - 1)
            rows.append(("colored set", degree, neighbor_degree, first, second))
            # Uncolored set: merging has resulting degree >= 4, hence weight A[4].
            first = weight(X, degree) + degree * delta(A, neighbor_degree)
            second = weight(X, degree) + degree * weight(A, neighbor_degree) - A[4]
            rows.append(("uncolored set", degree, neighbor_degree, first, second))

    certified_slacks = []
    for kind, degree, neighbor_degree, first, second in rows:
        upper = exp_minus_upper(first) + exp_minus_upper(second)
        assert upper < 1, (kind, degree, neighbor_degree)
        certified_slacks.append((1 - upper, kind, degree, neighbor_degree))

    probabilities = {i: 1 - F(1, 2 ** (i - 1)) for i in range(2, 8)}
    ratios = {i: weight(X, i) / probabilities[i] for i in probabilities}
    budget = max(ratios.values())
    assert budget == ratios[4]
    # The weights of degree >=6 sets are constant and their split probabilities
    # increase, so degrees >=7 introduce no larger ratio.
    exponent = A[4] + budget
    assert exp_upper(exponent) < q("1.7116")

    # Terminal: degree-3 core vertices have weight >=Y[3], every core
    # vertex has weight >=Y[2]. With epsilon=.01 and ln(2)<.7:
    # ln(2)*(n3/6+.01*n) <= (.7/(6Y3)+.007/Y2)*mu < .9*mu.
    assert min(A[3], X[3], Y[3]) == Y[3]
    assert min(A[2], X[2], Y[2]) == Y[2]
    terminal_ratio = q(".7") / (6 * Y[3]) + q(".007") / Y[2]
    assert terminal_ratio < q(".9")

    worst = min(certified_slacks)
    print("Exact rational inequalities checked:", len(rows))
    print("Smallest certified branching slack:", float(worst[0]), worst[1:])
    print("Initial exponent budget:", exponent, "=", float(exponent))
    print("Corresponding numerical base:", exp(float(exponent)))
    print("Certified base < 1.7116")
    print("Terminal exponent / measure upper bound:", float(terminal_ratio))


if __name__ == "__main__":
    check()
