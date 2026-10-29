# Branching certificate for a proposed 1.7116^k algorithm

Status: this document certifies the branching and initial measure calculation.
The separate tensor terminal lemma must also hold to obtain the full claimed
algorithm. Numerical optimization alone is not used as a proof.

Use the kernel and expectation preprocessing from Nederlof, van Rooij and van
Dijk, *Inclusion/Exclusion Meets Measure and Conquer*, Sections 5.1 and 6.2.
The residual instance has at most k elements and satisfies

    sum_{i>=2} (1-2^(1-i)) s_i < k.

Modify their Algorithm 2 by **omitting its degree-two-twin annotation rule**.
Keep only annotation of vertices of induced degree at most one. Equivalently,
recompute the ordinary 2-core after every branch. Branch as in the paper while
the core has maximum degree at least four, and use the new tensor terminal
algorithm when its maximum degree is at most three.

The distinction between the full incidence graph and its 2-core matters. The
old twin annotations cannot simply be inherited: summing two twin element
vertices joining two sets gives a rank-three effective connection, which a
single binary bond cannot represent. Leaf annotations alone leave pendant
trees, each attached to at most one core vertex. Their exact contractions leave
Boolean tensors of arity at most three at the terminal core vertices.

## Measure

Use natural logarithmic weights: a for an element, x for an uncolored set,
y for a set containing an assigned color. Set weights at degrees zero and one
to zero. Set

| degree | a | x | y |
|---|---:|---:|---:|
| 2 | .14213804 | .13207999 | .09903381 |
| 3 | .21320706 | .21642156 | .14587977 |
| 4 | .24168709 | .25874826 | .18044649 |
| 5 | .24168709 | .27075585 | .20049150 |
| >=6 | .24168709 | .27586196 | .20447113 |

Let mu be their sum over the ordinary 2-core. The intended bound is exp(mu),
so each two-branch recurrence requires exp(-drop1)+exp(-drop2)<=1.
These weights are exact terminating decimals, hence exact rationals.

For a weight function z write Dz(i)=z(i)-z(i-1). The monotonicity, concavity,
y<=x, 2Da(3)<=a(2), and 2 min(Dy(4),Dx(3))<=y(2) conditions of the paper's
Lemma 17 hold. They ensure that edge losses, including repeated losses at a
single neighbor, are not overcounted in the following lower bounds. Recomputing
the 2-core can only produce additional measure decreases.

## Branch inequalities

Let d>=4 be the maximum core degree of the chosen vertex and i the degree of
one of its neighbors. The following formulas are Lemma 17's formulas after
specializing to homogeneous neighborhoods and the capped a weights.

1. Element, all neighbors uncolored (2<=i<=d): both branches drop at least

       a(d) + d*(x(i)-y(i-1)).

2. Element, all neighbors carrying one color (2<=i<=d): the two drops are at least

       a(d) + d*(y(i)+Da(d)*(i-1)),
       a(d) + d*Dy(i).

3. Colored set (2<=i<=d-1): drops are at least

       y(d) + d*Da(i),
       y(d) + d*a(i) + d*(i-1)*min(Dy(d),Dx(d-1)).

4. Uncolored set (2<=i<=d-1): drops are at least

       x(d) + d*Da(i),
       x(d) + d*a(i) - a(4).

For (3) and (4), the strict bound i<=d-1 follows from the paper's priority
order: an element is chosen in any tie, then an uncolored set, then a colored
set. In (4), merging all neighbors has resulting degree at most the sum of
their residual degrees; that sum is at least d>=4, so its weight upper bound
is exactly a(4). Actual parallel incidences can collapse, causing further
reductions and never invalidating this upper bound.

It suffices to check homogeneous neighborhoods. For fixed d, both drop lower
bounds are linear in the counts of neighbor types and degrees; therefore the
sum of their negative exponentials is a convex function on the simplex of
these counts. Its maximum occurs at a simplex vertex, where all neighbors
have the same type and degree. The two possible fixed colors are symmetric.

It suffices to check d=4,5,6,7. For d>=7 all three weight functions have
stabilized. In (1), x(i)-y(i-1) stabilizes at i=7. In (2), Da(d)=0 and both
y(i) and Dy(i) stabilize at i=7. In (3), min(Dy(d),Dx(d-1))=0; a(i),Da(i)
stabilize at i=5. In (4), these same a terms stabilize at i=5. Thus at d=7
every neighbor type possible at any larger degree is already represented.
Increasing d then only increases, or leaves unchanged, both drop bounds,
since all relevant coefficients are nonnegative. This proves the infinite
tail rather than sampling it.

The verifier checks all 64 remaining inequalities using **rational upper
bounds** on exp(-drop), given by the even Taylor polynomial of degree 80.
Taylor's remainder has negative sign, so each such polynomial is an upper
bound for every nonnegative drop. The minimum certified slack below one is
greater than 0.00001293.

## Initial measure and exponential base

The maximum ratio x(i)/(1-2^(1-i)) is achieved at i=4 and equals

    .25874826 * 8/7.

Degrees at least seven introduce no greater ratio because x is constant and
the denominator increases. As every element has weight at most a(4),

    mu < [a(4)+.25874826*8/7] k
       = (376179571/700000000) k
       = 0.537399387142857... k.

An exact rational upper bound on the positive exponential series proves

    exp(376179571/700000000) < 1.7116.

Hence a terminal algorithm costing at most exp(mu) yields O*(1.7116^k)
overall. One can bound the recursion by induction, or by summing over the
polynomially many possible measures: all weights have one fixed rational
denominator and the number of residual vertices is polynomial in the kernel
size. This absorbs polynomial overhead without changing the displayed base.

## Terminal budget

This paragraph assumes the separate proposed lemma: a subcubic Boolean tensor
network on G can be contracted in O*(2^tw(G)) time, with polynomial overhead
for exact counting. Degree-two vertices contribute no leading term to the
known pathwidth estimate. For each fixed epsilon>0 and sufficiently large G,

    tw(G) <= n3/6 + epsilon*n.

Every core degree-three vertex has weight at least y(3)=.14587977, and every
core vertex has weight at least y(2)=.09903381. Taking epsilon=.01 and using
ln(2)<.7 gives

    ln(2)*tw(G)
       <= [.7/(6*.14587977)+.007/.09903381]*mu
       < .871*mu.

The terminal thus has ample budget below exp(mu). The finitely many small
graphs excluded by the pathwidth theorem can be solved by brute force at a
constant cost depending only on epsilon. Pendant-tree contractions add only
polynomial work and do not count in this core-width estimate.

## Remaining proof obligation

The certificate establishes all branching bounds for the leaf-stripping
variant provided the inherited combinatorial reductions and the separate
subcubic tensor terminal lemma are valid. In particular, the generic tensor
lemma needs exact, polynomial-bit arithmetic and must handle exceptional
rank-three Boolean ternary tensors; an argument applying only to the original
symmetric NAE tensor does not suffice after pendant-tree contractions.

## Why recomputing the ordinary 2-core is safe

For any graph, vertices deleted by iterative degree-at-most-one stripping
induce a forest. Every component of this forest meets the surviving 2-core
through at most one edge: a cycle, or a path between two surviving vertices,
would prevent all its vertices from ever being stripped. This is a purely
graph-theoretic statement about the incidence graph; no constraint is dropped
from the counting problem. All annotated vertices and their constraints remain
in the full problem until the exact terminal contraction.

Deleting a vertex or an edge cannot make an old stripped vertex enter the
new 2-core. Ordinary element-coloring and colored-set-forbidden branches are
such deletions (plus color annotations), and optional branches also only
delete a constraint vertex. Hence the core losses used by Lemma 17 remain
valid, and any additional stripping supplies further nonnegative losses.

The only operation that identifies vertices is the forbidden branch on an
uncolored set w. It deletes w and identifies its neighboring element vertices.
Each old stripped-tree component not attached to w meets at most one old core
vertex; identifying several core neighbors merely identifies some of these
attachment roots. Such pendant trees remain pendant after this identification.
Each old stripped-tree component attached to w contains exactly one neighbor
of w. Deleting w and identifying that neighbor with the new merged element
again attaches the remainder of this tree at exactly one root. Therefore no
old stripped vertex other than an identified neighbor can enter the new core.
The merged element is the one new vertex already charged at weight at most
a(4) in the forbidden-branch formula. Parallel incidences may collapse and
further reduce core degrees, which only helps the measure decrease.

For the original surviving vertices, degrees never increase in a branch;
the merged element is the sole possible exception. Thus the paper's
monotonicity and concavity bounds apply to all edge losses. The key repeated
loss inequalities are exactly the displayed 2Da(3)<=a(2) and
2min(Dy(4),Dx(3))<=y(2), preventing a degree-two vertex from being charged
more than its entire weight when both incident edges disappear. Neither
argument requires that degree-two twins be annotated.

## Executable semantic verification

`verify_colored_branching.py` implements the full three-rule recursion with
ordinary 2-core recomputation and checks its entire split-count profile against
exhaustive colorings. Its terminal deliberately uses brute force, so this is
a correctness check of the branching semantics, not a timing demonstration.
Every actual branch also checks its exact rational measure decrease against
the claimed recurrence lower bound.

The check covers all 2,048 simple uncolored hypergraphs on four vertices
without size-at-most-one sets, 700 seeded random partially colored instances
on up to nine vertices (allowing repeated sets), and 18 additional instances
forcing the set branching rules. The 2,766 comparisons pass, exercising
5,997 element branch nodes, 417 uncolored-set branch nodes, and 653 colored-set
branch nodes. Run:

    python3 research/verify_colored_branching.py

Run:

    python3 research/branch_certificate.py
