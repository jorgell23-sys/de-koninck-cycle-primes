# Prior art: what was searched, where, and when

**Not finding something is not the same as it being new.** This file records
every search made before claiming that the terms of A354427 beyond 2^24 had not
been determined, so that anyone can repeat them and so that the claim can be
withdrawn the day one of them returns something.

All searches: 2026-09-11.

## 1. What is already known, and is not claimed here

| what | where | status |
|---|---|---|
| The sequence and its first four terms 3, 13, 19, 631 | OEIS A354427 (T. Yamada, 2022-05-27) | known |
| "There are no other terms below 2^24" | A354427, comment | known |
| 1794067711 and 10855016833 are terms, with witnesses q = 9829 and q = 5569 | A354427, comment (Yamada, 2022-06-05) | known — **that they are terms is not claimed here** |
| The origin: if σ(n) = rad(n)² and n has a single odd prime to the first power, that prime is in A354427 or A355298 | T. Yamada, *On a problem of De Koninck*, Moscow J. Comb. Number Theory 10:3 (2021) 249–260; correction 10:4 (2021) 339; arXiv:1906.10001 | known |
| The sister sequences A354426 (vertex q) and A354428 (vertex r) | OEIS; A354426 extended to 10^8 by Lucas A. Brown (2024) | known, not touched |

**What is claimed here is the absence of other terms**: that 1794067711 and
10855016833 are the fifth and sixth terms, and that there is no seventh up to
the bound of the search. That is what OEIS left open.

## 2. OEIS itself

| query | result |
|---|---|
| `id:A354427`, `id:A354426`, `id:A354428`, `id:A347988`, `id:A355298` | the entries; A354427 data is still `3, 13, 19, 631` |
| revision history of A354427 (`oeis.org/history?seq=A354427`) | last change #14, approved 2022-06-05; **no pending proposal or draft** |
| revision history of A354428, A354426 | last changes approved 2022-06-02 and 2024-08-11; no pending proposal |
| `"De Koninck" rad`, `Yamada "De Koninck"`, `"rad(n)^2" sigma` | no entry that extends A354427 |

## 3. The literature — with a positive control in the same batch

Six sources: zbMATH Open, OpenAlex, Crossref, arXiv, Zenodo, DataCite. A work
counts only if **all** the required terms appear together in its title or
abstract.

| search | required terms | result |
|---|---|---|
| **positive control**: "On a problem of De Koninck" | `problem of De Koninck` | **found**: the article (OpenAlex), its correction, and the preprint arXiv:1906.10001 (DataCite) |
| sum of divisors equals square of radical | `sum of divisors`, `radical` | nothing |
| sigma(n) = rad(n)^2 De Koninck conjecture | `De Koninck`, `conjecture` | nothing |
| the prime triple p, q, r | `q^2+q+1`, `p+1` | nothing |
| cycles of primes, sum of divisors of prime squares | `prime squares`, `cycle` | nothing |
| Yamada, De Koninck, computation | `Yamada`, `De Koninck` | nothing |

The positive control matters: it shows that the same machinery, in the same
run, finds the one paper that is known to exist. A search that cannot find the
paper it builds on proves nothing by staying silent.

**Citations of Yamada's paper** (OpenAlex, works citing
`10.2140/moscow.2021.10.249` and its correction): **zero**.

**The paper itself** (arXiv:1906.10001, v3, 15 pages, full text): no
occurrence of 1794067711, 10855016833, 5569, 9829, 73363, "comput", "search",
"PARI" or "Table". The paper does not tabulate these primes; the 2^24 bound
lives only in the OEIS entries.

## 4. Code and data

| where | query | result |
|---|---|---|
| GitHub code search | `1794067711`, `10855016833` | only unrelated data files (prime lists, measurements) |
| GitHub code search | `A354427` | `gfis/OEIS-prog`: a copy of the OEIS PARI program (`bfimax=4`), no extension |
| GitHub | `lucasaugustus/oeis` (120 files) | only `A354426.py`, for the sister sequence |
| GitHub repositories | `De Koninck`, `A354427` | nothing related |

## 5. A full-text corpus of 316,098 harvested documents

Searched lexically, in English: `De Koninck sigma rad squared equation`,
`sum of divisors equal to square of radical`, `Yamada De Koninck problem`,
`primes q divides p+1 r divides q^2+q+1 odd perfect number`, and the literal
phrases `De Koninck`, `A354427`, `rad(n)^2`. The corpus contains two other
papers by T. Yamada on odd perfect numbers (arXiv:2103.16936 and
arXiv:2312.17059) and ten passages by or about J.-M. De Koninck on other
topics; the phrase `A354427` returns nothing.

## 6. What this does not rule out

A computation done privately and never published, or published in a place none
of these sources indexes (a thesis in a local repository, a talk, a forum post).
If one exists, it takes priority, and this repository will say so.
