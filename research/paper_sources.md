# Source and novelty audit for the SAT-based paper

Audit date: 29 October 2026. This file supplies source metadata and scope,
not a claim of publication priority.

## Verified bibliography

### Decision kernel

Daniel Lokshtanov and Saket Saurabh. **Even Faster Algorithm for Set
Splitting!** In Jianer Chen and Fedor V. Fomin, editors, *Parameterized and
Exact Computation*, IWPEC 2009, Lecture Notes in Computer Science **5917**,
pages **288–299**, Springer, 2009.
DOI: **10.1007/978-3-642-11269-0_24**.

Primary publisher page:
<https://link.springer.com/chapter/10.1007/978-3-642-11269-0_24>

Author manuscript:
<https://sites.cs.ucsb.edu/~daniello/papers/setSplitIWPEC09.pdf>

Theorem 1 gives a polynomial-time decision kernel with at most k elements
and 2k sets. It does not supply a counting kernel. Its second main result is
a deterministic O(1.9630^k+N) algorithm. For the new paper it is simplest to
keep K as the original target parameter: after kernelization the reduced
target may be k0<=K, but n<=K and m<=2K are all the complexity proof needs.
Test the computed profile at indices at least k0. This avoids unnecessary
dependence on whether every bound in the kernel proof uses K or k0.

```bibtex
@inproceedings{LokshtanovSaurabh2009,
  author = {Daniel Lokshtanov and Saket Saurabh},
  title = {Even Faster Algorithm for Set Splitting!},
  editor = {Jianer Chen and Fedor V. Fomin},
  booktitle = {Parameterized and Exact Computation},
  series = {Lecture Notes in Computer Science},
  volume = {5917},
  pages = {288--299},
  publisher = {Springer},
  year = {2009},
  doi = {10.1007/978-3-642-11269-0_24}
}
```

### Older specialized running times

Jesper Nederlof, Johan M. M. van Rooij, and Thomas C. van Dijk.
**Inclusion/Exclusion Meets Measure and Conquer.** *Algorithmica*
**69**(3):**685–740**, 2014.
DOI: **10.1007/s00453-013-9759-2**.

Primary author manuscript:
<https://www.researchgate.net/publication/287264463_InclusionExclusion_Meets_Measure_and_Conquer>

University record:
<https://research-portal.uu.nl/en/publications/inclusionexclusion-meets-measure-and-conquer/>

Table 2 and Theorems 18 and 23 give O*(1.8213^k) time with polynomial space
and O*(1.7171^k) time with exponential space. These are the strongest older
specialized published bounds located by this audit; avoid claiming an
exhaustive proof that no later paper improves them. The conference precursor
by Nederlof and van Rooij is IPEC 2010, LNCS 6478, pages 204–215, DOI
10.1007/978-3-642-17493-3_20. The manuscript has occasional year/label typos;
the 2014 journal record is the appropriate main citation.

```bibtex
@article{NederlofRooijDijk2014,
  author = {Jesper Nederlof and Johan M. M. van Rooij and Thomas C. van Dijk},
  title = {Inclusion/Exclusion Meets Measure and Conquer},
  journal = {Algorithmica},
  volume = {69},
  number = {3},
  pages = {685--740},
  year = {2014},
  doi = {10.1007/s00453-013-9759-2}
}
```

### Imported SAT/counting theorem

OpenAI. **The Exponential Time Hypothesis is False.** Preprint dated
**17 October 2026**, revised **25 October 2026**. The source explicitly lists
`\author{OpenAI}`; do not invent individual authors.

Primary manuscript:
<https://github.com/openai/math/blob/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/build/main_full_version.tex>

Formalization scope note:
<https://github.com/openai/math/blob/main/lean/docs/378.md>

Release/status context:
<https://openai.com/index/building-scientific-understanding-with-academic-communities/>

Theorem 1.1 (the source label is `thm:main`) states deterministic exact
counting for every fixed clause width d>=2, using polynomial space and time
poly_d(v,m) 2^{O_d(v loglog v/sqrt(log v))}; for every fixed density D the
bound improves to poly_{d,D}(v,m) 2^{O_{d,D}(v/sqrt(log v))} when m<=Dv.
The accompanying scope note documents the more conservative formalized
exponent O_d(v(loglog v)^2/sqrt(log v)). Keep these quantitative levels
distinct. The release describes outside examination led by Impagliazzo,
Paturi, and Williams. The Set Splitting paper should import the result as an
explicit hypothesis/theorem interface, without suggesting it reproduces or
independently verifies that work.

```bibtex
@misc{OpenAI2026Counting,
  author = {{OpenAI}},
  title = {The Exponential Time Hypothesis is False},
  year = {2026},
  note = {Preprint, 17 October 2026; revised 25 October 2026},
  url = {https://github.com/openai/math/blob/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/build/main_full_version.tex}
}
@misc{OpenAI2026Scope,
  author = {{OpenAI}},
  title = {The Exponential Time Hypothesis is False: Lean formalization scope},
  year = {2026},
  note = {Accessed 29 October 2026},
  url = {https://github.com/openai/math/blob/main/lean/docs/378.md}
}
```

The new manuscript itself already observes subexponential algorithms for
splitting **all** sets when their maximum cardinality is any fixed constant.
That elementary bounded-rank consequence must not be claimed here as new.

## Important prior art: the polynomial and recurrence

Jacob A. White. **On Multivariate Chromatic Polynomials of Hypergraphs and
Hyperedge Elimination.** *Electronic Journal of Combinatorics*
**18**(1), article **P160**, 2011. DOI: **10.37236/647**.

Primary journal PDF:
<https://www.combinatorics.org/ojs/index.php/eljc/article/download/v18i1p160/pdf/>

Section 6 defines a multivariate chromatic/coboundary polynomial. Set both
color parameters to 2 and all edge variables to t, obtaining
Q_H(t)=sum_colorings t^{number of monochromatic edges}. For a hypergraph
with m nonempty edges, our split-count polynomial is

    P_H(z)=z^m Q_H(1/z).

White's Theorem 9 specializes to

    Q_H(t)=Q_(H-e)(t)+(t-1)Q_(H/e)(t).

The displayed substitution gives exactly

    P_H(z)=z P_(H-e)(z)+(1-z)P_(H/e)(z).

White permits indexed parallel edges and uses the same vertex-identification
contraction. Thus neither this polynomial nor its recurrence should be
advertised as novel. Empty edges can be removed before applying the relation.

```bibtex
@article{White2011,
  author = {Jacob A. White},
  title = {On Multivariate Chromatic Polynomials of Hypergraphs and Hyperedge Elimination},
  journal = {Electronic Journal of Combinatorics},
  volume = {18},
  number = {1},
  pages = {P160},
  year = {2011},
  doi = {10.37236/647}
}
```

## General theorem supported by the reduction

The proof need not begin with a kernel. On any explicitly represented
hypergraph with n vertices and m indexed edges, set s=n+m. For cutoff r,
large-edge deletion/contraction gives at most

    sum_{j<=floor((n-1)/(r-1))} binom(m,j)

leaves, with the usual truncation at m. A uniform coarse bound is
2^{O(s log r/r)}. At each leaf the complete split-count distribution has a
parsimonious width-three encoding with O(rs) variables and fixed clause
density. Consequently the same quantitative rates proved for k in the
kernelized decision problem hold for exact profiles with k replaced by s.
This supplies an actual counting theorem without assuming a counting kernel.
In particular, when m=O(n), the full profile is computable in 2^{o(n)} time
and polynomial space under the imported counting theorem.

The bounds apply to indexed hyperedges, including parallel edges. Removing
isolated vertices requires a factor of two per removed vertex. The kernel
corollary is for decision; it does not turn the original-instance profile
into a function of target k alone.

## Suggested novelty statement

The contribution is a quantitative transfer from sparse width-three exact
counting to **unbounded-rank** hypergraph split profiles, and its combination
with a decision kernel to obtain parameter-subexponential Set Splitting.
The ingredients—coboundary polynomial, deletion/contraction, parsimonious
circuit encodings, and the kernel—are established or imported. A search has
not located this precise transfer, but that is insufficient to establish
priority. Describe the manuscript as a research draft pending independent
review and a fuller literature audit.
