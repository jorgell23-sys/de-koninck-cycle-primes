# OEIS A354427 has no other terms below 10^11

<!-- explicacion -->
**New to this? It is explained from scratch, assuming nothing:**
[English](https://jorgell23-sys.github.io/de-koninck-cycle-primes/) · [Español](https://jorgell23-sys.github.io/de-koninck-cycle-primes/es/)

<!-- hallazgo:que -->
## What was found

The primes p ≤ 10^11 of OEIS A354427 — primes p with primes q, r such that
q | p+1, r | q²+q+1 and p | r²+r+1 — are exactly **3, 13, 19, 631,
1794067711, 10855016833**. So a(5) = 1794067711, a(6) = 10855016833, and
there is no a(7) below 10^11.

<!-- hallazgo:enunciado -->
## The statement

**Theorem.** Let p ≤ 10^11 be prime. There exist primes q, r with

    q | p + 1,     r | q² + q + 1,     p | r² + r + 1

if and only if p ∈ {3, 13, 19, 631, 1794067711, 10855016833}. Each has exactly
one witness (q, r):

| p | q | r |
|---:|---:|---:|
| 3 | 2 | 7 |
| 13 | 7 | 3 |
| 19 | 2 | 7 |
| 631 | 79 | 43 |
| 1794067711 | 9829 | 73363 |
| 10855016833 | 5569 | 1477111 |

<!-- hallazgo:ejemplo -->
## The smallest case, done by hand

For p = 631: 631 + 1 = 632 = 2³ · **79**; 79² + 79 + 1 = 6321 = 3 · 7² · **43**;
43² + 43 + 1 = 1893 = 3 · **631**. For a(5) = 1794067711:
1794067711 + 1 = 2⁸ · 23 · 31 · **9829**; 9829² + 9829 + 1 = 96619071 =
3 · 439 · **73363**; 73363² + 73363 + 1 = 5382203133 = 3 · **1794067711**.

<!-- hallazgo:prueba -->
## Why it is proved

Every prime p ≤ 10^11 was examined; the search is exhaustive, not sampled. It
is fast because of a lemma (section 2): for p ≡ 1 (mod 3) and a root ρ of
x² + x + 1 mod p, a witness r > p forces the cofactor m = (q²+q+1)/r to be the
residue (q²+q+1)·ρ² mod p, because m < p; a witness r < p is ρ itself. So each
pair (p, q) is decided by one division, without factoring q² + q + 1. Two
further algorithms that share nothing with this one — the literal definition,
and a polynomial sieve that factors q² + q + 1 completely — give the same
witnesses, one by one, on the ranges they cover (section 4).

<!-- hallazgo:comprobar -->
## Check it yourself

```
python verify.py          # standard library only, about a minute
python verify.py --deep   # also re-runs random segments of the search
python src/search.py 100000000000   # the whole search (numba: ~70 min on 7 cores)
```

`verify.py` confirms every witness with exact integers, tests the lemma against
the definition on every prime up to 10^5 and on random primes up to 10^11, and
checks that the search log tiles [0, 10^11] with no gap. It prints `PASS` per
check and exits 1 if any fails.

<!-- hallazgo:nodice -->
## What it does not say

It does not say whether A354427 is finite. It says nothing above 10^11. It does
not discover a(5) and a(6) — Yamada found them and gave their witnesses in the
OEIS comment; what is new is that **nothing lies between them**, so they can be
indexed. The range covered by two independent algorithms is [0, 8589934589];
above that the result rests on one algorithm, proved correct in section 2 and
cross-checked by sampling. It does not touch A355298 (the four-step analogue).

---

## 1. The objects

A354427 was defined by Tomohiro Yamada (OEIS, 2022-05-27) from his work on
De Koninck's equation σ(n) = rad(n)²: if a solution n has exactly one odd prime
p dividing n exactly once, then p is in A354427 or in A355298 (Yamada, *On a
problem of De Koninck*, Moscow J. Comb. Number Theory 10 (2021) 249–260). The
entry reads *"There are no other terms below 2^24"* and adds *"1794067711 and
10855016833 are also terms"*, which were never put in the data because the gap
between 2^24 and them had not been searched.

Equivalently, a term is a vertex of a directed 3-cycle p → q → r → p on the
primes, with an arrow x → y when y divides σ(x^e): σ(p) = p + 1 for the first
arrow and σ(x²) = x² + x + 1 for the other two. The sister sequences A354426
and A354428 list the vertices q and r of the same cycles.

## 2. The lemma that makes the search cheap

**Lemma.** Let p > 3 be prime. Primes q, r with q | p+1, r | q²+q+1 and
p | r²+r+1 exist if and only if p ≡ 1 (mod 3) and, for some prime q | p+1 and
some root ρ of x²+x+1 mod p (ρ' = p − 1 − ρ the other root), with
N = q²+q+1, either

- **(A)** ρ is prime and ρ | N (then r = ρ), or
- **(B)** m := N·ρ' mod p satisfies m ≥ 1, m | N, and N/m is prime (then r = N/m > p).

*Proof.* If p | r²+r+1 then r³ ≡ 1 and r ≢ 1 (mod p) (else p | 3), so r has
order 3 and 3 | p − 1. For p ≡ 1 (mod 3) the roots of x²+x+1 are ρ and
ρ' = −1−ρ with ρρ' ≡ 1, so p | r²+r+1 iff r ≡ ρ or ρ' (mod p); treat r ≡ ρ.
Since p is odd, every prime q | p+1 satisfies q ≤ (p+1)/2, hence
N ≤ (p² + 4p + 7)/4. If r < p then r = ρ (as integers in [0, p)): case (A).
If r > p, put m = N/r; then 1 ≤ m < N/p ≤ p/4 + 1 + 7/(4p) < p, and
m·r = N with r ≡ ρ gives m ≡ N·ρ⁻¹ = N·ρ' (mod p); as 0 < m < p, m is that
residue: case (B). (r = p is impossible, since p ∤ p²+p+1.) Conversely, in
(B), r = N/m ≡ N·m⁻¹ ≡ ρ (mod p), so p | r²+r+1. ∎

For p = 3: q | 4 forces q = 2, N = 7, r = 7, and 3 | 57. For p ≡ 2 (mod 3)
there is no r at all.

## 3. The search

`src/search.py` walks every prime p ≤ 10^11 in segments of 2^24: a segmented
sieve finds the primes, a second sieve factors p + 1 (every prime q | p+1 is a
base prime ≤ √(10^11+1) or the prime cofactor left over), a cube root of unity
mod p gives ρ, and the lemma proposes at most four candidates per pair (p, q).
Each candidate is then confirmed with exact integers and a deterministic
primality test. Modular products use a float64 quotient estimate, exact for
moduli below 2^40; this was checked against exact integers in 200,039 cases,
including the edges of 2^40.

π(10^11) = 4,118,054,813 primes were examined. The search log is
`data/blocks/` (one file per 10^9, with the witnesses found in it and the
time it took); `data/terms.json` collects them.

## 4. The cross-checks

| range | algorithms that cover it | agreement |
|---|---|---|
| p ≤ 2^24 = 16,777,216 | **literal** definition (factor p+1 and q²+q+1 with a general-purpose factorizer), **sieve** (below), **lemma** | identical witnesses: (3,2,7), (13,7,3), (19,2,7), (631,79,43) — Yamada's data |
| p ≤ 8,589,934,589 | **sieve**: factors q²+q+1 completely by a polynomial sieve over q ≤ 2^32, then walks every p ≡ −1 (mod q) and tests p \| r²+r+1 directly; **lemma** | identical witnesses: the four above and (1794067711, 9829, 73363) — nothing in one that is not in the other |
| p ≤ 10^11 | **lemma**, run twice from two separate code copies (the one published here in `src/search.py`, and the one it was developed in) | identical, block by block: 101 blocks of 10^9, the same six witnesses, no block differs. Two copies of one algorithm guard against copying errors, not against a wrong method — that is what the lemma's proof and the two rows above are for |
| all 9,592 primes ≤ 10^5, and 2,000 random primes p ≡ 1 (mod 3) in [10^9, 10^11] | **lemma** against the **literal** definition, prime by prime (`verify.py`, plain Python) | identical |

The sieve does not use the lemma: it never computes a cube root of unity and
never forces a cofactor. The literal algorithm uses neither.

**Positive controls.** The search returns Yamada's four data terms and nothing
else below 2^24, his published bound; and it returns both comment terms with
exactly the witnesses he gave, (9829, 73363) and (5569, 1477111). Those two are
precisely the case r > p of the lemma, the one a faulty reduction would lose.

## 5. What this does not claim

- Nothing above 10^11, and nothing about finiteness. A heuristic count
  (each pair (p, q) closes with probability about 2/p) suggests the number of
  terms up to x grows like log log x, which would make a(7) very large; that is
  a heuristic and is not claimed.
- Not the discovery of 1794067711 and 10855016833 as terms: that is Yamada's.
- Nothing about A355298, A354426, A354428 or A347988. The lemma does not apply
  to A355298: there the last factor lives in a number of size p⁴ and its
  cofactor is not forced below p.
- Not a solution of De Koninck's problem.

## 6. Prior art

See [PRIOR_ART.md](PRIOR_ART.md): OEIS (including the revision history, with no
pending proposal), six literature sources with a positive control that finds
Yamada's paper, the full text of the paper, GitHub code search, and a
316,098-document corpus.

## Author

**Jorge Ellena Godoy** — responsible for the correctness of everything
published here.

## How this was produced

System design and research direction are the author's. The
mathematical results were produced by an automated system (Claude, Anthropic)
under that direction. All computations were verified by two independent
implementations and cross-checked against published work. The author is
responsible for the correctness of everything published here.

---

## Citing

Cite the **concept DOI**:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22708291.svg)](https://doi.org/10.5281/zenodo.22708291)

    10.5281/zenodo.22708291
