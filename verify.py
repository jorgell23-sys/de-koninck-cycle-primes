#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every claim in RESULT.md, checked. One command, no dependencies.

    python verify.py            # about a minute, standard library only
    python verify.py --deep     # also re-runs random 2^24-wide segments of the
                                # search (fast with numba, slow without)

Exit code 0 if everything passes, 1 otherwise.
"""
import glob
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "src"))

import cycle_primes as CP  # noqa: E402

FAILED = []
PASSED = 0


def check(cond, label):
    global PASSED
    print(("PASS  " if cond else "FAIL  ") + label)
    if cond:
        PASSED += 1
    else:
        FAILED.append(label)
    return cond


def load_blocks():
    rows = []
    for path in sorted(glob.glob(os.path.join(HERE, "data", "blocks", "block_*.json"))):
        with open(path) as fh:
            rows.append(json.load(fh))
    rows.sort(key=lambda r: r["lo"])
    return rows


def load_terms():
    with open(os.path.join(HERE, "data", "terms.json")) as fh:
        return json.load(fh)


# --------------------------------------------------------------------------
def external_control():
    """What is already published must come out of this code."""
    print("\n== external control: the published OEIS data and comment ==")
    # A354427, data field (Yamada, 2022): 3, 13, 19, 631, "no other terms below 2^24".
    small = sorted({p for p in CP.primes_between(2, 1000) if CP.literal(p)})
    check(small == [3, 13, 19, 631],
          "the definition gives 3, 13, 19, 631 below 1000 -- the OEIS data field")
    # The two terms Yamada left in the comment, with the witnesses he gave.
    check(CP.confirm(1794067711, 9829, 73363),
          "(1794067711, 9829, 73363) is a witness -- OEIS comment")
    check(CP.confirm(10855016833, 5569, 1477111),
          "(10855016833, 5569, 1477111) is a witness -- OEIS comment")
    check(CP.confirm(631, 79, 43) and not CP.confirm(631, 79, 7),
          "negative control: 7 divides 79^2+79+1 but does not close the cycle")


def reduction_theorem(limit=100000, samples=2000):
    """The reduction (RESULT.md, section 2) agrees with the definition."""
    print("\n== the reduction agrees with the definition ==")
    ps = CP.primes_between(2, limit + 1)
    bad = [p for p in ps if CP.reduction(p) != CP.literal(p)]
    check(not bad, "reduction(p) == literal(p) for all %d primes p <= %d%s"
          % (len(ps), limit, "" if not bad else " -- differs at %s" % bad[:5]))
    rng = random.Random(20260911)
    big, bad = [], []
    while len(big) < samples:
        p = rng.randrange(10 ** 9, 10 ** 11) | 1
        if CP.is_prime(p) and p % 3 == 1:
            big.append(p)
            if CP.reduction(p) != CP.literal(p):
                bad.append(p)
    check(not bad, "and for %d random primes p = 1 (mod 3) in [10^9, 10^11]%s"
          % (samples, "" if not bad else " -- differs at %s" % bad))
    known = [1794067711, 10855016833]
    check(all(CP.reduction(p) == CP.literal(p) != [] for p in known),
          "and it finds both comment terms, whose r exceeds p")


def blocks_and_terms():
    """The search log covers [0, X] without gaps and every witness is real."""
    print("\n== the search log ==")
    rows = load_blocks()
    if not check(bool(rows), "data/blocks/ is not empty"):
        return
    gaps, end = [], 0
    for r in rows:
        if r["lo"] != end:
            gaps.append((end, r["lo"]))
        end = max(end, r["hi"])
    terms = load_terms()
    X = terms["X"]
    check(not gaps and rows[0]["lo"] == 0 and end == X + 1,
          "the %d blocks tile [0, %d] with no gap and no overlap%s"
          % (len(rows), X, "" if not gaps else " -- gaps %s" % gaps[:3]))
    wit = sorted({tuple(w) for r in rows for w in r["witnesses"]})
    fake = [w for w in wit if not CP.confirm(*w)]
    check(not fake, "all %d witnesses are confirmed with exact integers%s"
          % (len(wit), "" if not fake else " -- %s" % fake))
    outside = [w for r in rows for w in r["witnesses"] if not r["lo"] <= w[0] < r["hi"]]
    check(not outside, "every witness lies inside the block that reports it")
    ps = sorted({w[0] for w in wit})
    check(ps == terms["terms"],
          "data/terms.json lists exactly the primes of the log: %s" % ps)
    check(sorted(map(tuple, terms["witnesses"])) == wit,
          "and exactly its witnesses")


def deep(segments=3):
    """Re-run random segments of the search and compare with the log."""
    print("\n== re-running random segments of the search ==")
    import search as S
    rows = load_blocks()
    X = load_terms()["X"]
    rng = random.Random()
    width = 1 << 24 if S.HAVE_NUMBA else 20000
    for _ in range(segments):
        lo = rng.randrange(0, X - width)
        got = S.segment((lo, lo + width))
        logged = sorted({tuple(w) for r in rows for w in r["witnesses"]
                         if lo <= w[0] < lo + width})
        check([tuple(w) for w in got] == logged,
              "[%d, %d) re-run gives the logged witnesses %s" % (lo, lo + width, logged))


FRONT_PAGE_PARTS = (
    ("hallazgo:que", "what was found, in one sentence"),
    ("hallazgo:enunciado", "the exact statement"),
    ("hallazgo:ejemplo", "the smallest case, with numbers"),
    ("hallazgo:prueba", "why it is proved"),
    ("hallazgo:comprobar", "the command that checks it"),
    ("hallazgo:nodice", "what it does not say"),
)


def front_page():
    """The front page states the finding, in six parts, before anything else."""
    print("\n== front page: the finding, in six parts, before anything else ==")
    historia = re.compile(
        r"(what changed in version|qu[eé] cambi[oó] en la versi[oó]n|"
        r"version \d|versi[oó]n \d|release \d)", re.I)
    leccion = re.compile(
        r"(la regla que sale|the rule that comes out|the rule this leaves|"
        r"lo que esto ense[nñ]a|what this teaches|the lesson)", re.I)
    for name in ("README.md", "README.es.md", "RESULT.md"):
        path = os.path.join(HERE, name)
        if not os.path.exists(path):
            check(False, "%s exists" % name)
            continue
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        at = [text.find("<!-- %s -->" % a) for a, _ in FRONT_PAGE_PARTS]
        missing = [q for (a, q), i in zip(FRONT_PAGE_PARTS, at) if i < 0]
        if not check(not missing, "%s: has all six parts%s"
                     % (name, "" if not missing else " -- missing %s" % missing)):
            continue
        check(at == sorted(at), "%s: the six parts are in order" % name)
        head = text[: at[0]]
        check(len(head.splitlines()) <= 12,
              "%s: the finding is at the top (line %d)" % (name, len(head.splitlines()) + 1))
        m = historia.search(head)
        check(m is None, "%s: no version history before the finding%s"
              % (name, "" if m is None else " -- found %r" % m.group(0)))
        numerals = len(re.findall(r"\d[\d.,]{2,}", text[at[2]:at[3]]))
        check(numerals >= 3, "%s: the example carries numbers (%d found)" % (name, numerals))
        part = text[at[4]:at[5]]
        check("```" in part or "\n    " in part,
              "%s: the check part carries an executable command" % name)
        m = leccion.search(text)
        check(m is None, "%s: no methodological aside%s"
              % (name, "" if m is None else " -- found %r" % m.group(0)))
        check("POR LLENAR" not in text and "POR_LLENAR" not in text,
              "%s: no unfilled template placeholder" % name)


def explainer():
    """The explainer page cannot go stale in silence."""
    print("\n== the explainer page is in sync with the data ==")
    terms = load_terms()
    expected = {
        "x_bound": "{:,}".format(terms["X"]),
        "n_terms": str(len(terms["terms"])),
        "old_frontier": "{:,}".format(2 ** 24),
        "a5": "{:,}".format(terms["terms"][4]),
        "a6": "{:,}".format(terms["terms"][5]),
    }
    for page in (os.path.join("docs", "index.html"), os.path.join("docs", "es", "index.html")):
        path = os.path.join(HERE, page)
        if not check(os.path.exists(path), "%s exists" % page):
            continue
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        facts = dict(re.findall(r'data-fact="([a-z_0-9]+)">([^<]+)<', html))
        wrong = {k: (facts.get(k), v) for k, v in expected.items()
                 if facts.get(k, "").replace(".", ",") != v}
        check(not wrong, "%s: every tagged number matches the data%s"
              % (page, "" if not wrong else " -- %s" % wrong))
        missing = [s for s in re.findall(r'<img src="([^"]+)"', html)
                   if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(path), s)))]
        check(not missing, "%s: every figure it references exists%s"
              % (page, "" if not missing else " -- missing %s" % missing))
    import make_figures as MF
    stale = []
    for name, fn in MF.FIGURES.items():
        for es, suf in ((False, ""), (True, ".es")):
            f = os.path.join(HERE, "docs", "figures", "%s%s.svg" % (name, suf))
            if not os.path.exists(f):
                stale.append(os.path.basename(f))
                continue
            with open(f, encoding="utf-8") as fh:
                if fh.read() != fn(terms, es=es):
                    stale.append(os.path.basename(f))
    check(not stale, "the %d figures are what their generator produces today%s"
          % (2 * len(MF.FIGURES), "" if not stale else " -- stale: %s" % stale))


def readme_counts():
    """The number of checks the front pages announce is the real one."""
    print("\n== the front pages announce the real number of checks ==")
    if "--deep" in sys.argv:
        # The announced count is the one of the default run; --deep adds its
        # own checks on top, so the comparison is only meaningful without it.
        print("(skipped under --deep: the front pages count the default run)")
        return
    total = PASSED + len(FAILED) + 2        # this check and the next one
    for name in ("README.md", "README.es.md"):
        with open(os.path.join(HERE, name), encoding="utf-8") as fh:
            text = fh.read()
        m = re.search(r"<!-- checks -->(\d+)<!-- /checks -->", text)
        check(m is not None and int(m.group(1)) == total,
              "%s announces %s checks; there are %d"
              % (name, m.group(1) if m else "no count", total))


def main():
    external_control()
    reduction_theorem()
    blocks_and_terms()
    if "--deep" in sys.argv:
        deep()
    front_page()
    explainer()
    readme_counts()
    print("\n%d passed, %d failed" % (PASSED, len(FAILED)))
    for f in FAILED:
        print("  FAILED: " + f)
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
