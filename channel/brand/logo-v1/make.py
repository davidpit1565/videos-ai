INK="#0f0f0f"; PAPER="#f4f2ec"; W="#fbfbf8"
def A(bg,fg,sh):  # check card
    return f'''<svg viewBox="0 0 512 512"><rect width="512" height="512" fill="{bg}"/>
<rect x="128" y="128" width="280" height="280" rx="44" fill="{sh}"/>
<rect x="104" y="104" width="280" height="280" rx="44" fill="{fg}"/>
<path d="M168 250 L226 308 L326 190" fill="none" stroke="{bg}" stroke-width="46" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
def B(bg,fg,sh):  # aw lettermark, check as the w's tail
    return f'''<svg viewBox="0 0 512 512"><rect width="512" height="512" fill="{bg}"/>
<text x="256" y="318" text-anchor="middle" font-family="IDB" font-size="250" letter-spacing="-14" fill="{fg}">aw</text>
<path d="M150 392 H362" stroke="{fg}" stroke-width="30" stroke-linecap="round"/></svg>'''
def C(bg,fg,sh):  # toggle ON
    return f'''<svg viewBox="0 0 512 512"><rect width="512" height="512" fill="{bg}"/>
<rect x="84" y="176" width="368" height="184" rx="92" fill="{sh}"/>
<rect x="60" y="152" width="368" height="184" rx="92" fill="{fg}"/>
<circle cx="336" cy="244" r="66" fill="{bg}"/>
<path d="M306 246 L328 268 L366 222" fill="none" stroke="{fg}" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
def D(bg,fg,sh):  # stamp: ring + check, tilted
    return f'''<svg viewBox="0 0 512 512"><rect width="512" height="512" fill="{bg}"/>
<g transform="rotate(-10 256 256)"><circle cx="256" cy="256" r="170" fill="none" stroke="{fg}" stroke-width="30"/>
<circle cx="256" cy="256" r="128" fill="none" stroke="{fg}" stroke-width="8" stroke-dasharray="4 14" stroke-linecap="round"/>
<path d="M186 258 L238 310 L334 198" fill="none" stroke="{fg}" stroke-width="44" stroke-linecap="round" stroke-linejoin="round"/></g></svg>'''
def Ewm(bg,fg):  # wordmark
    return f'''<svg viewBox="0 0 900 200" width="450"><rect width="900" height="200" fill="{bg}"/><text x="20" y="92" font-family="IDB" font-size="96" letter-spacing="-5" fill="{fg}">ACTUALLY</text><text x="20" y="180" font-family="IDB" font-size="96" letter-spacing="-5" fill="{fg}">WORKS</text><path d="M420 150 L452 182 L520 104" fill="none" stroke="{fg}" stroke-width="24" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
L=[("A","CHECK CARD",A),("B","AW LETTERS",B),("C","SWITCH ON",C),("D","TESTED STAMP",D)]
rows=""
for k,n,f in L:
    light=f(PAPER,INK,"#b9b6ac"); dark=f(INK,W,"#55554f")
    rows+=f'''<div class="row"><div class="lab"><b>{k}</b><span>{n}</span></div>
<div class="big">{light}</div><div class="big">{dark}</div>
<div class="circ c1">{light}</div><div class="circ c1">{dark}</div><div class="circ c2">{light}</div><div class="circ c2">{dark}</div></div>'''
    open(f"logo-{k}-light.svg","w").write(light); open(f"logo-{k}-dark.svg","w").write(dark)
html=f'''<!doctype html><meta charset=utf-8><style>@font-face{{font-family:IDB;src:url(InterDisplay-Black.otf)}}
body{{margin:0;background:#dedbd2;font-family:IDB;color:{INK};width:1500px;padding:40px}}
h1{{font-size:54px;letter-spacing:-2px;margin:0 0 6px}} p{{font:500 22px Helvetica;margin:0 0 30px}}
.row{{display:flex;align-items:center;gap:34px;margin-bottom:34px}} .lab{{width:200px}} .lab b{{font-size:110px;display:block;line-height:100px}} .lab span{{font-size:24px}}
.big svg{{width:280px;height:280px;display:block;border-radius:8px}} .circ{{border-radius:50%;overflow:hidden}} .c1{{width:150px;height:150px}} .c2{{width:56px;height:56px}} .circ svg{{width:100%;height:100%;display:block}}
.wm{{display:flex;gap:40px;margin-top:10px}}</style>
<h1>ACTUALLY WORKS · LOGO DIRECTIONS v1</h1><p>Each row: large on light, large on dark, profile circle (as on the profile page), tiny circle (as next to a comment). Drafts, not final.</p>
{rows}<div class="wm">{Ewm(PAPER,INK)}{Ewm(INK,W)}</div>'''
open("sheet.html","w").write(html)
