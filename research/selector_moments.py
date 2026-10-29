"""Verify the selector/binomial-moment reduction to dense #3SAT.

This uses the small exhaustive DPLL oracle in research.py, not the new SAT
algorithm. Run from the project root: python3 research/selector_moments.py.
"""

from itertools import product
from math import comb
from pathlib import Path
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from research import CircuitCNF, Hypergraph, brute_profile, count_cnf


def encode_moment(graph, target):
    circuit = CircuitCNF(graph.n)
    selectors = []
    for edge in graph.edges:
        selector = circuit.fresh()
        selectors.append(selector)
        if not edge:
            continue  # Empty/singleton edges are always monochromatic.
        anchor = edge[0] + 1
        for vertex in edge[1:]:
            variable = vertex + 1
            circuit.clauses.extend([
                (-selector, -anchor, variable),
                (-selector, anchor, -variable),
            ])
    numbers = [[flag] for flag in selectors]
    while len(numbers) > 1:
        numbers = [
            circuit.add(numbers[i], numbers[i + 1]) if i + 1 < len(numbers) else numbers[i]
            for i in range(0, len(numbers), 2)
        ]
    total = numbers[0] if numbers else [circuit.false]
    if target < 0 or target >= 1 << len(total):
        circuit.clauses.append(())
    else:
        circuit.clauses.extend((bit if (target >> i) & 1 else -bit,) for i, bit in enumerate(total))
    return circuit


def invert_moments(moments):
    m = len(moments) - 1
    monochromatic_profile = [
        sum((-1) ** (t - j) * comb(t, j) * moments[t] for t in range(j, m + 1))
        for j in range(m + 1)
    ]
    return list(reversed(monochromatic_profile))


def profile_with_pins(graph, pins=()):
    return invert_moments([count_cnf(encode_moment(graph, t), pins)
                           for t in range(len(graph.edges) + 1)])


def construct_optimal_coloring(graph):
    original = profile_with_pins(graph)
    optimum = max(s for s, number in enumerate(original) if number)
    pins = []
    coloring = []
    for variable in range(1, graph.n + 1):
        if profile_with_pins(graph, pins + [-variable])[optimum]:
            pins.append(-variable)
            coloring.append(0)
        else:
            pins.append(variable)
            coloring.append(1)
    return optimum, tuple(coloring)


def check_graph(graph):
    truth = brute_profile(graph)
    m = len(graph.edges)
    direct_moments = [sum(comb(m - s, t) * number for s, number in enumerate(truth)
                          if m - s >= t) for t in range(m + 1)]
    encoded_moments = [count_cnf(encode_moment(graph, t)) for t in range(m + 1)]
    assert direct_moments == encoded_moments, (graph, direct_moments, encoded_moments)
    assert invert_moments(encoded_moments) == truth
    for t in range(m + 1):
        circuit = encode_moment(graph, t)
        assert all(len(clause) <= 3 for clause in circuit.clauses)
        assert circuit.variables <= graph.n + 20 * max(1, m)
    return m + 1


def verify():
    graphs = calls = 0
    for n in range(4):
        possible = [tuple(v for v in range(n) if mask & (1 << v)) for mask in range(1 << n)]
        for mask in range(1 << len(possible)):
            graph = Hypergraph(n, tuple(edge for i, edge in enumerate(possible) if mask & (1 << i)))
            calls += check_graph(graph)
            graphs += 1
    rng = random.Random(20261029)
    constructions = 0
    for trial in range(100):
        n = rng.randrange(1, 7)
        graph = Hypergraph(n, tuple(tuple(v for v in range(n) if rng.randrange(2))
                                   for _ in range(rng.randrange(8))))
        calls += check_graph(graph)
        graphs += 1
        if trial < 20:
            optimum, coloring = construct_optimal_coloring(graph)
            actual = sum(len({coloring[v] for v in edge}) == 2 for edge in graph.edges)
            assert actual == optimum
            assert max(s for s, number in enumerate(brute_profile(graph)) if number) == optimum
            constructions += 1
            pins = tuple(v + 1 if bit else -(v + 1) for v, bit in enumerate(coloring))
            fixed = profile_with_pins(graph, pins)
            assert sum(fixed) == 1 and fixed[optimum] == 1
    print(f"PASS: {graphs} complete split-profile comparisons; {calls} exact selector-moment #3SAT counts.")
    print(f"PASS: {constructions} optimal-coloring self-reductions and fully pinned profile checks.")


if __name__ == "__main__":
    verify()
