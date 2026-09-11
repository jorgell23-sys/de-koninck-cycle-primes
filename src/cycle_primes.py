#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reference implementation, standard library only.

A prime p belongs to OEIS A354427 when there are primes q, r with

    q | p + 1,     r | q^2 + q + 1,     p | r^2 + r + 1.

This module gives two independent ways of deciding that for a single p:

* `literal(p)`   -- the definition: factor p+1, factor q^2+q+1, test p | r^2+r+1.
* `reduction(p)` -- the reduction proved in RESULT.md, which never factors
                    q^2+q+1: the cofactor of a large r is forced below p.

and `confirm(p, q, r)`, which checks a witness with exact integers. Everything
here is slow and simple on purpose; `search.py` is the fast one.
"""
from math import gcd, isqrt
import random

_SMALL = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]


def is_prime(n):
    """Deterministic Miller-Rabin; the 12 bases are exact for n < 3.3e24."""
    if n < 2:
        return False
    for p in _SMALL:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in _SMALL:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    if n >= 3317044064679887385961981:
        raise ValueError("is_prime: the 12 bases are only proven below 3.3e24")
    return True


def _pollard_brent(n):
    if n % 2 == 0:
        return 2
    rng = random.Random(n)
    while True:
        y, c, m = rng.randrange(1, n), rng.randrange(1, n), 128
        g = r = q = 1
        while g == 1:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n
                g = gcd(q, n)
                k += m
            r *= 2
        if g == n:
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = gcd(abs(x - ys), n)
        if g != n:
            return g


def prime_factors(n):
    """The distinct prime factors of n >= 1, sorted."""
    out = set()
    for p in range(2, 1000):
        if n % p == 0:
            out.add(p)
            while n % p == 0:
                n //= p
    stack = [n] if n > 1 else []
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        if is_prime(m):
            out.add(m)
            continue
        d = _pollard_brent(m)
        stack += [d, m // d]
    return sorted(out)


def confirm(p, q, r):
    """True iff (p, q, r) is a witness for A354427, checked with exact integers."""
    return (is_prime(p) and is_prime(q) and is_prime(r)
            and (p + 1) % q == 0
            and (q * q + q + 1) % r == 0
            and (r * r + r + 1) % p == 0)


def literal(p):
    """All witnesses (p, q, r) of a prime p, straight from the definition."""
    found = []
    for q in prime_factors(p + 1):
        for r in prime_factors(q * q + q + 1):
            if (r * r + r + 1) % p == 0:
                found.append((p, q, r))
    return sorted(found)


def cube_root_of_unity(p):
    """A root of x^2 + x + 1 modulo a prime p = 1 (mod 3)."""
    e, a = (p - 1) // 3, 2
    while True:
        w = pow(a, e, p)
        if w != 1:
            return w
        a += 1


def reduction(p):
    """All witnesses of a prime p, WITHOUT factoring q^2 + q + 1.

    p = 3 is done by hand (q | 4 forces q = 2). For p = 2 (mod 3) there are
    none, because x^2 + x + 1 has no root mod p. For p = 1 (mod 3), with rho
    and rho' = p - 1 - rho the two roots and N = q^2 + q + 1:

      r < p  ->  r is the root itself;
      r > p  ->  the cofactor m = N / r is < p and m = N * rho' (mod p),
                 so m is forced and one division decides.
    """
    if p == 3:
        return [(3, 2, 7)]
    if p % 3 != 1:
        return []
    rho = cube_root_of_unity(p)
    found = set()
    for q in prime_factors(p + 1):
        N = q * q + q + 1
        for root, inv in ((rho, p - 1 - rho), (p - 1 - rho, rho)):
            if root > 1 and N % root == 0 and is_prime(root):
                found.add((p, q, root))
            m = (N % p) * inv % p
            if m >= 1 and N % m == 0 and is_prime(N // m):
                found.add((p, q, N // m))
    return sorted(t for t in found if confirm(*t))


def primes_between(lo, hi):
    """Primes in [lo, hi) by a segmented sieve (pure Python)."""
    if hi <= 2:
        return []
    lo = max(lo, 2)
    base = [i for i in range(2, isqrt(hi) + 1)
            if all(i % d for d in range(2, isqrt(i) + 1))]
    mark = bytearray([1]) * (hi - lo)
    for b in base:
        start = max(b * b, (lo + b - 1) // b * b)
        mark[start - lo::b] = bytearray(len(range(start, hi, b)))
    return [lo + i for i, v in enumerate(mark) if v]
