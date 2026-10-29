# Selector reduction

This is the method used in the [paper](../paper/main.tex).
Let u(x) be the number of monochromatic edges under coloring x.
Count

```text
F[t] = sum_x binom(u(x), t).
```

Give each edge a selector y. For an anchor a and each other vertex v, add

```text
(not y or not x[a] or x[v])
(not y or x[a] or not x[v])
```

Require exactly t selectors using a linear-size binary-adder circuit.
Selecting an edge forces one color; leaving it unselected imposes no condition.
Each allowed selector assignment has one extension to the circuit variables.

The formula has O(n+m) variables and O(J+m+1) clauses, where J counts
incidences. It introduces no variable per incidence.
Recover the number a[j] of colorings with j monochromatic edges by

```text
a[j] = sum_{t=j}^m (-1)^(t-j) binom(t,j) F[t].
```

The revised SAT theorem gives exponent O(s loglog(s)/sqrt(log(s))), s=n+m.
Its formalization scope note gives the squared-loglog version.
The decision kernel replaces s by O(k). Both use polynomial space.
The faster fixed-density rate applies only when J=O(s).

Fixed-color unit clauses support optimal-coloring recovery.
The same construction works for families of 2-CNF predicates and for
violated-clause counts in arbitrary CNF.

Run `python3 research/verify_paper.py`. The results and source hashes are in
[verification.json](../paper/verification.json). These finite checks do not
validate the external SAT theorem. The polynomial transform has established
coboundary and random-cluster antecedents; publication priority is unresolved.
