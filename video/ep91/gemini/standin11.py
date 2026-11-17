#!/usr/bin/env python3
"""text-only stand-in for safe_check_hf (captions + CTA card positions from caps11.py). usage: standin11.py <cues.json> <out.html>"""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import caps11 as c
L = json.load(open(sys.argv[1]))['lines']; f = c.f_cap; sp = f.getlength(" "); items = []
def lines_for(words):
    full = sum(f.getlength(w) for w in words) + sp * (len(words) - 1)
    if full <= 880: return [words]
    best = None
    for k in range(1, len(words)):
        w1 = sum(f.getlength(x) for x in words[:k]) + sp * (k - 1); w2 = sum(f.getlength(x) for x in words[k:]) + sp * (len(words) - k - 1)
        sc = abs(w1 - w2) - (10000 if words[k - 1].endswith(',') else 0)
        if max(w1, w2) <= 880 and (best is None or sc < best[0]): best = (sc, k)
    k = best[1]; return [words[:k], words[k:]]
for words, ln in ((["Me", "with", "Claude,", "it", "listens."], 0), (["Me", "with", "ChatGPT,", "it's", "way", "more", "tangled."], 1)):
    t0 = L[ln]['start'] - 0.05 + 0.2; t1 = (2.45 if ln == 0 else 5.62) - 0.15; ls = lines_for(words); lh = 98; y = 1121 - lh * len(ls) / 2 + 6
    for row in ls:
        txt = " ".join(row); w = f.getlength(txt); items.append((txt, (1080 - w) / 2, y + 14, 80, t0, t1)); y += lh
fc = c.f_card
for li, row in enumerate(c.CARD):
    txt = " ".join(row); w = fc.getlength(txt); items.append((txt, 90 + (900 - w) / 2, 420 + [28, 112, 206, 312][li] + 14, 78, L[2]['start'] + 0.4, 10.0))
divs = "\n".join(f'<div class="clip t" data-start="{round(a,2)}" data-duration="{round(max(0.1,b-a),2)}" style="left:{int(x)}px;top:{int(y)}px;font-size:{s}px;color:#111">{t}</div>' for t, x, y, s, a, b in items)
open(sys.argv[2], 'w').write(f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=1080, height=1920">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>html,body{{margin:0;width:1080px;height:1920px;background:#f5f1e9;overflow:hidden;font-family:Inter,Helvetica,Arial,sans-serif;font-weight:900}}.t{{position:absolute;white-space:nowrap;line-height:1.08;letter-spacing:-.02em}}</style></head><body>
<!-- text-only stand-in for ep91 final11 captions + CTA card; the art's own burned-in text is not checked -->
<div id="root" data-composition-id="main" data-start="0" data-duration="10.03" data-width="1080" data-height="1920">
{divs}
</div><script>window.__timelines={{main:gsap.timeline({{paused:true}}).to({{}},{{duration:10.03}})}};</script></body></html>''')
