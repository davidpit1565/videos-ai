#!/usr/bin/env python3
"""Writes hf/index.html: a TEXT-ONLY stand-in of ep92's overlays (same positions, sizes and windows as build92.py)
so export/safe_check_hf.js and qa.py --hf can run. The real reel is made by build92.py (ffmpeg + PIL), not by this file."""
import build92 as b
els = []
def blk(lines, size, t0, t1, top, left=65, cls=""):
    out = []
    for i, ln in enumerate(lines):
        out.append(f'<div class="clip t {cls}" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" style="left:{left}px;top:{top + int(i * size * 1.08)}px;font-size:{size}px">{ln}</div>')
    return out
els += [f'<div class="clip t" data-start="0" data-duration="{b.HOOK_D}" style="left:{65+112+26}px;top:282px;font-size:124px">ChatGPT</div>',
        f'<div class="clip t" data-start="0" data-duration="{b.HOOK_D}" style="left:65px;top:412px;font-size:140px;color:#19c37d">begged me.</div>']
for lines, a, c, sz in b.cap_windows() + b.cta_windows():
    els += blk(lines, sz, a, c, 330)
html = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=1080, height=1920">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>html,body{{margin:0;width:1080px;height:1920px;background:#000;overflow:hidden;font-family:Inter,Helvetica,Arial,sans-serif;font-weight:900;color:#fff}}
.t{{position:absolute;white-space:nowrap;line-height:1.08;letter-spacing:-.03em}}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{b.D:.3f}" data-width="1080" data-height="1920">
{chr(10).join(els)}
</div>
<script>window.__timelines={{main:gsap.timeline({{paused:true}}).to({{}},{{duration:{b.D:.3f}}})}};</script></body></html>'''
open("hf/index.html", "w").write(html)
