# Independent audit of the SAT-based transfer

29 October 2026. This audit concerns the transfer argument, not an independent
verification of the external exact-counting theorem.

## Verdict and subsequent strengthening

The selector-moment reduction discovered during the continued investigation
strictly supersedes the cutoff bound audited below. Its generalized form is
sound: let Phi_1,...,Phi_m be 2-CNF predicates on n original variables, with C
clauses in total. Introduce one selector y_i for each predicate, and replace
each clause D in Phi_i by (not y_i or D). This has width at most three and
uses no additional variables for the predicate descriptions. Add a linear-size
balanced population-count circuit requiring exactly t true selectors, with
full Tseitin gate equivalences. The resulting formula has O(n+m) variables
and O(C+m) clauses.

For a fixed original assignment x making u(x) predicates true, exactly
binom(u(x),t) selector assignments meet these requirements. The gate variables
have a unique extension. Therefore the exact #3SAT answer is

    F_t = sum_x binom(u(x),t).

If A_j counts original assignments making exactly j predicates true, binomial
inversion gives

    A_j = sum_{t=j}^m (-1)^(t-j) binom(t,j) F_t.

Equivalently, sum_j A_j z^j = sum_t F_t (z-1)^t. This determines the entire
profile using m+1 counting calls, polynomial exact arithmetic, and polynomial
space. Every F_t is at most 2^(n+m), and all intermediate arithmetic has
O(n+m+log(m+1)) bits up to a constant factor.

The selector implications are intentionally one-way. They encode binomial
moments, rather than directly encoding the profile. Only the deterministic
population-count gates need logical equivalences. This distinction is central
to the proof and avoids the incidence-proportional auxiliary-variable cost.

With s=n+m, the revised manuscript's general theorem now gives

    poly(L) * 2^O(s log log s / sqrt(log s)),

and its Lean-scope conservative rate gives

    poly(L) * 2^O(s (log log s)^2 / sqrt(log s)).

If C=O(s) with a fixed density constant, the sparse theorem improves this to
poly(L)*2^O(s/sqrt(log s)). It is essential not to use this sparse rate on
arbitrary hypergraphs with quadratic total incidence.

Empty predicates are true; predicates containing an empty clause force their
selector false. Thus degenerate predicates cause no exception. Original
variables remain declared even if they occur nowhere. Fixed original colors
are unit clauses, so the same construction computes conditional profiles and
supports deterministic witness self-reduction on the s-sized input.

For a hyperedge e, monochromaticity has a 2-CNF representation: fix a member
a, and for each v in e\{a} use (not x_a or x_v) and (x_a or not x_v). Empty
and singleton edges are always monochromatic. Apply the profile theorem to
these predicates and reverse the score j to m-j to obtain the split profile.
For an arbitrary SAT clause, its unsatisfaction predicate is the conjunction
of the negations of its literals, a 1-CNF. Thus arbitrary-width Max SAT is
another direct application in the n+m parameter.

The rest of this audit records the valid but weaker original cutoff argument.

## Audit of the original cutoff proof

No gap found in the deletion/contraction identity, binomial branching bound,
parsimonious circuit encoding, optimized cutoff, or polynomial-space
calculation in `conditional_subexponential.md`. The following stronger
organization makes the paper's contribution clearer and avoids relying on
a counting kernel.

## General exact-counting theorem

Let H have n explicitly represented vertices and m labeled hyperedges, put
s=n+m, and let L denote its explicit encoding length. Under the recent
linear-density #3SAT bound, the entire split-count polynomial is computable
deterministically in polynomial space and time

    poly(L) * 2^O(s * sqrt(log log s) / (log s)^(1/4)).

Under the conservative rate in the Lean scope note, replace sqrt(log log s)
by (log log s)^(3/2). No kernel is used in this statement.

Proof: branch only on edges of current cardinality at least r. A path has at
most m branching decisions and at most floor((n-1)/(r-1)) contraction choices.
Hence the number of leaves is at most

    sum_{j<=min(m,floor((n-1)/(r-1)))} binom(m,j)
    <= sum_{j<=floor(s/(r-1))} binom(s,j)
    = 2^O(s log r / r + log s).

The last upper bound holds for the chosen asymptotic cutoff 4<=r<<s. Every
leaf has fewer than r incidences per set, so its uniquely extending 3-CNF
encoding has O(n+rm)=O(rs) variables and constant clause density. Apply the
same cutoff balancing as in the existing proof, with s replacing k.
Polynomial arithmetic costs polynomial overhead: the polynomial has at most
m+1 coefficients, each at most 2^n.

The parameter-k decision theorem is then a direct corollary of the known
decision kernel, whose unresolved output has O(k) vertices plus sets. This
does not imply that kernelization preserves the original counting profile.

## Pinned assignments and witness extraction on the original s-sized input

The general exact-counting theorem extends to fixed colors on any subset of
vertices. Residual sets have one of three statuses: uncolored; containing
only assigned color b; or already split. Already split sets contribute a
known power of z and may be removed. An uncolored large set uses the usual
deletion/contraction identity. For a large set already containing color b,
the unsplit branch forces all its free vertices to b. This is a bijective
restriction of assignments, reduces the number of free vertices by at least
r, and can split other sets; account for those by a power-of-z offset.

Thus each nondeletion branch still consumes at least r-1 free vertices,
the same branching bound holds, and the leaf circuits remain O(n+rm) size.
At most n conditional-profile computations therefore find an optimal
coloring: maintain a partial assignment extendable to an optimum and choose
the next bit with positive conditional count at the optimum score. The same
conditional counts support exact uniform sampling among optimum colorings.
Sampling incurs the usual random-bit overhead and need not be included in
the main deterministic theorem.

This is an s=n+m search result. A parameter-k search claim on the original
input additionally needs either a solution-lifting kernel audit or a kernel
for pinned instances. The known kernel proof does include a constructive
component-flipping lift for its strong-cut reduction, but I did not audit
the earlier Chen--Lu preprocessing on which it relies. The safest main
parameter-k statement remains decision only.

## Details the paper should state explicitly

1. The imported primitive must be **exact #3SAT**, not merely a SAT decision
   oracle; deletion/contraction combines counts with subtraction.
2. The cutoff may grow with s, but the oracle's clause width stays exactly
   three. Consequently its hidden constants do not depend on the cutoff.
3. Require full gate equivalences in Tseitin encodings. One-way implication
   encodings do not establish a counting reduction.
4. A gate encoding has at most four clauses per gate. Adding one output unit
   clause gives a universal fixed density, for example D=5 after handling
   tiny formulas. The sparse-density constant is independent of r.
5. Retain edge labels after contraction. Different original sets can become
   equal, and merging their labels would change the objective.
6. Retain isolated vertices, or multiply their exact contribution by 2 for
   each removed free vertex. Empty and singleton sets never split.
7. Define the hypergraph input representation explicitly. If n is declared
   in binary and isolated vertices are implicit, writing an n-bit coefficient
   can be exponential in the bit length. The theorem assumes an explicit
   universe, or must separately charge the output length.
8. The kernel is linear in **numbers of elements and sets**. Its incidence
   encoding can still have quadratic size in k. Avoid calling its bit size
   linear without qualification.
9. Source-kernel precision: its final number of sets is initially bounded
   by 2 times the original target; its unresolved number of elements is at
   most the reduced target. Removing unsplittable sets and answering YES
   when m>=2k' repairs the target-renaming detail in the existing note.
10. Use asymptotic logarithmic expressions only beyond a fixed threshold;
    handle finitely many small arguments directly.

## Source checks

- The revised October 25, 2026 manuscript's main theorem explicitly states
  exact fixed-width counting, polynomial space, and the sharper bound at
  fixed clause density:
  https://github.com/openai/math/blob/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/build/main_full_version.tex
- Its Lean scope note documents the weaker general exponent with a squared
  log-log factor, and distinguishes the sharper manuscript rates:
  https://github.com/openai/math/blob/main/lean/docs/378.md
- Lokshtanov--Saurabh Theorem 1 and proof give the decision kernel and the
  unresolved n<=k' property; Lemma 1 contains a constructive strong-cut lift:
  https://sites.cs.ucsb.edu/~daniello/papers/setSplitIWPEC09.pdf

The recent manuscript already points out the direct consequence for splitting
all bounded-size sets. The general unrestricted-rank profile theorem above
and its parameter-k corollary require the additional large-edge branching
argument. This observation does not establish publication priority.
