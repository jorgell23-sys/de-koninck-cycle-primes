# OEIS A354427 has no other terms below 10^11

<!-- explicacion -->
**New to this? It is explained from scratch, assuming nothing:**
[English](https://jorgell23-sys.github.io/de-koninck-cycle-primes/) · [Español](https://jorgell23-sys.github.io/de-koninck-cycle-primes/es/)

<!-- hallazgo:que -->
## What was found

The primes p ≤ 10^11 with primes q, r such that q | p+1, r | q²+q+1 and
p | r²+r+1 (OEIS A354427) are exactly 3, 13, 19, 631, 1794067711 and
10855016833. The last two were known to be terms; that nothing lies between
them and below 10^11 was not.

<!-- hallazgo:enunciado -->
## The statement

For every prime p ≤ 10^11: p is in A354427 **if and only if**
p ∈ {3, 13, 19, 631, 1794067711, 10855016833}. Hence a(5) = 1794067711,
a(6) = 10855016833, and a(7) > 10^11 if it exists. The previous bound was 2^24.

<!-- hallazgo:ejemplo -->
## The smallest case, done by hand

    631 + 1        = 632  = 2³ · 79
    79² + 79 + 1   = 6321 = 3 · 7² · 43
    43² + 43 + 1   = 1893 = 3 · 631        → back to 631

and for a(5): 1794067711 + 1 = 2⁸·23·31·9829, 9829² + 9829 + 1 = 3·439·73363,
73363² + 73363 + 1 = 3·1794067711.

<!-- hallazgo:prueba -->
## Why it is proved

All 4,118,054,813 primes below 10^11 were examined. A lemma (RESULT.md §2)
makes each one cheap: for a witness r > p, the cofactor (q²+q+1)/r is smaller
than p and congruent to (q²+q+1)·ρ² mod p, with ρ a cube root of unity mod p,
so one division replaces factoring q²+q+1; a witness r < p is ρ itself. Two
algorithms that share nothing with the lemma give the same witnesses on the
ranges they cover, and every witness is confirmed with exact integers.

<!-- hallazgo:comprobar -->
## Check it yourself

```
python verify.py
```

prints `PASS` for each of its <!-- checks -->46<!-- /checks --> checks and
`N passed, 0 failed`; no dependencies. `python verify.py --deep` also re-runs
random segments of the search, and `python src/search.py 100000000000` re-runs
all of it.

<!-- hallazgo:nodice -->
## What it does not say

Nothing above 10^11, and nothing on whether the sequence is finite. It does not
discover a(5) and a(6) (Yamada did, in the OEIS comment): it shows there is
nothing before them. Two independent algorithms cover p ≤ 8589934589; above,
one algorithm, proved and sampled. It does not touch A355298.

---

## Files

| | |
|---|---|
| [RESULT.md](RESULT.md) | the statement, the lemma with its proof, the search, the cross-checks, the limits |
| [PRIOR_ART.md](PRIOR_ART.md) | what was searched, where, and the positive control |
| `verify.py` | every claim, checked; standard library only |
| `src/cycle_primes.py` | the definition and the lemma, in plain Python |
| `src/search.py` | the full search (numba optional) |
| `data/terms.json`, `data/blocks/` | the witnesses and the search log, one file per 10^9 |
| `docs/` | the explanation for non-specialists, in English and Spanish |

## Author

**Jorge Ellena Godoy**

## How this was produced

System design and research direction are the author's. The mathematical
results were produced by an automated system (Claude, Anthropic) under that
direction. All computations were verified by two independent implementations
and cross-checked against published work. The author is responsible for the
correctness of everything published here.
