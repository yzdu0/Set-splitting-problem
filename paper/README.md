# Subexponential Set Splitting through Selector Moments and Exact #3SAT

Research draft, 29 October 2026. No human authorship or publication-priority
claim is assigned. The manuscript is AI-assisted and has not received
external peer review.

`main.tex` is a self-contained LaTeX article with an inline bibliography.
Open this folder in Codex for the editable source and live PDF preview.
The exported PDF is `../output/pdf/subexponential-set-splitting.pdf`.

The main reduction is unconditional: a hypergraph with n vertices, m indexed
edges, and J incidences yields m+1 exact #3SAT calls using O(n+m) variables
and O(J+m+1) clauses each. Binomial inversion recovers its complete split
profile. The subexponential runtime imports the October 2026 exact-counting
theorem through explicit interfaces. The revised manuscript's general rate
gives `poly(L) * 2^O(s loglog(s) / sqrt(log(s)))`, s=n+m; the formalization
scope note documents the more conservative squared-loglog rate. Their
fixed-density rate is used only under the paper's linear-incidence condition.

The established decision kernel gives the corresponding target-k decision
corollary. No counting-kernel or original-instance target-k search claim is
made. The original full-profile theorem supports optimal-coloring recovery
in the joint size n+m.

## Reproduce checks

From the repository or archive root:

```sh
python3 research/verify_paper.py
```

This requires Python 3.10 or later and no third-party packages. It invokes
`research/selector_moments.py`, imports utilities from `research.py`, and
refreshes `paper/verification.json`. The verifier uses exhaustive counting;
it is not the imported subexponential SAT implementation. The manifest
contains exact check counts, deterministic seeds, encoding sizes, and hashes.

## Compile

With Tectonic and its package cache available, from the archive root:

```sh
mkdir -p output/pdf
tectonic --outdir output/pdf paper/main.tex
```

This produces `output/pdf/main.pdf`. The delivered copy has the descriptive
name `subexponential-set-splitting.pdf`. A conventional LaTeX installation
can also compile `main.tex`; no external bibliography processor is required.

## Review priorities

Check the one-way selector guards, the unique extensions of circuit gates,
the distinction between general and fixed clause density, and the imported
counting statement's exact version. The paper supplies full proofs of the
reduction but does not independently validate the external SAT theorem or
establish priority for the application.
