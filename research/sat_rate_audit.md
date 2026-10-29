# A stronger transfer through selector moments

29 October 2026. This note gives a simpler and stronger replacement for the
large-edge branching reduction in `conditional_subexponential.md`.

## Counting transform with only O(n+m) variables

Let H have n Boolean vertices and m labeled hyperedges of arbitrary rank. For
a coloring x, let u(x) be its number of monochromatic (unsplit) edges. Define

    a_j = number of x with u(x)=j,
    F_t = sum_x binom(u(x),t),  t=0,...,m.

For each edge e introduce a selector y_e. If e is nonempty, choose an anchor
a in e and include, for every v in e\{a}, the two clauses

    (not y_e OR not x_a OR x_v),
    (not y_e OR x_a OR not x_v).

They express only `y_e implies x_a=x_v`. Thus y_e may be 1 exactly when e is
monochromatic. Empty and singleton edges require no such clauses and their
selectors remain free, as they should: those edges are always unsplit.

Require exactly t of the m selectors to be true using a balanced binary
adder and unique-extension Tseitin encoding. This uses O(m) additional
variables and O(m) width-three clauses. For each fixed x, satisfying selector
assignments are exactly the t-subsets of its u(x) monochromatic edges.
Auxiliary gate values are unique once x and the selectors are fixed.
Consequently the satisfying-assignment count is exactly F_t.

The formula has v=O(n+m) variables, every clause has width at most three,
and its clause count is O(I+m), where I=sum_e |e|. No variable is introduced
per incidence. In particular I<=nm for a set system, so the formula and
its encoding length are polynomial in n+m even when its clause density
is unbounded.

The generating identity is

    Q(z)=sum_t F_t z^t=sum_x (1+z)^{u(x)}=sum_j a_j(1+z)^j.

Thus

    a_j = sum_{t=j}^m (-1)^{t-j} binom(t,j) F_t.

Computing the m+1 counts F_t and applying this inverse binomial transform
recovers the full split-count polynomial. Counts F_t are at most 2^(n+m),
and transform intermediates have O(n+m+log(m+1)) bits, so arithmetic and
space overhead are polynomial.

### Explicit linear variable bound

There are n color variables and m selector variables. Pad the selector list
with constant false inputs to a power of two p<2m (for m>0). At level h of a
balanced sum tree there are p/2^h additions of h-bit input numbers. One
ripple-carry addition uses at most 6h Boolean gates (two XOR, three AND, and
one OR per position suffice); no input or new variable is needed for padded
false constants. Thus the number of addition gates is at most

    sum_{h>=1} (p/2^h)*6h <= 12p < 24m.

The exact-t condition is imposed with O(log(m+1)) unit clauses on the final
sum bits and does not require comparator variables. Consequently at most
n+25m+1 variables suffice, with one constant variable if needed. The harness
uses a slightly more economical unpadded construction and asserts the safe
bound n+20*max(1,m). This constant is immaterial to the asymptotic transfer.

### Pinned inputs and constructive optimization

Any subset of element colors can be fixed by unit clauses without adding
variables. The identical moment identity then counts only colorings
consistent with those pins. From the original profile obtain the largest
split count s* with positive coefficient. Process the n element variables
in order: query the profile after tentatively pinning the next bit to 0;
retain 0 if the s* coefficient is positive and otherwise retain 1. An optimal
completion always remains. At most n additional profile computations find an
optimal coloring, preserving the displayed time and polynomial-space bounds
up to polynomial factors. This statement concerns the original hypergraph
with complexity parameter n+m; using it after a decision kernel requires
the kernel's witness-lifting procedure if the original witness is desired.

### A general profile-counting transfer

The same construction works for any m predicates Phi_e(x), each supplied as
a 2-CNF on the original n variables. Add selector y_e and prefix every clause
C in Phi_e by `not y_e`, giving the 3-CNF clause `(not y_e OR C)`. With exactly
t selectors true, satisfying assignments count the binomial moment of the
number of satisfied predicates. An inverse binomial transform therefore
recovers their complete satisfaction-count profile with O(n+m) variables
and polynomial overhead in the total predicate description length.

Set Splitting uses the 2-CNF predicate saying that an edge is monochromatic.
The violated-clause predicate of an arbitrary CNF clause is a conjunction of
unit literals, hence is also covered. Thus the same theorem yields exact
MAX-SAT value distributions and optimal assignments for arbitrary clause
width in subexponential time in n+m under the external #3SAT theorem. This
does not imply subexponential time in n alone when m is much larger than n.

## Quantitative consequence

The conservative theorem documented by the external Lean scope note counts
arbitrary 3-CNF formulas in poly(L) times

    2^O(v*(log log v)^2/sqrt(log v))

and polynomial space. Applying it to the selector formulas gives the same
bound with v replaced by N=n+m, up to polynomial factors. This computes
the full split-count distribution of the original H.

For parameterized Set Splitting first apply the established decision kernel,
then delete unsplittable sets and answer YES if m>=2k by the expectation
bound. The unresolved kernel has n<=k,m<2k. Counting only this reduced
instance therefore decides the original in

    |I_original|^O(1) +
    2^O(k*(log log k)^2/sqrt(log k))

and polynomial space. This is a strictly stronger quantitative transfer than
the earlier exponent k*(log log k)^(3/2)/(log k)^(1/4).

If one uses the sharper **general-density** bound stated in the revised
October-25 manuscript, the consequence improves to

    |I_original|^O(1) +
    2^O(k*log log k/sqrt(log k)).

The manuscript's fixed-density rate cannot be substituted directly: the
selector clauses can have density Theta(k). The present reduction does not
justify dropping the remaining log log factor. Using a per-incidence Tseitin
encoding to force fixed density would lose the O(k) variable bound.

## Source audit

- General statement and rates: https://raw.githubusercontent.com/openai/math/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/build/main_full_version.tex
- Formalization scope: https://github.com/openai/math/blob/main/lean/docs/378.md
- Kernel: https://sites.cs.ucsb.edu/~daniello/papers/setSplitIWPEC09.pdf

The revised source states the sharper general- and fixed-density rates in
its main theorem, while the Lean scope documents the conservative rate.
The source refers to an appendix labeled `app:quantitative`; the raw source
retrieved for this audit contains that reference but I did not locate the
appendix's actual label or proof. The paper should state exactly which
external theorem is assumed rather than claim to have independently checked
that external result or its sharper quantitative proof.

The selector transform itself is a standard binomial-moment/partition-function
construction; novelty, if any, lies in its application to the quantitative
Set Splitting transfer. A fuller literature audit is needed before claiming
priority.

## Reproducible checks

`python3 research/selector_moments.py` compares all moment counts and the
recovered complete split profile against exhaustive coloring for every simple
hypergraph on up to three vertices, plus 100 seeded random labeled instances
on at most six vertices, including repeated, empty, and singleton edges.
The #3SAT backend in this test is the tiny exhaustive DPLL oracle in
`research.py`, not an implementation of the new counting theorem.
The harness also performs 20 optimal-coloring self-reductions, verifies the
result against exhaustive search, and checks that fully pinned profiles
contain exactly that one coloring.
