# Set Splitting

[Read the paper](subexponential-set-splitting.pdf) · [LaTeX source](paper/main.tex)

Author: GPT-6 (OpenAI Codex). Research draft, 29 October 2026.

The paper reduces Set Splitting to exact SAT counting using O(n+m) variables,
where n is the number of elements and m the number of sets.
It counts colorings by how many sets they split.

Assuming the revised October 2026 SAT counting theorem, the running time is

```text
|I|^O(1) + 2^O(k loglog(k) / sqrt(log(k)))
```

Here k is the number of sets to split. Space is polynomial.
The paper also states the weaker rate documented by the theorem's
formalization scope note. The external SAT theorem is not proved here.

Run the checks:

```sh
python3 research/verify_paper.py
```

Python 3.10 or later is sufficient. Results are in
[paper/verification.json](paper/verification.json).
The code checks the reduction by exhaustive counting; it does not implement
the fast SAT algorithm.

[Research notes](research/sat_rate_audit.md) give supporting details.
Earlier branching and tensor notes are separate, unreviewed work.
