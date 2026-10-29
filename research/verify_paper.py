"""Reproduce the paper's selector reduction checks and save a JSON manifest.

Run from the repository root: python3 research/verify_paper.py
The backend is exhaustive DPLL; this does not implement the external theorem.
"""

import hashlib
import json
from itertools import product
from math import comb
from pathlib import Path
import random
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from research import CircuitCNF, Hypergraph, count_cnf
from selector_moments import encode_moment


def selector_cardinality(circuit, selectors, target):
    numbers = [[selector] for selector in selectors]
    while len(numbers) > 1:
        numbers = [circuit.add(numbers[i], numbers[i + 1]) if i + 1 < len(numbers) else numbers[i]
                   for i in range(0, len(numbers), 2)]
    total = numbers[0] if numbers else [circuit.false]
    circuit.clauses.extend((bit if (target >> i) & 1 else -bit,) for i, bit in enumerate(total))


def predicate_encoding(n, predicates, target):
    circuit = CircuitCNF(n)
    selectors = []
    for predicate in predicates:
        selector = circuit.fresh()
        selectors.append(selector)
        circuit.clauses.extend((-selector,) + clause for clause in predicate)
    selector_cardinality(circuit, selectors, target)
    return circuit


def predicate_profile(n, predicates):
    profile = [0] * (len(predicates) + 1)
    for bits in product((0, 1), repeat=n):
        def literal_value(literal):
            value = bits[abs(literal) - 1]
            return value if literal > 0 else 1 - value
        score = sum(all(any(literal_value(literal) for literal in clause) for clause in predicate)
                    for predicate in predicates)
        profile[score] += 1
    return profile


def check_predicates(n, predicates):
    truth = predicate_profile(n, predicates)
    m = len(predicates)
    expected = [sum(number * comb(j, t) for j, number in enumerate(truth) if j >= t)
                for t in range(m + 1)]
    actual = []
    for t in range(m + 1):
        circuit = predicate_encoding(n, predicates, t)
        assert all(len(clause) <= 3 for clause in circuit.clauses)
        assert circuit.variables <= n + 25 * m + 1
        actual.append(count_cnf(circuit))
    assert actual == expected
    recovered = [sum((-1) ** (t-j) * comb(t, j) * actual[t] for t in range(j, m+1))
                 for j in range(m+1)]
    assert recovered == truth
    return m + 1


def main():
    completed = subprocess.run([sys.executable, "research/selector_moments.py"], cwd=ROOT,
                               text=True, capture_output=True, check=True)
    assert "378 complete split-profile comparisons; 1773" in completed.stdout
    assert "20 optimal-coloring self-reductions" in completed.stdout
    rng = random.Random(20261029)
    predicate_calls = 0
    for _ in range(80):
        n, m = rng.randrange(1, 6), rng.randrange(7)
        predicates = []
        for _ in range(m):
            predicate = tuple(tuple((1 if rng.randrange(2) else -1) * rng.randrange(1, n+1)
                                    for _ in range(rng.randrange(3)))
                              for _ in range(rng.randrange(5)))
            predicates.append(predicate)
        predicate_calls += check_predicates(n, predicates)
    maxsat_calls = 0
    for _ in range(20):
        n, m = rng.randrange(1, 6), rng.randrange(7)
        clauses = [tuple((1 if rng.randrange(2) else -1) * rng.randrange(1, n+1)
                         for _ in range(rng.randrange(n+2))) for _ in range(m)]
        violated_predicates = [tuple((-literal,) for literal in clause) for clause in clauses]
        maxsat_calls += check_predicates(n, violated_predicates)
    sizes = []
    for m in (0, 1, 2, 4, 8, 16, 32, 64):
        n = max(1, m)
        for rank in sorted({0, 1, min(2, n), n}):
            graph = Hypergraph(n, (tuple(range(rank)),) * m)
            circuit = encode_moment(graph, m // 2)
            assert all(len(clause) <= 3 for clause in circuit.clauses)
            assert circuit.variables <= n + 25 * m + 1
            sizes.append({"vertices": n, "sets": m, "rank": rank,
                          "incidences": rank * m, "variables": circuit.variables,
                          "clauses": len(circuit.clauses)})
    source_files = ["research.py", "research/selector_moments.py", "research/verify_paper.py", "paper/main.tex"]
    result = {
        "status": "passed", "date": "2026-10-29", "seed": 20261029,
        "backend": "exhaustive DPLL and independent exhaustive coloring; not the external SAT algorithm",
        "commands": ["python3 research/verify_paper.py", "python3 research/selector_moments.py"],
        "checks": {
            "full_hypergraph_profiles": 378, "selector_moment_cnf_counts": 1773,
            "optimal_coloring_self_reductions": 20, "fully_pinned_profiles": 20,
            "general_2cnf_predicate_profiles": 80, "general_predicate_cnf_counts": predicate_calls,
            "maxsat_violation_profiles": 20, "maxsat_violation_cnf_counts": maxsat_calls,
            "encoding_size_checks": len(sizes),
        },
        "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in source_files},
        "selector_harness_output": completed.stdout.strip(),
        "encoding_sizes": sizes,
        "scope": "Finite checks validate encodings, moments, inversion, and construction. They do not prove asymptotic complexity or validate the external theorem.",
    }
    destination = ROOT / "paper" / "verification.json"
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["checks"], indent=2))
    print("PASS; wrote", destination)


if __name__ == "__main__":
    main()
