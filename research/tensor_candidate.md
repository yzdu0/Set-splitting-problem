# Tensor terminal solver for the leaf-only modification

This note proves the terminal lemma used in the proposed O*(1.7116^k) algorithm. The complete proposal combines this lemma with branch_certificate.md; it is a research claim awaiting outside review and a fuller prior-art audit.

## Established baseline

Nederlof, van Rooij, and van Dijk, *Inclusion/Exclusion Meets Measure and Conquer*, Algorithmica 69 (2014), 685–740, Theorem 23, gives O*(1.7171^k) time and space. The polynomial-space bound is O*(1.8213^k). DOI: https://doi.org/10.1007/s00453-013-9759-2 . An author-uploaded manuscript is readable at https://www.researchgate.net/publication/287264463_InclusionExclusion_Meets_Measure_and_Conquer .

## Verified local identity

For a ternary uncoloured set, let f_t(x,y,z) equal 1 on 000 and 111 and t otherwise. For any rational q >= 2, put

    t = q / (q^2 - q + 1),
    c = 1 / ((q + 1)(q^2 - q + 1)).

Then

    f_t(x,y,z) = c sum_{s in {0,1}} product_{v in {x,y,z}} M(s,v),
    M(s,v) = q if s=v and 1 otherwise.

The monochromatic entries are c(q^3+1)=1; the other entries are c(q^2+q)=t. Thus this is a binary latent-spin representation on the same incidence star. The integer choices q=2,...,m+2 give m+1 distinct rational t values, sufficient to interpolate the degree-m split-count polynomial. Arithmetic bit lengths are polynomial.

A coloured set factor is t + (1-t) product_i 1[x_i=b], which also has rank at most two. Uncoloured degree-two factors are already binary pairwise interactions.

Consequently an actual maximum-degree-three incidence instance, without problematic compressed annotations, can be evaluated using binary pairwise partition-function dynamic programming in O*(2^tw), instead of the three-state O*(3^tw) terminal routine in the 2014 analysis.

## Generic Boolean ternary tensors

If leaf elimination creates arbitrary 2x2x2 tensors, the same conclusion is available with polynomial interpolation over finite fields. For every ternary tensor T, perturb T to T(e)=T+e R, with the two matrix slices of R equal to I and diag(1,2). Except at at most six field values e, its first slice is nonsingular and the matrix formed by the second slice times the inverse first slice has distinct eigenvalues. Diagonalising that matrix decomposes T(e) as a sum of two simple tensors. Over an odd finite field F_p, all these eigenvalues lie in the common extension F_(p^2).

For h ternary tensors, at most 6h evaluation points are bad. From 7h+1 distinct values, choose h+1 good values. The whole partition function is a polynomial of degree at most h in e, so interpolate its value at zero. Dynamic programming runs over binary latent spins on the same graph. CRT over polynomial-size primes reconstructs the integer split-count coefficients. This gives a potential O*(2^tw) evaluator for arbitrary cubic Boolean tensor networks with polynomial overhead.

## Verified obstruction to applying this directly to the published algorithm

The published algorithm annotates degree-two twins as well as leaves. A core degree-three set vertex can therefore have total arity greater than three, and the removed part need not preserve Boolean bond dimension two.

Take two sets

    A={a1,a2,u,v}, B={b1,b2,u,v}.

The elements u,v are degree-two twins. One can be annotated. After summing over u,v, group each external pair (a1,a2) and (b1,b2) into states 00, mixed, 11. The resulting boundary matrix is

    [[1+3t^2, t+3t^2, 2t+2t^2],
     [t+3t^2, 4t^2,   t+3t^2],
     [2t+2t^2,t+3t^2, 1+3t^2]].

Its determinant is 2t^2(t-1)^4. It has rank three for every t other than zero or one. A binary pairwise model on the retained one-twin core path A-u-B can transmit matrix rank at most two across that path. Therefore the direct replacement of the published annotated terminal solver by the above binary solver is invalid.

An equivalent latent-three-state explanation: one shared degree-two element yields the interaction

    K=[[2,1,1],[1,1,0],[1,0,1]],

of rank two, but l twins yield its entrywise l-th power, whose determinant is 2^l-2 and is nonzero for l>=2.

## Necessary change to the annotation rule

Omit degree-two-twin annotations and retain only degree-zero/one leaf annotations. Annotated components then form pendant trees and can be eliminated into local tensors without producing higher-dimensional bonds between core nodes. The lemma below applies to this modification. The separate branch_certificate.md audits the recurrence bounds and provides exact feasible weights for the modified algorithm; the old numerical exponent is not simply inherited.

## Terminal solver lemma for the leaf-only modification

**Lemma (derived here).** Let I be an incidence instance with n remaining Boolean elements and m remaining sets; each set can be uncoloured, previously red, or previously green. Delete vertices of degree zero or one repeatedly, recording their elimination order, and let C be the ordinary 2-core. If C has maximum degree at most three and a tree decomposition of C of width w is supplied, then the complete split-count polynomial can be computed deterministically in O*(2^w) time and space. The suppressed factor is polynomial in the original incidence-instance size. This statement does not use degree-two-twin annotations.

**Proof.** Introduce a Boolean port on each incidence edge. An element vertex carries the equality tensor on its ports, and a set vertex carries the tensor t^(split indicator), respecting a previously assigned colour if any. For an isolated element the scalar tensor is 2, accounting for its two colour choices. Empty sets are handled as scalar 1. Contracting this tensor network gives

    P(t) = sum_colourings t^(number of split sets).

Every connected component deleted while obtaining the 2-core is a tree attached to at most one core vertex, or is a whole tree component. A cycle, or a path joining two core attachments, would survive leaf deletion. Thus each deleted component sends a two-entry message along its sole edge to the core. These messages can be computed in polynomial time. Equality tensors and the set tensors permit this even if their original arities are large: the equality tensor is the sum of two simple tensors; an uncoloured nonempty set tensor is

    t * 1^tensor_d + (1-t) * (e0^tensor_d + e1^tensor_d),

and a previously colour-b set tensor is

    t * 1^tensor_d + (1-t) * eb^tensor_d.

Contracting incoming messages therefore takes a linear number of field operations per incident edge. The resulting core is a Boolean tensor network with arbitrary tensors of arity two or three; tree components contribute scalar factors. A whole degree-two core cycle can also be contracted directly in polynomial time, although the construction below handles it as well.

Fix an odd prime p greater than max(m,7h), where h is the number of degree-three core vertices. Work first at one value of t in F_p. A core ternary tensor T has matrix slices A=T[:,:,0] and B=T[:,:,1]. Let R have slices I and diag(1,2), and replace every ternary T by

    T(e) = T + e R.

Its first slice A(e) is singular at at most two values of e. Define

    D(e) = trace(B(e) adj(A(e)))^2 - 4 det(B(e)) det(A(e)).

This polynomial has degree at most four and leading coefficient 1: the leading matrices are I and diag(1,2), giving 3^2-4*2=1. Therefore D has at most four roots. If A(e) is nonsingular and D(e) is nonzero, B(e) A(e)^(-1) has two distinct eigenvalues in the common quadratic extension F_(p^2). Diagonalise it as

    B A^(-1) = U diag(lambda0,lambda1) U^(-1),
    V = U^(-1) A.

Then

    T(i,j,k) = sum_{s=0,1} U(i,s) V(s,j) L(s,k),
    L(s,0)=1, L(s,1)=lambda_s.

Thus T has a two-term simple-tensor decomposition over the same field F_(p^2) for every core vertex. A degree-two tensor A(i,j) always has the two-term decomposition sum_s A(i,s) delta(s,j).

At most 6h values of e are bad for at least one ternary tensor. Among 7h+1 distinct values in F_p there are at least h+1 good ones. For each good e, replace each core tensor by the above decomposition, with one hidden Boolean spin s per core vertex. Summing the port bit on an edge uv gives a binary interaction

    W_uv(s_u,s_v) = sum_{b=0,1} g_(u,uv)(s_u,b) g_(v,uv)(s_v,b).

The resulting object is an arbitrary binary pairwise partition function on exactly the graph C. Standard tree-decomposition dynamic programming evaluates it using O*(2^w) field operations and space. All tensors use the one field F_(p^2), so extension degrees do not multiply with the number of vertices.

The perturbed partition function is a polynomial of degree at most h in e. Interpolate it from the h+1 good evaluations and obtain its value at e=0. This is precisely P(t) modulo p. Repeating at m+1 distinct t values recovers every coefficient of P modulo p. Perform the same computation for polynomially many polynomial-size odd primes and use CRT until their product exceeds 2^n: every integer coefficient of P is between zero and 2^n. These primes can be found by sieving to a polynomial bound; a nonsquare defining F_(p^2), square roots, and eigenvectors can all be computed deterministically in polynomial time (even brute-force field search is polynomial because p is polynomially bounded). Polynomial interpolation and CRT have polynomial bit complexity. This proves the lemma.

### Relation to the structural width bound

Proposition 6 of the 2014 paper gives a polynomially constructible path decomposition of a subcubic graph C with width at most

    n3(C)/6 + epsilon*|V(C)| + O(1)

for each fixed positive epsilon, where n3 counts degree-three vertices. The epsilon term involves all core vertices, not only degree-three vertices. Because the measure assigns a strictly positive weight to every core vertex, |V(C)| is at most the measure divided by the smallest positive weight. A fixed sufficiently small epsilon can therefore be absorbed in any explicit slack in the final exponential base. The branching-certificate note must supply that slack before asserting a rounded numerical global bound.

### Verification and novelty status

The tensor identities and the leaf-only terminal lemma above have explicit algebraic proofs. Applying the lemma to a new global Set Splitting bound additionally requires the separate recurrence audit for omitting degree-two-twin annotations and an exact feasible measure certificate. The local ternary decomposition is a form of binary tensor factorisation / holographic transformation; its algebra should not be represented as established novel prior art without a fuller literature search. The proposed application to this branching algorithm is a research claim requiring independent review.
