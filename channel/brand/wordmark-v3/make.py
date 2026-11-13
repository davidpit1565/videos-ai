INK="#0B0B0C";W="#FFFFFF";Y="#FFE600";NP="#EFECE4"
A="425,235 575,235 788,765 592,765 500,521 408,765 212,765"; SW="177.3,553 892.3,465.2 837.7,615.2 122.7,703"
def mark(x,y,s,fg,over):
    a=f'<polygon points="{A}" fill="{fg}"/>'; sw=f'<polygon points="{SW}" fill="{Y}"/>'
    return f'<g transform="translate({x},{y}) scale({s})">{a+sw if over else sw+a}</g>'
def T(x,y,t,fg,sz=120): return f'<text x="{x}" y="{y}" font-family="AB" font-size="{sz}" letter-spacing="-2" fill="{fg}">{t}</text>'
def box(inner,bg): return f'<svg viewBox="0 0 1260 420" width="630"><rect width="1260" height="420" fill="{bg}"/>{inner}</svg>'
opts=[]
for bg,fg,over in ((INK,W,True),(W,INK,False)):
    # 1: mark + plain two-line text, no yellow in the text
    o1=mark(20,40,.34,fg,over)+T(360,190,"ACTUALLY",fg)+T(360,310,"WORKS",fg)
    # 2: one line, plain, yellow thin underline stroke under WORKS only (stroke, not a box)
    ul=f'<polygon points="356,336 742,318 740,340 354,358" fill="{Y}"/>' if bg==INK else f'<polygon points="356,336 742,318 740,340 354,358" fill="{INK}"/>'
    o2=mark(20,40,.34,fg,over)+T(360,190,"ACTUALLY",fg)+T(360,310,"WORKS",fg)+ul
    # 3: text only, one line, small caps feel, the A of ACTUALLY replaced by the mark
    o3=mark(-20,30,.36,fg,over)+T(270,262,"CTUALLY WORKS",fg,100)
    opts.append((o1,o2,o3,bg))
rows=""
for i,name in enumerate(["1 · MARK + PLAIN TEXT (no yellow in the words)","2 · PLAIN TEXT + THIN UNDERLINE (a line, not a box)","3 · THE MARK IS THE FIRST LETTER"]):
    rows+=f'<div class="lab">{name}</div><div class="row">{box(opts[0][i],INK)}{box(opts[1][i],W)}</div>'
open("sheet.html","w").write(f'<!doctype html><meta charset=utf-8><style>@font-face{{font-family:AB;src:url(ArchivoBlack-Regular.ttf)}}body{{margin:0;background:#d9d6cc;padding:36px;width:1330px;font-family:AB;color:{INK}}}h1{{font-size:40px;margin:0 0 20px}}.lab{{font-size:24px;margin:18px 0 8px}}.row{{display:flex;gap:24px}}</style><h1>WORDMARK v3 · no word inside a coloured box</h1>{rows}')
