import math
INK="#0B0B0C"; W="#FFFFFF"; Y="#FFE600"; NP="#EFECE4"
def poly(pts,fill): return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)}" fill="{fill}"/>'
def bar(x0,y0,x1,y1,t,fill):
    # a stroke as a parallelogram with flat (horizontal) cuts top and bottom
    h=t/abs(math.sin(math.atan2(abs(y1-y0),abs(x1-x0))))/2
    return poly([(x0-h,y0),(x0+h,y0),(x1+h,y1),(x1-h,y1)],fill)
def A(bg,fg,acc):  # tick ligature: A + W zigzag, last two strokes = check
    base,cap,top=735,300,185; t=92; dx=118
    xs=[150+ i*dx for i in range(6)]
    s=f'<rect width="1000" height="1000" fill="{bg}"/>'
    s+=bar(xs[0],base,xs[1],cap,t,fg)+bar(xs[1],cap,xs[2],base,t,fg)+bar(xs[2],base,xs[3],cap,t,fg)
    s+=f'<rect x="{xs[0]+28}" y="560" width="{xs[2]-xs[0]-56}" height="70" fill="{fg}"/>'
    s+=bar(xs[3],cap,xs[4],base,t,acc)+bar(xs[4],base,xs[5]+52,top,t,acc)
    return f'<svg viewBox="0 0 1000 1000">{s}</svg>'
def B(bg,fg,acc):  # the highlight: heavy A, yellow marker swipe as the crossbar
    s=f'<rect width="1000" height="1000" fill="{bg}"/>'
    s+=poly([(410,215),(590,215),(820,790),(630,790),(500,455),(370,790),(180,790)],fg)
    sw=[(118,612),(140,560),(905,505),(884,640),(600,662),(300,676),(126,668)]
    s+=f'<g transform="rotate(-2 500 600)">{poly(sw,acc)}</g>'
    return f'<svg viewBox="0 0 1000 1000">{s}</svg>'
def C(bg,face,feat,ring=False):  # the wink: dot eye + check eye
    s=f'<rect width="1000" height="1000" fill="{bg}"/><circle cx="500" cy="500" r="500" fill="{face}"/>'
    s+=f'<circle cx="320" cy="520" r="105" fill="{feat}"/>'
    s+=bar(520,470,625,640,104,feat)+bar(625,640,850,270,104,feat)
    return f'<svg viewBox="0 0 1000 1000">{s}</svg>'
def wm(bg,fg,acc):
    return f'''<svg viewBox="0 0 980 300" width="490"><rect width="980" height="300" fill="{bg}"/><rect x="24" y="158" width="560" height="118" fill="{acc}" transform="rotate(-1.5 260 215)"/>
<text x="34" y="132" font-family="AB" font-size="124" letter-spacing="-3" fill="{fg}">ACTUALLY</text><text x="40" y="262" font-family="AB" font-size="124" letter-spacing="-3" fill="{INK}">WORKS</text></svg>'''
L=[("A","TICK LIGATURE · AW with the check inside",A(INK,W,Y),A(W,INK,Y)),
   ("B","THE HIGHLIGHT · A with a marker swipe",B(INK,W,Y),B(W,INK,Y)),
   ("C","THE WINK · a face for a faceless channel",C(INK,Y,INK),C(W,INK,Y))]
rows=""
for k,n,d,l in L:
    open(f"logo2-{k}-dark.svg","w").write(d); open(f"logo2-{k}-light.svg","w").write(l)
    rows+=f'''<div class="row"><div class="lab"><b>{k}</b><span>{n}</span></div>
<div class="circ c0">{d}</div><div class="circ c0 bd">{l}</div><div class="circ c1">{d}</div><div class="circ c1 bd">{l}</div><div class="circ c2">{d}</div><div class="circ c2 bd">{l}</div><div class="circ c3">{d}</div><div class="circ c3 bd">{l}</div></div>'''
html=f'''<!doctype html><meta charset=utf-8><style>@font-face{{font-family:AB;src:url(ArchivoBlack-Regular.ttf)}}
body{{margin:0;background:#d9d6cc;font-family:AB;color:{INK};width:1560px;padding:44px}}
h1{{font-size:56px;letter-spacing:-1px;margin:0 0 6px}} p{{font:500 22px Helvetica;margin:0 0 34px}}
.row{{display:flex;align-items:center;gap:30px;margin-bottom:40px}} .lab{{width:300px}} .lab b{{font-size:120px;display:block;line-height:110px}} .lab span{{font:700 20px Helvetica}}
.circ{{border-radius:50%;overflow:hidden;flex:none}} .bd{{box-shadow:0 0 0 2px #bbb}} .c0{{width:320px;height:320px}} .c1{{width:110px;height:110px}} .c2{{width:40px;height:40px}} .c3{{width:32px;height:32px}} .circ svg{{width:100%;height:100%;display:block}}
.wm{{display:flex;gap:40px}}</style>
<h1>ACTUALLY WORKS · LOGO DIRECTIONS v2</h1><p>Each row: 320 px, 110 px (profile), 40 px and 32 px (comments), on black and on white. Drafts for choosing a direction, not final artwork.</p>
{rows}<div class="wm">{wm(INK,W,Y)}{wm(NP,INK,Y)}</div>'''
open("sheet.html","w").write(html)
