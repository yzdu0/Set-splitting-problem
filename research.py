"""Exact checks for the accompanying set-splitting research note.

This is a verification harness, not an implementation of a new #SAT algorithm.
Hyperedges are labelled: equal tuples in the edge list remain separate sets.
Run: python3 research.py
"""

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
from math import comb
import json
import random


@dataclass(frozen=True)
class Hypergraph:
    n: int
    edges: tuple[tuple[int, ...], ...]

    def delete(self, index):
        return Hypergraph(self.n, self.edges[:index] + self.edges[index + 1:])

    def contract(self, index):
        edge = self.edges[index]
        assert edge
        representative = edge[0]
        mapping = {v: representative if v in edge else v for v in range(self.n)}
        remaining = sorted(set(mapping.values()))
        renumber = {v: i for i, v in enumerate(remaining)}
        images = tuple(
            tuple(sorted({renumber[mapping[v]] for v in other}))
            for i, other in enumerate(self.edges) if i != index
        )
        return Hypergraph(len(remaining), images)


def split_count(graph, assignment):
    return sum(len({assignment[v] for v in e}) == 2 for e in graph.edges)


def brute_profile(graph):
    result = [0] * (len(graph.edges) + 1)
    for assignment in product((0, 1), repeat=graph.n):
        result[split_count(graph, assignment)] += 1
    return result


def combine(deleted, contracted):
    """z A(z) + (1-z) B(z), retaining exact signed arithmetic."""
    assert len(deleted) == len(contracted)
    result = [0] * (len(deleted) + 1)
    for i, value in enumerate(deleted):
        result[i + 1] += value
    for i, value in enumerate(contracted):
        result[i] += value
        result[i + 1] -= value
    return result


def deletion_contraction_profile(graph, rank_limit, leaf_solver=brute_profile):
    """Only contract edges of size > rank_limit; DFS, no memoization."""
    chosen = next((i for i, e in enumerate(graph.edges) if len(e) > rank_limit), None)
    if chosen is None:
        return leaf_solver(graph), 1
    deleted, left = deletion_contraction_profile(graph.delete(chosen), rank_limit, leaf_solver)
    contracted, right = deletion_contraction_profile(graph.contract(chosen), rank_limit, leaf_solver)
    return combine(deleted, contracted), left + right


class CircuitCNF:
    """Fan-in two gates with unique Tseitin extensions, all clauses width <=3."""

    def __init__(self, input_count):
        self.variables = input_count
        self.clauses = []
        self.true = self.fresh()
        self.clauses.append((self.true,))
        self.false = -self.true

    def fresh(self):
        self.variables += 1
        return self.variables

    def and_gate(self, a, b):
        z = self.fresh()
        self.clauses.extend([(-a, -b, z), (a, -z), (b, -z)])
        return z

    def or_gate(self, a, b):
        return -self.and_gate(-a, -b)

    def xor_gate(self, a, b):
        z = self.fresh()
        self.clauses.extend([(a, b, -z), (-a, -b, -z), (a, -b, z), (-a, b, z)])
        return z

    def reduce_or(self, literals):
        if not literals:
            return self.false
        current = list(literals)
        while len(current) > 1:
            current = [
                self.or_gate(current[i], current[i + 1]) if i + 1 < len(current) else current[i]
                for i in range(0, len(current), 2)
            ]
        return current[0]

    def add(self, a, b):
        carry = self.false
        output = []
        for i in range(max(len(a), len(b))):
            av = a[i] if i < len(a) else self.false
            bv = b[i] if i < len(b) else self.false
            ab = self.xor_gate(av, bv)
            output.append(self.xor_gate(ab, carry))
            carry = self.or_gate(self.and_gate(av, bv), self.and_gate(ab, carry))
        output.append(carry)
        return output


def encode_exact_splits(graph, target):
    circuit = CircuitCNF(graph.n)
    split_flags = []
    for edge in graph.edges:
        some_one = circuit.reduce_or([v + 1 for v in edge])
        some_zero = circuit.reduce_or([-(v + 1) for v in edge])
        split_flags.append(circuit.and_gate(some_one, some_zero))
    numbers = [[flag] for flag in split_flags]
    while len(numbers) > 1:
        numbers = [
            circuit.add(numbers[i], numbers[i + 1]) if i + 1 < len(numbers) else numbers[i]
            for i in range(0, len(numbers), 2)
        ]
    total = numbers[0] if numbers else [circuit.false]
    if target < 0 or target >= (1 << len(total)):
        circuit.clauses.append(())
    else:
        circuit.clauses.extend((bit if (target >> i) & 1 else -bit,) for i, bit in enumerate(total))
    return circuit


def count_cnf(circuit, assumptions=()):
    """Tiny exhaustive DPLL oracle. No claimed subexponential bound."""
    initial = tuple(circuit.clauses) + tuple((lit,) for lit in assumptions)

    def visit(clauses, assigned):
        while True:
            if any(not clause for clause in clauses):
                return 0
            unit = next((clause[0] for clause in clauses if len(clause) == 1), None)
            if unit is None:
                break
            variable = abs(unit)
            value = unit > 0
            if variable in assigned and assigned[variable] != value:
                return 0
            assigned[variable] = value
            clauses = tuple(
                tuple(lit for lit in clause if lit != -unit)
                for clause in clauses if unit not in clause
            )
        if not clauses:
            return 1 << (circuit.variables - len(assigned))
        variable = abs(clauses[0][0])
        return sum(visit(clauses + ((lit,),), dict(assigned)) for lit in (variable, -variable))

    return visit(initial, {})


def cnf_profile(graph):
    return [count_cnf(encode_exact_splits(graph, target)) for target in range(len(graph.edges) + 1)]


def verify():
    counts = {"identity_checks": 0, "recursive_profiles": 0, "cnf_profiles": 0,
              "unique_extension_checks": 0, "tensor_entries": 0, "leaf_bound_checks": 0}
    # Exhaust every simple hypergraph on up to four vertices, including small sets.
    for n in range(5):
        edges = [tuple(i for i in range(n) if mask & (1 << i)) for mask in range(1 << n)]
        for mask in range(1 << len(edges)):
            graph = Hypergraph(n, tuple(edge for i, edge in enumerate(edges) if mask & (1 << i)))
            if n == 4:
                # All 65,536 systems, check one deterministically chosen large edge.
                choices = [i for i, e in enumerate(graph.edges) if len(e) >= 2][:1]
            else:
                choices = [i for i, e in enumerate(graph.edges) if len(e) >= 2]
            original = brute_profile(graph) if choices else None
            for i in choices:
                assert combine(brute_profile(graph.delete(i)), brute_profile(graph.contract(i))) == original
                counts["identity_checks"] += 1
    rng = random.Random(20261029)
    for trial in range(250):
        n = rng.randrange(1, 9)
        # Includes duplicate labels, empty/singleton edges, isolated vertices.
        graph = Hypergraph(n, tuple(tuple(v for v in range(n) if rng.randrange(2)) for _ in range(rng.randrange(13))))
        truth = brute_profile(graph)
        for limit in (1, 2, 3):
            profile, leaves = deletion_contraction_profile(graph, limit)
            assert profile == truth
            bound = sum(comb(len(graph.edges), j) for j in range(min(len(graph.edges), (n - 1) // limit) + 1))
            assert leaves <= bound
            counts["recursive_profiles"] += 1
            counts["leaf_bound_checks"] += 1
        if trial < 70:
            assert cnf_profile(graph) == truth
            counts["cnf_profiles"] += 1
            for assignment in product((0, 1), repeat=n):
                target = split_count(graph, assignment)
                assumptions = [v + 1 if bit else -(v + 1) for v, bit in enumerate(assignment)]
                assert count_cnf(encode_exact_splits(graph, target), assumptions) == 1
                wrong = (target + 1) % (len(graph.edges) + 1) if graph.edges else 1
                assert count_cnf(encode_exact_splits(graph, wrong), assumptions) == 0
                counts["unique_extension_checks"] += 2
    for q in range(2, 15):
        t = Fraction(q, q * q - q + 1)
        c = Fraction(1, q ** 3 + 1)
        for bits in product((0, 1), repeat=3):
            value = c * (q ** bits.count(0) + q ** bits.count(1))
            assert value == (1 if len(set(bits)) == 1 else t)
            counts["tensor_entries"] += 1
    sizes = []
    for m in (8, 16, 32, 64, 128, 256):
        graph = Hypergraph(3, ((0, 1, 2),) * m)
        encoding = encode_exact_splits(graph, m // 2)
        assert all(len(clause) <= 3 for clause in encoding.clauses)
        assert encoding.variables <= graph.n + 20 * m
        assert len(encoding.clauses) <= 80 * m
        sizes.append({"sets": m, "variables": encoding.variables, "clauses": len(encoding.clauses)})
    return {"status": "passed", "seed": 20261029, "checks": counts, "rank3_encoding_sizes": sizes}


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
