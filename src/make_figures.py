#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The figures of the explainer, generated from data/terms.json.

    python src/make_figures.py

Each figure is a function of the data and of the language, so verify.py can
regenerate it and compare character by character: a figure that no longer
matches the data fails the verification.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "docs", "figures")

STYLE = """<style>
  svg { font-family: system-ui, -apple-system, 'Segoe UI', sans-serif; }
  .ink { fill: #1d2433; } .soft { fill: #5b6478; } .line { stroke: #1d2433; }
  .accent { fill: #2f6fdd; } .accentline { stroke: #2f6fdd; }
  .warm { fill: #c2541b; } .warmline { stroke: #c2541b; }
  .box { fill: #eef2fa; stroke: #9aa7c2; } .grid { stroke: #d5dbe7; }
  @media (prefers-color-scheme: dark) {
    .ink { fill: #e7ebf3; } .soft { fill: #a8b1c4; } .line { stroke: #e7ebf3; }
    .accent { fill: #7aa7ff; } .accentline { stroke: #7aa7ff; }
    .warm { fill: #ff9a5c; } .warmline { stroke: #ff9a5c; }
    .box { fill: #1f2940; stroke: #4a587a; } .grid { stroke: #2e3850; }
  }
</style>"""


def _svg(w, h, body, title):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'width="100%%" role="img" aria-label="%s">\n%s\n%s\n</svg>\n'
            % (w, h, title, STYLE, body))


def _t(x, y, s, cls="ink", size=15, anchor="middle", weight="normal"):
    return ('<text x="%.1f" y="%.1f" class="%s" font-size="%d" text-anchor="%s" '
            'font-weight="%s">%s</text>' % (x, y, cls, size, anchor, weight, s))


def fig_cycle(terms, es=False):
    """The cycle of 631: 631 -> 79 -> 43 -> 631, with the numbers that make it."""
    p, q, r = 631, 79, 43
    assert [p, q, r] in [list(w) for w in terms["witnesses"]]
    pos = {"p": (340, 70), "q": (560, 300), "r": (120, 300)}
    body = []
    for key, (x, y) in pos.items():
        body.append('<circle cx="%d" cy="%d" r="38" class="box" stroke-width="2"/>' % (x, y))
        body.append(_t(x, y + 7, {"p": p, "q": q, "r": r}[key], size=22, weight="bold"))
    arrows = [
        ("p", "q", "631 + 1 = 2³ · 79"),
        ("q", "r", "79² + 79 + 1 = 3 · 7² · 43"),
        ("r", "p", "43² + 43 + 1 = 3 · 631"),
    ]
    body.append('<defs><marker id="h" viewBox="0 0 10 10" refX="9" refY="5" '
                'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                '<path d="M0,0 L10,5 L0,10 z" class="accent"/></marker></defs>')
    for a, b, label in arrows:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy)
        sx, sy = x1 + dx / d * 44, y1 + dy / d * 44
        ex, ey = x2 - dx / d * 46, y2 - dy / d * 46
        body.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="accentline" '
                    'stroke-width="2.5" marker-end="url(#h)"/>' % (sx, sy, ex, ey))
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        off = {"pq": (70, -18), "qr": (0, 44), "rp": (-70, -18)}[a + b]
        body.append(_t(mx + off[0], my + off[1], label, cls="soft", size=14))
    cap = ("Cada flecha: el número de la izquierda de la cuenta es divisible por el primo al que llega."
           if es else "Each arrow: the prime it points to divides the number on the left.")
    body.append(_t(340, 390, cap, cls="soft", size=13))
    return _svg(680, 410, "\n".join(body),
                "ciclo de 631" if es else "the cycle of 631")


def fig_reduction(terms, es=False):
    """Why the cofactor is forced: residues mod p on a line, N/r below p."""
    body = []
    L, R, Y = 60, 620, 150
    body.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="line" stroke-width="2"/>' % (L, Y, R, Y))
    for x, lab in ((L, "0"), (R, "p")):
        body.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="line" stroke-width="2"/>' % (x, Y - 10, x, Y + 10))
        body.append(_t(x, Y + 32, lab, size=16))
    quarter = L + (R - L) / 4
    body.append('<rect x="%d" y="%d" width="%.1f" height="22" class="box" stroke-width="1"/>' % (L, Y - 11, quarter - L))
    body.append(_t((L + quarter) / 2, Y - 22, "m < N/p < p/4 + 2", cls="accent", size=14))
    mx = L + (R - L) * 0.13
    body.append('<circle cx="%.1f" cy="%d" r="7" class="warm"/>' % (mx, Y))
    body.append(_t(mx, Y + 32, "m = N·ρ′ mod p", cls="warm", size=14))
    lines = (["Si r > p, el cofactor m = N/r es menor que p,",
              "y como m ≡ N·ρ′ (mod p) sólo hay un lugar posible:",
              "una división decide, sin factorizar N = q² + q + 1."]
             if es else
             ["If r > p, the cofactor m = N/r is smaller than p,",
              "and since m ≡ N·ρ′ (mod p) it has only one possible place:",
              "one division decides, without factoring N = q² + q + 1."])
    for i, s in enumerate(lines):
        body.append(_t(340, 235 + 22 * i, s, cls="soft", size=14))
    return _svg(680, 310, "\n".join(body),
                "el cofactor forzado" if es else "the forced cofactor")


def fig_frontier(terms, es=False):
    """The known terms and the search frontiers on a log scale."""
    X = terms["X"]
    lo_e, hi_e = 0, math.ceil(math.log10(X)) + 0.3
    L, R, Y = 60, 640, 170

    def px(v):
        return L + (R - L) * (math.log10(v) - lo_e) / (hi_e - lo_e)

    body = ['<line x1="%d" y1="%d" x2="%d" y2="%d" class="line" stroke-width="1.5"/>' % (L, Y, R, Y)]
    for e in range(0, int(hi_e) + 1):
        x = px(10 ** e)
        body.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" class="grid"/>' % (x, 40, x, Y))
        body.append(_t(x, Y + 22, "10<tspan baseline-shift=\"super\" font-size=\"10\">%d</tspan>" % e, cls="soft", size=13))
    for v, lab, cls, yy in ((2 ** 24, "2²⁴ (OEIS, 2022)", "soft", 60),
                            (X, ("hasta aquí, sin huecos" if es else "searched, no gaps"), "accent", 60)):
        x = px(v)
        body.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" class="%s" stroke-width="2" stroke-dasharray="5,4"/>'
                    % (x, 45, x, Y, "accentline" if cls == "accent" else "warmline"))
        body.append(_t(x, yy - 20, lab, cls=cls, size=13))
    for t in terms["terms"]:
        x = px(t)
        body.append('<circle cx="%.1f" cy="%d" r="6" class="warm"/>' % (x, Y))
    body.append(_t(340, Y + 55, ("Los %d primos hallados (puntos) y hasta dónde se buscó."
                                 if es else "The %d primes found (dots) and how far the search went.")
                   % len(terms["terms"]), cls="soft", size=14))
    return _svg(700, 250, "\n".join(body),
                "frontera de búsqueda" if es else "search frontier")


FIGURES = {"cycle": fig_cycle, "reduction": fig_reduction, "frontier": fig_frontier}


def main():
    with open(os.path.join(HERE, "..", "data", "terms.json")) as fh:
        terms = json.load(fh)
    os.makedirs(OUT, exist_ok=True)
    for name, fn in FIGURES.items():
        for es, suf in ((False, ""), (True, ".es")):
            svg = fn(terms, es=es)
            nums = [float(v) for v in __import__("re").findall(r'(?:x|y|cx|cy|x1|x2|y1|y2)="(-?[\d.]+)"', svg)]
            assert min(nums) >= 0, "a coordinate fell off the canvas in %s" % name
            with open(os.path.join(OUT, "%s%s.svg" % (name, suf)), "w", encoding="utf-8") as fh:
                fh.write(svg)
    print("figures written to docs/figures/")


if __name__ == "__main__":
    main()
