# Paper

Author: GPT-6 (OpenAI Codex).

- [PDF](../subexponential-set-splitting.pdf)
- [Editable source](main.tex)
- [Check results](verification.json)

The running-time result assumes the external SAT counting theorem.
The paper proves the reduction and separates the two reported counting rates.

From the repository root:

```sh
python3 research/verify_paper.py
```

To rebuild the root PDF with Tectonic:

```sh
tectonic --outdir . paper/main.tex
mv main.pdf subexponential-set-splitting.pdf
```

The source includes its bibliography. No bibliography processor is needed.
