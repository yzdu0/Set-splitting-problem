# A conditional subexponential algorithm for parameterized Set Splitting

**Status, 29 October 2026.** This is a reduction and complexity argument, conditional on the recently released subexponential exact-counting theorem for fixed-width CNF. The reduction below does not establish that external theorem, independently certify its formalization, or establish publication priority. Its elementary steps can be audited separately from that theorem.

## Problem and external inputs

An instance consists of a universe \(U\), a family \(\mathcal F\) of subsets of \(U\), and an integer \(k\). The question is whether a coloring \(\chi:U\to\{0,1\}\) makes at least \(k\) members of \(\mathcal F\) nonmonochromatic. Here \(k\) counts sets that must be split; it is not a bound on set size.

We use two external inputs:

1. **Established decision kernel.** Lokshtanov and Saurabh give an equivalent instance with parameter \(k'\le k\), at most \(k\) elements, and at most \(2k\) sets, in polynomial time. Their proof additionally shows that an unresolved reduced instance has at most \(k'\) elements. Its bound on the number of sets is stated in terms of the original \(k\); the elementary additional preprocessing below brings that number below \(2k'\). This is a decision-preserving kernel. We do **not** assume it preserves numbers of colorings. [Even Faster Algorithm for Set Splitting!, Theorem 1 and its proof](https://sites.cs.ucsb.edu/~daniello/papers/setSplitIWPEC09.pdf).
2. **Recent external counting theorem.** Assume a uniform deterministic algorithm exactly counts satisfying assignments of a 3-CNF with \(v\) declared variables and encoding length \(L\) in time
   \[
   (L+1)^{O(1)}2^{O\!\left(v(\log\log v)^2/\sqrt{\log v}\right)}
   \]
   and polynomial space. This is the conservative rate described in the [Lean scope note](https://github.com/openai/math/blob/main/lean/docs/378.md) accompanying [The Exponential Time Hypothesis is False, revised 25 October 2026](https://github.com/openai/math/blob/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/build/main_full_version.tex). Logarithms and formulas below are understood for sufficiently large arguments; finite small cases can be handled by exhaustive search.

The [official release of 26 October 2026](https://openai.com/index/building-scientific-understanding-with-academic-communities/) describes ongoing external examination. We treat the counting algorithm as an explicit external assumption here. The displayed rate is not a theorem proved in this note.

For comparison, the older specialized published algorithms give \(O^*(1.8213^k)\) time with polynomial space and \(O^*(1.7171^k)\) time and exponential space. See [Nederlof, van Rooij, and van Dijk, Inclusion/Exclusion Meets Measure and Conquer, Theorems 18 and 23](https://doi.org/10.1007/s00453-013-9759-2), with an [author-posted manuscript](https://www.researchgate.net/publication/287264463_InclusionExclusion_Meets_Measure_and_Conquer).

## Conditional result

**Theorem.** Under external input 2 above, parameterized Set Splitting admits a uniform deterministic algorithm using polynomial space and time
\[
|I|^{O(1)}+
2^{O\!\left(
\frac{k(\log\log k)^{3/2}}{(\log k)^{1/4}}
\right)}.
\]
In particular, its dependence on \(k\) is \(2^{o(k)}\). This is an implication of the recent external counting theorem, not an unconditional improvement independent of it.

### 1. Kernelize for decision

Apply external input 1. If the kernelization directly answers the instance, stop. Otherwise work only with its reduced instance. If its target \(k'\le0\), answer yes. Delete empty and singleton sets, since they never split. If the number \(m\) of remaining sets satisfies \(m\ge2k'\), answer yes: a uniformly random coloring splits each remaining set with probability at least one half, so its expected number of split sets is at least \(m/2\ge k'\), and some coloring attains that expectation. This can also be made constructive by conditional expectations.

For an unresolved instance, we now have \(n\le k'\) and \(m<2k'\). Rename its parameter to \(k\) for the remainder of the proof. Because this parameter is at most the original parameter, a running-time upper bound in terms of it also gives the claimed upper bound in terms of the original parameter.

All counting in the rest of the algorithm concerns this reduced instance. Its split-count distribution need not equal the original instance's distribution. This causes no problem: deciding whether the reduced distribution has a positive coefficient at an index at least its reduced target answers the original decision problem.

Empty and singleton sets can be deleted because they never split. Isolated elements must either be retained or, if deleted, contribute a factor of two per element in every counting operation.

### 2. A generating-polynomial recurrence

For a residual hypergraph \(H\), define
\[
P_H(z)=\sum_{\chi:V(H)\to\{0,1\}}z^{s_H(\chi)},
\]
where \(s_H(\chi)\) is the number of sets split by \(\chi\).

Residual sets are **labeled occurrences**: if contraction turns two different sets into the same subset, both occurrences are retained. Deleting duplicates would change the optimization problem.

For a selected set \(e\), let \(H-e\) delete that one occurrence. Let \(H/e\) first delete that occurrence and then identify all vertices of \(e\) into one vertex, applying this identification to every other set. In particular, \(H/e\) retains all other set labels, even when their images coincide. Then
\[
\boxed{P_H(z)=zP_{H-e}(z)+(1-z)P_{H/e}(z).}
\]

**Proof.** For a coloring of \(H-e\), write \(s\) for its number of split sets there. If it splits \(e\), its contribution to \(P_H\) is \(z^{s+1}\). If it does not split \(e\), its contribution is \(z^s\), while the first term on the right assigns it \(z^{s+1}\). Colorings for which \(e\) is monochromatic are in bijection with colorings of \(H/e\); each such pair splits the same number of the other labeled sets. Thus the correcting contribution is \((1-z)z^s\), proving the identity.

The coloring of the contracted vertex can be either 0 or 1, so there is no extra factor of two in the contraction term.

### 3. Process large sets with a small branching tree

Fix an integer \(r\ge4\). Repeatedly apply the recurrence to a set of current size at least \(r\), stopping along a branch as soon as all remaining sets have size less than \(r\).

Each recurrence deletes its selected set in both children, so every root-to-leaf path has length at most the original \(m\le2k\). A contraction child reduces the number of vertices by at least \(r-1\). Consequently each root-to-leaf path has at most
\[
b=\left\lfloor\frac{n-1}{r-1}\right\rfloor\le\frac{k}{r-1}
\]
contraction steps. The case \(n=0\) is trivial and can be handled before this argument.

Encode deletion as 0 and contraction as 1, and pad a root-to-leaf word with zeros to length \(2k\). Distinct leaves have distinct padded words: otherwise one unpadded leaf word would be a prefix of another, which is impossible in a tree. The number of leaves is therefore at most
\[
\sum_{j=0}^{\min(b,2k)}\binom{2k}{j}
=2^{O(k\log r/r+\log k)}.
\]
For large \(r\) with \(r\ll k\), this follows from the standard binomial-tail bound \(\sum_{j\le b}\binom{2k}{j}\le(b+1)(2ek/b)^b\). For bounded small \(r\) the same big-O expression remains a valid coarse bound. The tree is binary, so its total number of nodes is at most twice its leaf count minus one.

This step avoids enumerating all \(2^m\) subsets of large sets. A large-set contraction consumes many vertices, which limits how many such choices can occur in one path.

### 4. Count the distribution at each bounded-rank leaf

At a leaf there are at most \(k\) elements, at most \(2k\) labeled sets, and fewer than \(r\) incidences per set. For \(t=0,\ldots,m_H\), let
\[
A_t=\#\{\chi:s_H(\chi)\ge t\}.
\]
Also set \(A_{m_H+1}=0\). The coefficient of \(z^t\) in \(P_H\) is exactly \(A_t-A_{t+1}\).

For each threshold \(t\), construct a Boolean circuit whose input bits are the element colors and whose output is true exactly when at least \(t\) sets split:

- A set \(e\) is split precisely when
  \[
  \left(\bigvee_{u\in e}x_u\right)\wedge
  \left(\bigvee_{u\in e}\neg x_u\right).
  \]
  Fan-in-two AND, OR, and NOT gates compute this with \(O(|e|)\) gates. Across all sets this uses \(O(rk)\) gates.
- Sum the resulting \(m_H\) indicator bits using a balanced binary tree of binary adders, then compare the result with the constant threshold \(t\). The total gate count of the sum is \(O(m_H)\), not \(O(m_H\log m_H)\): at level \(h\) there are \(O(m_H/2^h)\) additions of \(O(h)\)-bit integers, each needing \(O(h)\) fixed-fan-in gates, and \(\sum_{h\ge1}h/2^h<\infty\). The comparator costs \(O(\log(m_H+1))\) gates. Padding the input count to the next power of two changes only a constant factor.

Use a parsimonious Tseitin encoding: introduce a variable for each gate, impose its full logical equivalence to its input operation, and require the circuit output to be true. For example, \(g\leftrightarrow(a\wedge b)\) is encoded by \((\neg g\vee a)\wedge(\neg g\vee b)\wedge(g\vee\neg a\vee\neg b)\). OR and NOT have analogous constant-size encodings.

Every assignment of the original element-color inputs has **exactly one** extension to all gate variables. Thus the number of satisfying assignments of this 3-CNF is exactly \(A_t\). Using implications in only one direction would not justify this counting claim.

The formula has \(v=O(rk)\) variables and \(O(rk)\) clauses, with a universal constant bound on the clause-to-variable ratio. Its encoding length is \(O(rk\log(rk))\). Clauses of width one or two can be padded by repeating a literal if the counting routine expects exactly three literal occurrences. Such padding does not change satisfying assignments. For \(t=0\), \(A_0=2^{|V(H)|}\) can be computed directly.

The assumed counting algorithm computes all \(A_t\) by at most \(m_H+1=O(k)\) calls, so a leaf costs
\[
\operatorname{poly}(rk)\,
2^{O\!\left(
\frac{rk(\log\log(rk))^2}{\sqrt{\log(rk)}}
\right)}.
\]
Small formulas can be handled directly. The asymptotic expression is an upper bound for all formulas of size at most \(O(rk)\), by taking the monotone upper envelope of the counting-time bound if necessary.

### 5. Recover the root and analyze time and space

Evaluate the branching recurrence bottom-up to recover the root polynomial. The target answer is yes exactly when some coefficient at an index \(t\ge k\) is positive. All polynomial degrees are at most \(2k\), and coefficients at a node count colorings of its residual hypergraph, so they have \(O(k)\) bits. The two summands used to combine children also have polynomial bit length, despite the subtraction inherent in \(1-z\).

Combining the leaf bound and the work per leaf gives, up to polynomial factors,
\[
T(k,r)\le
2^{O\!\left(
\frac{k\log r}{r}
+\frac{rk(\log\log(rk))^2}{\sqrt{\log(rk)}}
\right)}.
\]
Choose, for sufficiently large \(k\),
\[
r=\left\lceil\frac{(\log k)^{1/4}}{\sqrt{\log\log k}}\right\rceil,
\]
and use \(r\ge4\) for finite exceptional values. Then \(\log r=O(\log\log k)\), \(\log(rk)=\Theta(\log k)\), and both contributions to the exponent are
\[
O\!\left(
\frac{k(\log\log k)^{3/2}}{(\log k)^{1/4}}
\right)=o(k).
\]
The choice is computable and calls one fixed 3-CNF counting algorithm, so no nonuniformity or diagonalization is needed.

A depth-first traversal needs only the current recursion path of length at most \(2k\), a polynomial-size residual hypergraph at each depth, one saved child polynomial per active node, and the polynomial-space counting routine at a leaf. Since \(r\) is polylogarithmic in \(k\), total space is polynomial in the input size. The initial kernelization costs polynomial time and space. This proves the conditional theorem.

## Sharper rate if the manuscript's sparse-density theorem is accepted

The revised manuscript also states a stronger bound for a fixed clause density \(D\): a 3-CNF with \(v\) variables and at most \(Dv\) clauses can be counted in time
\[
\operatorname{poly}(v)2^{O_D(v/\sqrt{\log v})}
\]
using polynomial space. The Tseitin formulas above have a universal fixed density (for example, at most four clauses per variable after a harmless treatment of tiny cases), so this stronger statement would give
\[
T(k,r)\le
2^{O\!\left(\frac{k\log r}{r}
+\frac{rk}{\sqrt{\log(rk)}}\right)}.
\]
Choosing
\[
r=\left\lceil(\log k)^{1/4}\sqrt{\log\log k}\right\rceil
\]
yields
\[
|I|^{O(1)}+
2^{O\!\left(
\frac{k\sqrt{\log\log k}}{(\log k)^{1/4}}
\right)}
\]
with polynomial space. This uses the sharper manuscript rate; it should not be described as the precise bound documented in the accompanying Lean scope note.

## What is and is not established here

- The polynomial recurrence, its large-set branching bound, the parsimonious bounded-rank encoding, and the transfer calculation are explicit deductions in this note.
- Their combination gives a parameter-subexponential algorithm **conditional on the external fixed-width exact-counting theorem**. It does not follow from the old Set Splitting algorithms alone.
- The method counts colorings of a reduced decision kernel. It does not provide a counting kernel for the original instance.
- This note does not implement the new counting theorem, validate its entire proof, demonstrate practical speed, or claim that this consequence has not already been observed elsewhere.
