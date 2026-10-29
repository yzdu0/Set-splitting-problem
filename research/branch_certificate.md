# Earlier branching certificate

This is the separate, unreviewed O*(1.7116^k) proposal.
It is not used by the SAT-based paper.

Use the kernel and expectation preprocessing of
[Nederlof, van Rooij, and van Dijk](https://doi.org/10.1007/s00453-013-9759-2).
The remaining instance has at most k elements and satisfies
sum_i (1-2^(1-i)) s_i < k.
Modify their Algorithm 2 by peeling only degree-zero/one vertices.
Do not annotate degree-two twins. Recompute the ordinary 2-core after each
branch. Prefer an element in a maximum-degree tie, then an uncolored set,
then a colored set. Stop at core degree three and use the
[tensor solver](tensor_candidate.md).

## Weights

Use a for elements, x for uncolored sets, and y for sets with one assigned
color. Degree-zero/one weights are zero.

| Degree | a | x | y |
|---|---:|---:|---:|
| 2 | .14213804 | .13207999 | .09903381 |
| 3 | .21320706 | .21642156 | .14587977 |
| 4 | .24168709 | .25874826 | .18044649 |
| 5 | .24168709 | .27075585 | .20049150 |
| >=6 | .24168709 | .27586196 | .20447113 |

Let mu be their sum over the core and Dz(i)=z(i)-z(i-1).
The weights are exact rational numbers. They are nondecreasing and concave
from degree two, with y<=x, 2Da(3)<=a(2), and
2min(Dy(4),Dx(3))<=y(2). These conditions bound repeated edge losses.

## Branch bounds

For branching degree d>=4 and a uniform neighborhood of degree i, the two
measure drops are bounded below as follows.

| Branch | First drop | Second drop |
|---|---|---|
| Element; uncolored neighbors | a(d)+d(x(i)-y(i-1)) | Same |
| Element; one-color neighbors | a(d)+d(y(i)+Da(d)(i-1)) | a(d)+dDy(i) |
| Colored set | y(d)+dDa(i) | y(d)+da(i)+d(i-1)min(Dy(d),Dx(d-1)) |
| Uncolored set | x(d)+dDa(i) | x(d)+da(i)-a(4) |

For element branches, 2<=i<=d. For set branches, 2<=i<=d-1 because of the
tie order. In a merge, the new degree is at most the sum of residual neighbor
degrees. This sum is at least four, so a(4) is a valid weight upper bound.

For fixed d, exp(-drop1)+exp(-drop2) is convex in the neighbor-type counts.
Its maximum occurs at a uniform neighborhood. Only d=4,5,6,7 need checking:
all weight terms have stabilized by seven, and larger d cannot lower either
drop. The verifier checks all 64 cases with exact rational upper bounds on
the exponential. The minimum slack is greater than 0.00001293.

## Bound and core invariant

The initial measure obeys

```text
mu < [a(4)+x(4)*8/7] k = (376179571/700000000) k.
exp(376179571/700000000) < 1.7116.
```

The subcubic width bound is w<=n3/6+.01n+O(1).
Since degree-three weights are at least .14587977 and every core weight is
at least .09903381, ln(2)w<.871mu+O(1). Thus the terminal cost fits exp(mu).
Summing the recursion potential at each depth gives the proposed bound.

Leaf peeling removes trees, each attached to at most one core vertex.
Deletions cannot return an old tree vertex to the core. When a set is
contracted, its neighboring elements merge into one root; each attached tree
still has one attachment. The merged element is the only possible new core
vertex and is charged at most a(4). Other degrees do not increase.
This preserves the branch-drop argument without the twin annotation rule.

## Checks

```sh
python3 research/branch_certificate.py
python3 research/verify_colored_branching.py
```

The first script proves the 64 rational inequalities and the final base.
The second compares 2,766 complete profiles with exhaustive coloring and
checks actual measure drops. These checks support the proposal; they do not
establish publication priority or replace external review.
