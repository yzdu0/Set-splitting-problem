# Sources

- Lokshtanov and Saurabh, *Even Faster Algorithm for Set Splitting!* (2009),
  [DOI](https://doi.org/10.1007/978-3-642-11269-0_24).
  Theorem 1 gives a decision kernel with at most k vertices and 2k edges.
  It is not a counting kernel.
- Nederlof, van Rooij, and van Dijk, *Inclusion/Exclusion Meets Measure and
  Conquer* (2014), [DOI](https://doi.org/10.1007/s00453-013-9759-2).
  Published bounds: O*(1.7171^k) with exponential space and O*(1.8213^k)
  with polynomial space.
- OpenAI, *The Exponential Time Hypothesis is False*, revised 25 October 2026,
  [manuscript](https://github.com/openai/math/blob/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/build/main_full_version.tex).
  Its main theorem states exponent O(v loglog(v)/sqrt(log(v))) for general
  fixed-width formulas, and O(v/sqrt(log(v))) at fixed clause density.
- The accompanying [formalization scope note](https://github.com/openai/math/blob/main/lean/docs/378.md)
  documents the weaker exponent O(v(loglog(v))^2/sqrt(log(v))).
  The paper distinguishes these rates and assumes the external result.
- White, *On Multivariate Chromatic Polynomials of Hypergraphs and Hyperedge
  Elimination* (2011), [DOI](https://doi.org/10.37236/647).
  Section 6 and Theorem 9 cover the polynomial and its deletion-contraction
  relation. The selector moments are its binomial transform.

Sources checked 29 October 2026. The application may be new; this search does
not establish priority. Full references are in [the paper](../paper/main.tex).
