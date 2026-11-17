#!/usr/bin/env python3
"""Text-only stand-in of ep92's two overlays (same sizes/windows as build92.py) so export/safe_check_hf.js and qa.py --hf can run. The real reel is made by build92.py (ffmpeg + PIL)."""
import sys
CU = sys.argv[1] if len(sys.argv) > 1 else "voice/cues.json"; OUTH = sys.argv[2] if len(sys.argv) > 2 else "hf/index.html"; sys.argv = ["x", CU]
import build92 as b
els = []
def blk(lines, size, t0, t1, top, lh):
    for i, ln in enumerate(lines):
        els.append(f'<div class="clip t" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" style="left:540px;transform:translateX(-50%);top:{top + int(i * size * lh)}px;font-size:{size}px">{ln}</div>')
blk(b.HOOK_LINES, b.HOOK_SIZE, 0, b.HOOK_END, 268, 1.0); blk(b.END_LINES, b.END_SIZE, b.END_T, b.D, b.END_Y, 1.04)
D = b.D
html = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=1080, height=1920">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>html,body{{margin:0;width:1080px;height:1920px;background:#000;overflow:hidden;font-family:Inter,Helvetica,Arial,sans-serif;font-weight:900;color:#fff}}
.t{{position:absolute;white-space:nowrap;line-height:1.0;letter-spacing:-.03em}}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D:.3f}" data-width="1080" data-height="1920">
{chr(10).join(els)}
</div>
<script>window.__timelines={{main:gsap.timeline({{paused:true}}).to({{}},{{duration:{D:.3f}}})}};</script></body></html>'''
open(OUTH, "w").write(html); print("hf", D)
