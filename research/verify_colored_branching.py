"""Small-instance executable check of the proposed branching semantics.

The terminal is brute force here; this does not implement or verify the
proposed tensor terminal's running time. It checks the entire colored
branching recursion against exhaustive coloring, plus actual measure drops.
"""

from collections import deque
from itertools import combinations, product
import random

from branch_certificate import A, X, Y, delta, weight


def core(edges):
    graph = {("s", j): {("v", v) for v in vertices} for j, (vertices, _) in enumerate(edges)}
    for j, (vertices, _) in enumerate(edges):
        for v in vertices:
            graph.setdefault(("v", v), set()).add(("s", j))
    queue = deque(v for v in graph if len(graph[v]) <= 1)
    while queue:
        v = queue.popleft()
        if v not in graph:
            continue
        for u in graph.pop(v):
            graph[u].remove(v)
            if len(graph[u]) <= 1:
                queue.append(u)
    return graph


def measure(edges):
    graph = core(edges)
    total = sum(
        weight(A if v[0] == "v" else X if edges[v[1]][1] is None else Y, len(neighbors))
        for v, neighbors in graph.items()
    )
    return total, graph


def force(variables, edges, values, omitted=None):
    new_edges, split = [], 0
    for j, (vertices, flag) in enumerate(edges):
        if j == omitted:
            continue
        colors = {values[v] for v in vertices if v in values}
        if flag is not None:
            colors.add(flag)
        if len(colors) == 2:
            split += 1
        else:
            new_edges.append((vertices - values.keys(), next(iter(colors)) if colors else None))
    return variables - values.keys(), new_edges, split


def shift(profile, amount):
    return [0] * amount + profile


def linear_combination(*terms):
    length = max(len(profile) for _, profile in terms)
    result = [sum(sign * profile[i] for sign, profile in terms if i < len(profile)) for i in range(length)]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def brute(variables, edges):
    variables = sorted(variables)
    profile = [0] * (len(edges) + 1)
    for bits in product((0, 1), repeat=len(variables)):
        colors = dict(zip(variables, bits))
        count = 0
        for vertices, flag in edges:
            values = {colors[v] for v in vertices}
            if flag is not None:
                values.add(flag)
            count += len(values) == 2
        profile[count] += 1
    while len(profile) > 1 and profile[-1] == 0:
        profile.pop()
    return profile


stats = {"variable": 0, "uncolored_set": 0, "colored_set": 0, "terminal": 0}


def solve(variables, edges):
    mu, graph = measure(edges)
    if not graph or max(map(len, graph.values())) <= 3:
        stats["terminal"] += 1
        return brute(variables, edges)
    degree = max(map(len, graph.values()))
    choices = [v for v in graph if len(graph[v]) == degree]
    chosen = min(choices, key=lambda v: (0 if v[0] == "v" else 1 if edges[v[1]][1] is None else 2, v[1]))
    if chosen[0] == "v":
        stats["variable"] += 1
        results = []
        for color in (0, 1):
            new_variables, new_edges, split = force(variables, edges, {chosen[1]: color})
            lower = weight(A, degree)
            for neighbor in graph[chosen]:
                i = len(graph[neighbor])
                flag = edges[neighbor[1]][1]
                lower += (
                    weight(X, i) - weight(Y, i - 1) if flag is None else
                    delta(Y, i) if flag == color else
                    weight(Y, i) + delta(A, degree) * (i - 1)
                )
            assert mu - measure(new_edges)[0] >= lower
            results.append(shift(solve(new_variables, new_edges), split))
        return linear_combination(*((1, result) for result in results))

    j = chosen[1]
    vertices, flag = edges[j]
    optional_edges = edges[:j] + edges[j + 1:]
    optional_lower = weight(X if flag is None else Y, degree) + sum(delta(A, len(graph[u])) for u in graph[chosen])
    assert mu - measure(optional_edges)[0] >= optional_lower
    optional = solve(variables, optional_edges)
    if flag is None:
        stats["uncolored_set"] += 1
        representative = min(vertices)
        new_variables = (variables - vertices) | {representative}
        new_edges = [
            (frozenset(representative if v in vertices else v for v in vertices2), flag2)
            for jj, (vertices2, flag2) in enumerate(edges) if jj != j
        ]
        forbidden_lower = weight(X, degree) + sum(weight(A, len(graph[u])) for u in graph[chosen])
        forbidden_lower -= weight(A, sum(len(graph[u]) - 1 for u in graph[chosen]))
        split = 0
    else:
        stats["colored_set"] += 1
        new_variables, new_edges, split = force(variables, edges, {v: flag for v in vertices}, omitted=j)
        forbidden_lower = weight(Y, degree) + sum(weight(A, len(graph[u])) for u in graph[chosen])
        forbidden_lower += min(delta(Y, degree), delta(X, degree - 1)) * sum(len(graph[u]) - 1 for u in graph[chosen])
    assert mu - measure(new_edges)[0] >= forbidden_lower
    forbidden = shift(solve(new_variables, new_edges), split)
    result = linear_combination((1, shift(optional, 1)), (1, forbidden), (-1, shift(forbidden, 1)))
    assert all(count >= 0 for count in result)
    return result


def main():
    cases = 0
    # Every simple uncolored hypergraph on four vertices, omitting size <=1.
    possible = [frozenset(s) for size in range(2, 5) for s in combinations(range(4), size)]
    for mask in range(1 << len(possible)):
        edges = [(vertices, None) for j, vertices in enumerate(possible) if mask >> j & 1]
        assert solve(set(range(4)), edges) == brute(set(range(4)), edges)
        cases += 1
    rng = random.Random(958132)
    # Partial colors exercise both set branching rules, including repeated sets.
    for _ in range(700):
        n = rng.randrange(4, 10)
        edges = [
            (frozenset(rng.sample(range(n), rng.randrange(1, n + 1))), rng.choice((None, None, None, 0, 1)))
            for _ in range(rng.randrange(3, 19))
        ]
        assert solve(set(range(n)), edges) == brute(set(range(n)), edges)
        cases += 1
    # Force colored/uncolored set maxima: large constraints on few low-degree variables.
    for flag in (None, 0, 1):
        for n in range(4, 10):
            edges = [(frozenset(range(n)), flag), (frozenset(range(n)), 1)]
            assert solve(set(range(n)), edges) == brute(set(range(n)), edges)
            cases += 1
    print("Exact profile comparisons passed:", cases)
    print("Branch/terminal counts:", stats)


if __name__ == "__main__":
    main()
