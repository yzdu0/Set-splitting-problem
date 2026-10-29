# Set Splitting: research outcome

29 October 2026. **Research claim; independently unreviewed.**

I obtained a proposed deterministic **O*(1.7116^k)** algorithm for unweighted
parameterized Set Splitting. It uses exponential space. Here k is the target
number of sets split, and O* suppresses polynomial factors in the input size.
The proposal has a mathematical derivation and an exact rational branching
certificate. It has not been formally verified or reviewed by an outside
researcher, and a full implementation with the claimed running time has not
been built. Publication priority has not been established.

The strongest older specialized result verified in the literature search is
O*(1.7171^k) time and exponential space; its polynomial-space alternative is
O*(1.8213^k). The source is Nederlof, van Rooij, and van Dijk,
[Inclusion/Exclusion Meets Measure and Conquer](https://doi.org/10.1007/s00453-013-9759-2),
Algorithmica 69 (2014), 685–740; see its
[author manuscript](https://www.researchgate.net/publication/287264463_InclusionExclusion_Meets_Measure_and_Conquer).
The slide's 4^(k²+k) bound is therefore a substantially older starting point.

## Proposed theorem and proof outline

**Proposed theorem.** Unweighted Set Splitting with target k can be decided
deterministically in O*(1.7116^k) time and exponential space, using the
established decision kernel and structural pathwidth theorem together with
the terminal lemma and measure certificate in this directory. This claim
does not depend on ETH, its negation, or the recent #SAT announcement.

The instance is a universe U, a family F of subsets, and an integer k. We ask
for a coloring U -> {0,1} that makes at least k sets nonmonochromatic.
Empty and singleton sets cannot split. Distinct set labels must remain
distinct if later contractions make their underlying subsets equal.

1. Use the established
   [Lokshtanov–Saurabh kernel](https://sites.cs.ucsb.edu/~daniello/papers/setSplitIWPEC09.pdf)
   to obtain a decision-equivalent instance with at most k remaining elements
   (or answer the instance directly). Use the reduced target if it decreases.
   A random coloring splits a size-i set with probability
   p_i = 1 - 2^(1-i). If sum_i p_i s_i >= k, conditional expectation gives a
   YES answer. Otherwise retain the inequality sum_i p_i s_i < k. This also
   ensures fewer than 2k nontrivial sets. This kernel need not preserve counts:
   the subsequent algorithm counts only the reduced instance.
2. Use the variable-coloring and set deletion/contraction branching framework.
   Maintain whether a residual set contains an already assigned color. A set
   containing both assigned colors is already split and contributes an offset.
   For an uncolored set e, the split-count polynomial obeys

       P_H(z) = z P_(H-e)(z) + (1-z) P_(H/e)(z).

   Here H/e deletes e and merges all its vertices, retaining the labels of all
   other sets. For a set already containing color b, its unsplit branch instead
   forces all remaining elements in it to b. Branching on an element uses its
   two color assignments. These operations count all colorings exactly.
3. **Change the annotation rule:** use only repeated degree-zero/one peeling,
   recomputing the ordinary 2-core after each branch. Do not apply the old
   degree-two-twin annotation. That old annotation can create a rank-three
   effective connection, so merely substituting a binary terminal solver in
   the original algorithm would be invalid. An explicit obstruction is in
   [the tensor note](research/tensor_candidate.md).
4. Branch while the 2-core has a vertex of degree at least four. Prefer an
   element in a maximum-degree tie, then an uncolored set, then a colored set.
   When the core has maximum degree three, use the new terminal solver below.

### Terminal solver

Represent each incidence by a Boolean port. Element nodes enforce equality
of their ports; set nodes contribute z when split and 1 otherwise. Peeling
removes pendant trees, each of which sends a two-entry message to at most one
core node. Original high-arity factors are sums of at most three product
tensors, so these messages are computable in polynomial time. Only tensors
of arity two or three remain at core nodes.

For a ternary tensor with two matrix slices A and B, perturb the slices to
A+epsilon I and B+epsilon diag(1,2). The first is invertible and their matrix
ratio has distinct eigenvalues except at at most six epsilon values. At all
other values the tensor is a sum of two product tensors over a single common
quadratic finite field. This converts the network to a binary pairwise model
on the **same core graph**. Its partition function takes O*(2^w) time on a
width-w decomposition. Interpolation handles the exceptional tensors,
including those that actually have tensor rank three. A second interpolation
recovers the polynomial in z, and CRT recovers its integer coefficients.
All additional work and arithmetic bit lengths are polynomial.

This uses established tensor factorization ideas; the proposed contribution
is their application to this modified Set Splitting analysis. The complete
algebraic argument, field choices, exceptional-point bounds, and a warning
about the old annotation rule are in
[tensor_candidate.md](research/tensor_candidate.md).

### Certified measure and global bound

Assign logarithmic weights a to core elements, x to uncolored core sets,
and y to core sets containing one assigned color:

| Degree | a | x | y |
|---|---:|---:|---:|
| 2 | .14213804 | .13207999 | .09903381 |
| 3 | .21320706 | .21642156 | .14587977 |
| 4 | .24168709 | .25874826 | .18044649 |
| 5 | .24168709 | .27075585 | .20049150 |
| >=6 | .24168709 | .27586196 | .20447113 |

Let mu be the sum of these weights over the ordinary 2-core. The detailed
branch-drop derivation is in
[branch_certificate.md](research/branch_certificate.md). Omitting twin
annotations does not remove any drop used in those displayed inequalities:
they use degree bounds, concavity, color changes, and the cost of merging
elements. Peeling additional leaves only lowers the measure. The effect of
the graph operations on pendant trees must be accounted for; no arbitrary
old annotation marks are carried into a new call.

For fixed branching degree, exp(-drop1)+exp(-drop2) is convex in neighborhood
type counts, so homogeneous neighborhoods suffice. The degree caps make all
degrees >=7 a monotone tail. This reduces the infinite recurrence family to
64 explicit inequalities. Every one passes an exact rational Taylor upper
bound, with minimum slack greater than 0.00001293.

The initial measure satisfies

    mu < [a(4) + max_i x(i)/p_i] k
       = [a(4) + x(4)*8/7] k
       = (376179571/700000000) k.

The certificate proves, using rational arithmetic, that

    exp(376179571/700000000) < 1.7116.

For terminal graphs, the established structural theorem supplies a
polynomially constructible decomposition with

    w <= n3/6 + .01*n + O(1)

for sufficiently large graphs. Here n3 counts core vertices of degree three
and n counts all core vertices. The certificate establishes

    log(2)*w <= .871*mu + O(1).

Thus the terminal computation fits strictly within exp(mu). The finitely many
small graphs excluded by the structural theorem contribute a constant.
At every recursion depth the sum of exp(mu) over nodes is at most its value
at the root. Recursion depth is polynomial, and each node has polynomial
overhead. This gives O*(exp(mu_initial)), hence the proposed O*(1.7116^k)
bound. Terminal dynamic programming uses exponential space.

## Verification and limits

The following deterministic checks passed:

- 64 exact rational branch inequalities, including an analytic treatment of
  all larger degrees and the terminal-width budget.
- 990 exact finite-field ternary decompositions, 65 comparisons of equivalent
  K4 tensor networks, and 13 perturbation/interpolation reconstructions.
- 2,766 complete colored-branching profile comparisons, exercising variable,
  uncolored-set, and colored-set branches and checking their measure drops.
- 66,024 small-instance deletion/contraction identities, 750 recursive profile
  comparisons, 750 branching-leaf bounds, 70 exact-CNF count distributions,
  and 10,004 unique-extension checks for the circuit encoding.

Commands:

```sh
python3 research.py
python3 research/branch_certificate.py
python3 research/verify_tensors.py
python3 research/verify_colored_branching.py
```

[verification.json](verification.json) records the first harness's results.
These checks support the proof; finite testing does not establish an
asymptotic theorem. The terminal harness evaluates small networks directly,
and the general harness uses exhaustive search or a tiny DPLL oracle. They
are verification code, not a complete fast solver. In particular no practical
speedup has been demonstrated. The main remaining validation is independent
review of the full modified-algorithm proof and a fuller prior-art audit.

## Separate consequence of the very recent #SAT result

There is also a stronger **conditional** result. Assuming the fixed-width
exact-counting theorem released in October 2026, processing large sets by
deletion/contraction and encoding the bounded-rank leaves parsimoniously
gives deterministic polynomial-space time

    |I|^O(1) + 2^O(k*(log log k)^(3/2)/(log k)^(1/4)) = |I|^O(1) + 2^o(k).

This is separate from the 1.7116 proposal and depends on that recent external
theorem. It does not independently verify the external theorem or establish
priority for the consequence. Its full reduction, including a sharper rate
if the revised manuscript's density bound is accepted, is in
[conditional_subexponential.md](research/conditional_subexponential.md).
