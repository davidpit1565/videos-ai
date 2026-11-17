import os, json, subprocess, base64
from geomA import *
HERE = os.path.dirname(os.path.abspath(__file__)); TMP = os.path.join(HERE, "_tmp")
INK="#0B0B0B"; WHITE="#FFFFFF"; Y="#FFE600"
G = dict(g=0, sep=50)
def lum(h):
    c=[int(h[i:i+2],16)/255 for i in (1,3,5)]; c=[x/12.92 if x<=0.03928 else ((x+0.055)/1.055)**2.4 for x in c]
    return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
def cr(a,b):
    la,lb=sorted((lum(a),lum(b)),reverse=True); return (la+0.05)/(lb+0.05)
OPT = {
 "D dark: ink field, white A+V, yellow check": dict(field=INK, fg=WHITE, acc=Y),
 "L0 white field, ink, yellow check (kit)": dict(field=WHITE, fg=INK, acc=Y),
 "L1 white field, ink keyline round check": dict(field=WHITE, fg=INK, acc=Y, key=20),
 "L2 white field, darker yellow #E3B000": dict(field=WHITE, fg=INK, acc="#E3B000"),
 "L3 yellow field, all ink (check split by gap)": dict(field=Y, fg=INK, acc=INK, g=26),
 "L4 yellow field, ink AW, white check": dict(field=Y, fg=INK, acc=WHITE),
 "L5 white field, yellow disc behind, ink": dict(field=WHITE, fg=INK, acc=INK, g=26, disc=455),
 "L6 off-white #F4F1E8 field, keyline": dict(field="#F4F1E8", fg=INK, acc=Y, key=20),
}
def svg(o, n):
    o=dict(o); gg=dict(G); 
    if "g" in o: gg["g"]=o["g"]
    R = 400 if "disc" not in o else 340
    g,s = fit(geom(**gg), R)
    bg = f'<circle cx="500" cy="500" r="500" fill="{o["field"]}"/>'
    if "disc" in o: bg += f'<circle cx="500" cy="500" r="{o["disc"]}" fill="{Y}"/>'
    key = ""
    if o.get("key"):
        key = polys(g["y"], INK, f' stroke="{INK}" stroke-width="{2*o["key"]}" stroke-linejoin="miter" stroke-miterlimit="3"')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="{n}" height="{n}">{bg}{polys(g["fg"],o["fg"])}{key}{polys(g["y"],o["acc"])}</svg>'
def render(jobs):
    jf=os.path.join(TMP,"jobs.json"); json.dump(jobs,open(jf,"w"))
    subprocess.run(["node",os.path.join(HERE,"render.js"),jf],check=True,env=dict(os.environ,NODE_PATH="/opt/node-tools/node_modules"))
if __name__=="__main__":
    jobs=[dict(html=svg(o,32),w=32,h=32,transparent=True,out=os.path.join(TMP,f"l{i}-32.png")) for i,o in enumerate(OPT.values())]
    render(jobs)
    b64=lambda p:"data:image/png;base64,"+base64.b64encode(open(p,"rb").read()).decode()
    cells=""
    for i,(name,o) in enumerate(OPT.items()):
        im=f'<img src="{b64(os.path.join(TMP,f"l{i}-32.png"))}" style="width:160px;height:160px;image-rendering:pixelated">'
        cells+=f'''<div class=c><div class=t>{name} · acc/field {cr(o["acc"],o["field"]):.2f} fg/field {cr(o["fg"],o["field"]):.2f}</div>
        <div class=r><div class=w>{svg(o,260)}{svg(o,110)}{svg(o,32)}{im}</div><div class=k>{svg(o,110)}{svg(o,32)}{im}</div></div></div>'''
    html=f'''<!doctype html><meta charset=utf-8><style>body{{margin:0;background:#888;font:14px sans-serif;padding:10px;width:1580px}}
    .c{{margin-bottom:8px}}.r{{display:flex}}.w,.k{{display:flex;gap:16px;align-items:center;padding:10px}}.w{{background:#fff}}.k{{background:#000}}.t{{background:#222;color:#eee;padding:4px}}</style>{cells}'''
    open(os.path.join(TMP,"light.html"),"w").write(html)
    render([dict(file=os.path.join(TMP,"light.html"),w=1600,h=1500,out=os.path.join(TMP,"light.png"),full=True)])
