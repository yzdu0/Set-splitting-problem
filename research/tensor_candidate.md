# Earlier tensor solver

This lemma supports the separate O*(1.7116^k) proposal in
[branch_certificate.md](branch_certificate.md). It is not used by the current
SAT-based paper. The proposal has not had external review.

## Terminal lemma

Peel degree-zero/one vertices from the incidence graph. If the remaining
2-core has maximum degree three and a width-w tree decomposition is supplied,
its full split-count polynomial can be computed in O*(2^w) time and space.

Represent each incidence by a Boolean port. Element tensors require equal
port values; set tensors contribute t when split and 1 otherwise.
An isolated element contributes 2; an empty set contributes 1.
Removed trees attach to at most one core vertex and send two-entry messages.
These messages are cheap even at large degrees: equality is a sum of two
product tensors, and the uncolored nonempty set factor is

```text
t * 1^tensor_d + (1-t) * (e0^tensor_d + e1^tensor_d).
```

For a set already containing color b, keep only the eb product term.
After tree elimination, each core tensor has two or three Boolean ports.

## Exact factorization

Fix a polynomial-size odd prime p>max(m,7h), where h counts ternary tensors.
For each ternary tensor with matrix slices A,B, perturb them to
A+epsilon I and B+epsilon diag(1,2).
The determinant of the first slice has degree two and leading coefficient 1.
The polynomial

```text
D = trace(B adj(A))^2 - 4 det(B) det(A)
```

has degree four and leading coefficient 1.
Thus at most six epsilon values per tensor are unusable.
For every other value, BA^(-1) has distinct eigenvalues in the common field
F_(p^2). Write BA^(-1)=U diag(lambda0,lambda1) U^(-1) and V=U^(-1)A.
Then

```text
T(i,j,k) = sum_s U(i,s) V(s,j) L(s,k),
L(s,0)=1, L(s,1)=lambda_s.
```

This expresses the tensor using one hidden Boolean variable.
Binary tensors have such a factorization directly.
Summing each shared port gives a pairwise interaction on the same core graph.
Its partition function costs O*(2^w).

Among 7h+1 epsilon values, at least h+1 work for every tensor.
The partition function has degree at most h in epsilon, so interpolate its
value at zero. Repeat at m+1 values of t to recover all coefficients modulo p.
Use polynomially many polynomial-size primes and CRT until their product
exceeds 2^n. Each coefficient is at most 2^n, so this recovers the exact
integers. Field arithmetic, interpolation, and CRT take polynomial overhead.

## Why twin annotations must be omitted

Let A={a1,a2,u,v} and B={b1,b2,u,v}. The elements u,v are degree-two twins.
After summing their colors, group each external pair into 00, mixed, and 11.
The boundary matrix is

```text
[[1+3t^2, t+3t^2, 2t+2t^2],
 [t+3t^2, 4t^2,   t+3t^2],
 [2t+2t^2,t+3t^2, 1+3t^2]].
```

Its determinant is 2t^2(t-1)^4, so its rank is three for t other than 0 or 1.
Keeping only one twin would leave a binary path that can transmit rank at
most two. Ordinary leaf peeling avoids this obstruction.

Run `python3 research/verify_tensors.py`.
The checks cover 990 decompositions, 65 complete network comparisons, and
13 interpolation recoveries. The factorization ideas have established
holographic precedents; novelty of this application is unresolved.
