"""Geometry of mark A (AW + check), parametrised. Coordinates on a free canvas, fitted later."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "logo-kit-B", "src"))
from geom import enclosing_circle

def clip(poly, a, b, c):
    """keep the part of poly where a*x+b*y+c >= 0 (Sutherland-Hodgman)"""
    out = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        fp = a * p[0] + b * p[1] + c; fq = a * q[0] + b * q[1] + c
        if fp >= 0: out.append(p)
        if (fp >= 0) != (fq >= 0):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out

def geom(p=132.0, w=96.0, top=300.0, bot=735.0, tick_top=185.0, g=26.0, apex="yellow", sep=None,
         bar=(596.0, 664.0), pw=None):
    """apex: 'yellow' (yellow stroke whole, white stroke cut to a point: the kit-ABC drawing),
    'white' (white stroke whole with flat top, yellow cut), 'split' (vertical slit through the middle peak).
    sep: None = A and W share a stroke; number = W is its own letter, sep units after the A.
    pw: pitch of the W strokes (default p)."""
    pw = pw or p
    k = p / (bot - top); kw = pw / (bot - top)
    up = lambda b, kk, t=top: [(b, bot), (b + w, bot), (b + w + kk * (bot - t), t), (b + kk * (bot - t), t)]
    dn = lambda a, kk: [(a, top), (a + w, top), (a + w + kk * (bot - top), bot), (a + kk * (bot - top), bot)]
    s1 = up(0, k); s2 = dn(p, k)
    by0, by1 = bar
    cb = [(w + k * (bot - by0) - 3, by0), (2 * p - k * (bot - by0) + 3, by0),
          (2 * p - k * (bot - by1) + 3, by1), (w + k * (bot - by1) - 3, by1)]
    fg = [s1, s2, cb]
    if sep is None:
        x0 = 2 * p                       # bottom-left of the first up stroke of the W
        if pw != p:                      # W strokes steeper/flatter than the A: restart from the foot of s2
            x0 = 2 * p
    else:
        a = p + w + sep
        fg.append(dn(a, kw)); x0 = a + pw
    u1 = up(x0, kw); d2 = dn(x0 + pw, kw); u2 = up(x0 + 2 * pw, kw, tick_top)
    # lines: left edge of d2: x = x0+pw + kw*(y-top);  right edge of u1: x = x0+w+kw*(bot-y)
    n = math.hypot(1, kw)
    if apex == "yellow":   # keep u1 where it is at least g to the left of d2's left edge
        u1 = clip(u1, -1, kw, (x0 + pw - kw * top) - g * n)
    elif apex == "white":  # keep d2 where it is at least g right of u1's right edge
        d2 = clip(d2, 1, kw, -(x0 + w + kw * bot) - g * n)
    else:
        cx = x0 + pw + w / 2
        u1 = clip(u1, -1, 0, cx - g / 2); d2 = clip(d2, 1, 0, -(cx + g / 2))
    fg.append(u1)
    return {"fg": fg, "y": [d2, u2]}

def allpts(g): return [q for grp in ("fg", "y") for pl in g[grp] for q in pl]

def fit(g, R, centre=(500, 500), shift=(0, 0)):
    (cx, cy), r = enclosing_circle(allpts(g))
    s = R / r
    f = lambda q: (centre[0] + shift[0] + (q[0] - cx) * s, centre[1] + shift[1] + (q[1] - cy) * s)
    return {k: [[f(q) for q in pl] for pl in g[k]] for k in ("fg", "y")}, s

def P(poly): return " ".join(f"{round(x,1):g},{round(y,1):g}" for x, y in poly)
def polys(pls, fill, extra=""): return "".join(f'<polygon points="{P(pl)}" fill="{fill}"{extra}/>' for pl in pls)
