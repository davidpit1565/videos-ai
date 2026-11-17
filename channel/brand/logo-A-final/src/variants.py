import os, json, subprocess, base64
from geomA import *
HERE = os.path.dirname(os.path.abspath(__file__)); TMP = os.path.join(HERE, "_tmp"); os.makedirs(TMP, exist_ok=True)
INK="#0B0B0B"; WHITE="#FFFFFF"; Y="#FFE600"
V = {
 "v0 kit-ABC (yellow over, point)": dict(),
 "v8 shared stroke, halves touch (g=0)": dict(g=0),
 "v9 own W, sep 50, halves touch": dict(g=0, sep=50),
 "v10 own W, sep 50, hairline g=12": dict(g=12, sep=50),
 "v11 own W, sep 44, touch, w88 p124": dict(g=0, sep=44, p=124, w=88, bar=(598,662)),
 "v12 own W, sep 56, split g=10": dict(apex="split", g=10, sep=56),
 "v13 shared, hairline g=10": dict(g=10),
 "v14 own W sep 40 touch, tick 215": dict(g=0, sep=40, tick_top=215),
}
def svg(name, n, shape="circle"):
    g, s = fit(geom(**V[name]), 400)
    bg = '<circle cx="500" cy="500" r="500" fill="%s"/>' % INK
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="{n}" height="{n}">{bg}{polys(g["fg"],WHITE)}{polys(g["y"],Y)}</svg>'
def render(jobs):
    jf=os.path.join(TMP,"jobs.json"); json.dump(jobs,open(jf,"w"))
    subprocess.run(["node",os.path.join(HERE,"render.js"),jf],check=True,env=dict(os.environ,NODE_PATH="/opt/node-tools/node_modules"))
jobs=[]
for i,name in enumerate(V):
    for n in (32,):
        jobs.append(dict(html=svg(name,n),w=n,h=n,transparent=True,out=os.path.join(TMP,f"v{i}-{n}.png")))
render(jobs)
b64=lambda p:"data:image/png;base64,"+base64.b64encode(open(p,"rb").read()).decode()
cells=""
for i,name in enumerate(V):
    cells+=f'''<div class=c><div class=t>{name}</div><div class=r>{svg(name,300)}{svg(name,110)}{svg(name,32)}
    <img src="{b64(os.path.join(TMP,f"v{i}-32.png"))}" style="width:160px;height:160px;image-rendering:pixelated"></div></div>'''
html=f'''<!doctype html><meta charset=utf-8><style>body{{margin:0;background:#1c1c1c;color:#ddd;font:14px sans-serif;display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:10px;width:1580px}}
.c{{background:#000;padding:10px}}.r{{display:flex;gap:18px;align-items:center}}.t{{margin-bottom:6px}}</style>{cells}'''
open(os.path.join(TMP,"variants.html"),"w").write(html)
render([dict(file=os.path.join(TMP,"variants.html"),w=1600,h=1500,out=os.path.join(TMP,"variants.png"),full=True)])
