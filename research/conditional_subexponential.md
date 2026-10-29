# Earlier SAT reduction

This valid but weaker argument is superseded by the
[selector reduction](sat_rate_audit.md). It is retained as a working note.

For the split-count polynomial, deleting a nonempty edge e and contracting
all its vertices gives

```text
P[H](z) = z P[H-e](z) + (1-z) P[H/e](z).
```

Keep every edge label, including labels that become equal after contraction.
Keep isolated vertices or restore their factor of two.

After the decision kernel, n<=k and m<=2k. Branch on edges of size at least r.
Each contraction removes at least r-1 vertices, so there are at most

```text
sum_{j<=floor((n-1)/(r-1))} binom(m,j)
```

leaves, with j also bounded by m. This is 2^O(k log(r)/r).
At each leaf, a bounded-fan-in circuit tests the number of split edges using
O(rk) gates. Full gate equivalences give a 3-CNF with one extension per valid
coloring. Exact counts recover the leaf polynomial.

The conservative external SAT rate yields total exponent

```text
O(k log(r)/r + rk (loglog(rk))^2/sqrt(log(rk))).
```

Choosing r approximately (log(k))^(1/4)/sqrt(loglog(k)) gives
O(k(loglog(k))^(3/2)/(log(k))^(1/4)).
Using the manuscript's fixed-density rate instead gives
O(k sqrt(loglog(k))/(log(k))^(1/4)).
Both algorithms use polynomial space by traversing the tree depth first.

The selector method removes this branching and uses only O(k) SAT variables,
so it gives the stronger bound in the current paper.
