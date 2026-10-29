#!/usr/bin/env python3
"""Deterministic finite-field checks for the cubic terminal-solver lemma.

No external dependencies. This verifies algebra and small network contractions;
it is not an implementation of the full parameterized algorithm.
"""
from itertools import product
from random import Random

P = 101
D = 2  # a nonsquare modulo 101


class F:
    __slots__ = ('a', 'b')

    def __init__(self, a=0, b=0):
        if isinstance(a, F):
            self.a, self.b = a.a, a.b
        else:
            self.a, self.b = a % P, b % P

    def __add__(self, other):
        other = F(other)
        return F(self.a + other.a, self.b + other.b)
    __radd__ = __add__

    def __neg__(self):
        return F(-self.a, -self.b)

    def __sub__(self, other):
        return self + -F(other)

    def __rsub__(self, other):
        return F(other) + -self

    def __mul__(self, other):
        other = F(other)
        return F(self.a * other.a + D * self.b * other.b,
                 self.a * other.b + self.b * other.a)
    __rmul__ = __mul__

    def inverse(self):
        norm = (self.a * self.a - D * self.b * self.b) % P
        if not norm:
            raise ZeroDivisionError
        inv = pow(norm, -1, P)
        return F(self.a * inv, -self.b * inv)

    def __truediv__(self, other):
        return self * F(other).inverse()

    def __eq__(self, other):
        other = F(other)
        return self.a == other.a and self.b == other.b

    def __bool__(self):
        return bool(self.a or self.b)

    def __repr__(self):
        return f'F({self.a},{self.b})'


def sqrt_base(value):
    """Every base-field element has a square root in the common quadratic field."""
    value = F(value)
    assert value.b == 0
    for x in range(P):
        if x * x % P == value.a:
            return F(x)
    for x in range(P):
        if D * x * x % P == value.a:
            return F(0, x)
    raise AssertionError('quadratic extension failed')


def determinant(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inverse(a):
    den = determinant(a)
    return [[a[1][1] / den, -a[0][1] / den],
            [-a[1][0] / den, a[0][0] / den]]


def multiply(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(2)), F())
             for j in range(2)] for i in range(2)]


def eigenvector(c, value):
    rows = [[c[0][0] - value, c[0][1]],
            [c[1][0], c[1][1] - value]]
    row = next(row for row in rows if any(row))
    vector = [row[1], -row[0]]
    assert all(sum((rows[i][j] * vector[j] for j in range(2)), F()) == 0
               for i in range(2))
    return vector


def decompose(tensor):
    """Return three [latent spin][port bit] matrices, or None if exceptional."""
    a = [[tensor[(i << 2) | (j << 1)] for j in range(2)] for i in range(2)]
    b = [[tensor[(i << 2) | (j << 1) | 1] for j in range(2)] for i in range(2)]
    if not determinant(a):
        return None
    c = multiply(b, inverse(a))
    trace = c[0][0] + c[1][1]
    disc = trace * trace - 4 * determinant(c)
    if not disc:
        return None
    root = sqrt_base(disc)
    values = [(trace + root) / 2, (trace - root) / 2]
    vectors = [eigenvector(c, value) for value in values]
    u = [[vectors[s][i] for s in range(2)] for i in range(2)]
    v = multiply(inverse(u), a)
    factors = [[[u[i][s] for i in range(2)] for s in range(2)],
               v,
               [[F(1), values[s]] for s in range(2)]]
    for i, j, k in product(range(2), repeat=3):
        recovered = sum((factors[0][s][i] * factors[1][s][j] *
                         factors[2][s][k] for s in range(2)), F())
        assert recovered == tensor[(i << 2) | (j << 1) | k]
    return factors


R = [F(v) for v in [1, 1, 0, 0, 0, 0, 1, 2]]


def perturb(tensor, epsilon):
    return [value + epsilon * r for value, r in zip(tensor, R)]


def contract_ports(tensors):
    """Brute force on the six Boolean edges of the K4 tensor network."""
    edges = [(a, b) for a in range(4) for b in range(a + 1, 4)]
    ports = [[i for i, edge in enumerate(edges) if v in edge] for v in range(4)]
    total = F()
    for bits in product(range(2), repeat=len(edges)):
        term = F(1)
        for v in range(4):
            index = sum(bits[edge] << (2 - j) for j, edge in enumerate(ports[v]))
            term *= tensors[v][index]
        total += term
    return total


def contract_latent(factors):
    """Brute force the binary pairwise model derived on that same K4."""
    edges = [(a, b) for a in range(4) for b in range(a + 1, 4)]
    ports = [[i for i, edge in enumerate(edges) if v in edge] for v in range(4)]
    total = F()
    for spins in product(range(2), repeat=4):
        term = F(1)
        for edge_id, (u, v) in enumerate(edges):
            pu, pv = ports[u].index(edge_id), ports[v].index(edge_id)
            term *= sum((factors[u][pu][spins[u]][bit] *
                         factors[v][pv][spins[v]][bit]
                         for bit in range(2)), F())
        total += term
    return total


def interpolate_zero(points):
    answer = F()
    for i, (x, y) in enumerate(points):
        weight = F(1)
        for j, (z, _) in enumerate(points):
            if i != j:
                weight *= -F(z) / (F(x) - F(z))
        answer += weight * y
    return answer


def verify():
    assert all(x * x % P != D for x in range(P))
    rng = Random(292026)
    exceptional = [
        [F(0) for _ in range(8)],
        [F(int(i in (0, 7))) for i in range(8)],
        [F(int(i in (1, 2, 4))) for i in range(8)],
    ]
    samples = exceptional + [[F(rng.randrange(-9, 10)) for _ in range(8)]
                             for _ in range(100)]
    decompositions = 0
    for tensor in samples:
        bad = 0
        for epsilon in range(10):
            result = decompose(perturb(tensor, epsilon))
            bad += result is None
            decompositions += result is not None
        assert bad <= 6

    networks = [[[F(rng.randrange(-5, 6)) for _ in range(8)] for _ in range(4)]
                for _ in range(12)]
    networks += [[[F(1 if i in (0, 7) else 2) for i in range(8)]
                  for _ in range(4)]]
    network_evaluations = 0
    for tensors in networks:
        points = []
        for epsilon in range(29):  # 7h+1, with h=4
            perturbed = [perturb(t, epsilon) for t in tensors]
            factors = [decompose(t) for t in perturbed]
            if any(f is None for f in factors):
                continue
            z_ports = contract_ports(perturbed)
            z_latent = contract_latent(factors)
            assert z_ports == z_latent
            points.append((epsilon, z_latent))
            network_evaluations += 1
            if len(points) == 5:
                break
        assert len(points) == 5
        assert interpolate_zero(points) == contract_ports(tensors)
    print(f'PASS: {decompositions} ternary decompositions; '
          f'{network_evaluations} exact K4 network evaluations; '
          f'{len(networks)} perturbation/interpolation recoveries over F_(101^2).')


if __name__ == '__main__':
    verify()
