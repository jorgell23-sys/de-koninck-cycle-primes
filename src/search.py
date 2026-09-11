#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The full search: every prime p <= X of A354427, block by block.

    python src/search.py 100000000000            # writes data/blocks/*.json
    python src/search.py 100000000000 --check    # re-run only the blocks that
                                                 # disagree with data/blocks

Uses numba when it is installed (about 40 s per 10^9 on 7 cores); without it,
the same algorithm runs in pure Python and is correct but very slow. Each
block is written as soon as it finishes, so an interrupted run resumes.

The kernel is the reduction of RESULT.md, section 2: for each prime
p = 1 (mod 3) and each prime q | p+1, a witness r is either the cube root of
unity rho itself (r < p) or N / m with the cofactor m = N * rho' mod p forced
below p (r > p). The kernel only PROPOSES candidates; every one is confirmed
with exact integers by `cycle_primes.confirm`.
"""
import argparse
import json
import os
import sys
import time
from math import isqrt
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cycle_primes as CP  # noqa: E402

try:
    import numpy as np
    from numba import njit
    HAVE_NUMBA = True
except ImportError:          # the pure-Python path below is used instead
    HAVE_NUMBA = False

MAX_MODULUS = 1 << 40        # _mulmod is exact below this (float64 quotient)

if HAVE_NUMBA:
    _U1, _U2, _U3 = np.uint64(1), np.uint64(2), np.uint64(3)
    _SIGN = np.uint64(1) << np.uint64(63)

    @njit(cache=True)
    def _mulmod(a, b, m):
        q = np.uint64(np.float64(a) * np.float64(b) / np.float64(m))
        r = a * b - q * m
        if r >= _SIGN:
            r += m
        elif r >= m:
            r -= m
        return r

    @njit(cache=True)
    def _powmod(a, e, m):
        r = _U1 % m
        a = a % m
        while e > 0:
            if e & _U1:
                r = _mulmod(r, a, m)
            a = _mulmod(a, a, m)
            e >>= _U1
        return r

    @njit(cache=True)
    def _cube_root(p):
        e = (p - _U1) // _U3
        a = _U2
        while True:
            x = _powmod(a, e, p)
            if x != _U1:
                return x
            a += _U1

    @njit(cache=True)
    def _divides_poly(q, d):
        qm = q % d
        return (_mulmod(qm, qm, d) + qm + _U1) % d == 0

    @njit(cache=True)
    def _pair(p, q, rho, out, n):
        rho2 = p - _U1 - rho
        qp = q % p
        nmod = (_mulmod(qp, qp, p) + qp + _U1) % p
        for k in range(2):
            root = rho if k == 0 else rho2
            inv = rho2 if k == 0 else rho
            if root > _U1 and _divides_poly(q, root):
                if n < out.shape[0]:
                    out[n, 0], out[n, 1], out[n, 2], out[n, 3] = p, q, root, 0
                n += 1
            m0 = _mulmod(nmod, inv, p)
            if m0 >= _U1 and _divides_poly(q, m0):
                if n < out.shape[0]:
                    out[n, 0], out[n, 1], out[n, 2], out[n, 3] = p, q, m0, 1
                n += 1
        return n

    @njit(cache=True)
    def _segment(lo, hi, base, out):
        S = hi - lo
        isp = np.ones(S, dtype=np.bool_)
        for j in range(S):
            if lo + j < 2:
                isp[j] = False
        for i in range(base.shape[0]):
            b = np.int64(base[i])
            if b * b >= hi:
                break
            for x in range(max(b * b, ((lo + b - 1) // b) * b), hi, b):
                isp[x - lo] = False
        rho = np.zeros(S, dtype=np.uint64)
        for j in range(S):
            if isp[j] and (lo + j) % 3 == 1:
                rho[j] = _cube_root(np.uint64(lo + j))
        rem = np.empty(S, dtype=np.uint64)
        for j in range(S):
            rem[j] = np.uint64(lo + j + 1)
        n = 0
        for i in range(base.shape[0]):
            b = np.int64(base[i])
            if b * b > hi + 1:
                break
            ub = np.uint64(b)
            for mm in range(((lo + 1 + b - 1) // b) * b, hi + 1, b):
                j = mm - 1 - lo
                while rem[j] % ub == 0:
                    rem[j] //= ub
                if rho[j] != 0:
                    n = _pair(np.uint64(lo + j), ub, rho[j], out, n)
        for j in range(S):
            if rho[j] != 0 and rem[j] > _U1:
                n = _pair(np.uint64(lo + j), rem[j], rho[j], out, n)
        return n


def _confirm_row(p, q, x, kind):
    N = q * q + q + 1
    if kind == 1:
        if x < 1 or N % x:
            return None
        r = N // x
    else:
        r = x
    return (p, q, r) if CP.confirm(p, q, r) else None


def segment(item):
    """Witnesses (p, q, r) with p in [lo, hi)."""
    lo, hi = item
    if hi > MAX_MODULUS:
        raise ValueError("search.py: p must stay below 2^40")
    found = set()
    if lo <= 3 < hi:
        found.add((3, 2, 7))
    if not HAVE_NUMBA:
        for p in CP.primes_between(max(lo, 5), hi):
            found.update(CP.reduction(p))
        return sorted(found)
    base = np.array(CP.primes_between(2, isqrt(hi + 1) + 3), dtype=np.uint64)
    cap = 1 << 16
    out = np.zeros((cap, 4), dtype=np.uint64)
    n = _segment(int(max(lo, 4)), int(hi), base, out)
    if n > cap:
        raise RuntimeError("more candidates than reserved in [%d,%d)" % (lo, hi))
    for p, q, x, kind in out[:n].tolist():
        t = _confirm_row(int(p), int(q), int(x), int(kind))
        if t:
            found.add(t)
    return sorted(found)


def collect(X, blocks_dir, out_path):
    """Build data/terms.json from the block files, refusing gaps or overlaps."""
    rows = []
    for name in sorted(os.listdir(blocks_dir)):
        if name.startswith("block_") and name.endswith(".json"):
            with open(os.path.join(blocks_dir, name)) as fh:
                rows.append(json.load(fh))
    rows.sort(key=lambda r: r["lo"])
    end = 0
    for r in rows:
        if r["lo"] != end:
            raise SystemExit("gap or overlap at %d (next block starts at %d)" % (end, r["lo"]))
        end = r["hi"]
    if end != X + 1:
        raise SystemExit("the blocks reach %d, not %d" % (end - 1, X))
    wit = sorted({tuple(w) for r in rows for w in r["witnesses"]})
    with open(out_path, "w") as fh:
        json.dump({"X": X, "terms": sorted({w[0] for w in wit}),
                   "witnesses": [list(w) for w in wit]}, fh, indent=1)
    print("wrote %s: %d witnesses, terms %s" % (out_path, len(wit), sorted({w[0] for w in wit})))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("X", type=int)
    ap.add_argument("--collect", action="store_true",
                    help="only build data/terms.json from data/blocks")
    ap.add_argument("--block", type=int, default=10 ** 9)
    ap.add_argument("--segment", type=int, default=1 << 24)
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument("--out", default=os.path.join(HERE, "..", "data", "blocks"))
    a = ap.parse_args()
    if a.collect:
        collect(a.X, a.out, os.path.join(HERE, "..", "data", "terms.json"))
        return
    os.makedirs(a.out, exist_ok=True)
    print("numba: %s" % ("yes" if HAVE_NUMBA else "NO -- pure Python, very slow"))
    with Pool(a.workers) as pool:
        for lo in range(0, a.X + 1, a.block):
            hi = min(lo + a.block, a.X + 1)
            path = os.path.join(a.out, "block_%015d_%015d.json" % (lo, hi))
            if os.path.exists(path):
                continue
            t0 = time.time()
            segs = [(s, min(s + a.segment, hi)) for s in range(lo, hi, a.segment)]
            found = sorted({t for r in pool.map(segment, segs) for t in r})
            with open(path, "w") as fh:
                json.dump({"lo": lo, "hi": hi, "witnesses": found,
                           "seconds": round(time.time() - t0, 1)}, fh)
            print("[%d, %d)  %.0f s  %s" % (lo, hi, time.time() - t0, found), flush=True)


if __name__ == "__main__":
    main()
