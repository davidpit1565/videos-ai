"""Wordmark + lockups. Text is converted to outlines with fontTools (no font needed to view)."""
import math, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
import uharfbuzz as hb
from geom import INK,WHITE,SIGNAL,polygon,swipe
FONT=os.path.join(os.path.dirname(__file__),'..','..','logo-v2','ArchivoBlack-Regular.ttf')
_f=TTFont(FONT); _gs=_f.getGlyphSet()
_hbf=hb.Font(hb.Face(open(FONT,'rb').read()))
def _b(name):
    bp=BoundsPen(_gs); _gs[name].draw(bp); return bp.bounds
CAP=_b('H')[3]                       # cap height in font units (flat letters)
TRACK=-6                             # font units added between letters
KERN={('L','L'):-10,('L','Y'):-14,('A','C'):0,('W','O'):-6,('R','K'):0}   # hand kerning on top of the font's own

def line(text,x,base,k):
    """Outline `text`, left ink edge at x, baseline at `base`, k = svg units per font unit.
    Returns (path d, ink left, ink right)."""
    buf=hb.Buffer(); buf.add_str(text); buf.guess_segment_properties(); hb.shape(_hbf,buf,{"kern":True})
    names=[_f.getGlyphName(i.codepoint) for i in buf.glyph_infos]; adv=[p.x_advance for p in buf.glyph_positions]
    pen=SVGPathPen(_gs,ntos=lambda v:f"{round(v,2):g}"); cur=-_b(names[0])[0]; right=0
    for i,n in enumerate(names):
        _gs[n].draw(TransformPen(pen,(k,0,0,-k,x+cur*k,base)))
        right=x+(cur+_b(n)[2])*k
        cur+=adv[i]+TRACK+(KERN.get((text[i],text[i+1]),0) if i+1<len(text) else 0)
    return pen.getCommands(),x,right

def chisel_bar(l,r,base,cap,ang=2.0,cut=70.0):
    """Bar behind one word. Top edge passes 0.08 cap above the cap line at the word's left
    edge, bottom edge 0.10 cap under the baseline at its right edge (so the 2-degree tilt
    never uncovers a letter). Ends: 70-degree chisel cuts, 0.35 cap past the word on the
    left and 0.5 cap on the right, measured at mid-height."""
    t=math.tan(math.radians(ang)); c=math.cos(math.radians(cut)); s=math.sin(math.radians(cut))
    top=lambda x:base-1.08*cap-(x-l)*t; bot=lambda x:base+0.10*cap-(x-r)*t
    def end(xm):
        ym=(top(xm)+bot(xm))/2; out=[]
        for f,x_ref,y_ref in((top,l,base-1.08*cap),(bot,r,base+0.10*cap)):
            u=(y_ref-(xm-x_ref)*t-ym)/(s-c*t); out.append((xm-u*c,ym+u*s))
        return out
    (lt,lb),(rt,rb)=end(l-0.35*cap),end(r+0.5*cap)
    return [lt,rt,rb,lb]

def wordmark(mode,mark=None,one_swipe=False,pad=0.9,cap=200.0):
    """mark: None or (A,S) master polygons. Returns (svg, width, height)."""
    k=cap/CAP; fg=WHITE if mode=='dark' else INK; bg=INK if mode=='dark' else WHITE
    P=pad*cap; lead=(1.34 if one_swipe else 1.47)*cap                       # baseline to baseline
    top=P
    b1=top+cap; b2=b1+lead
    body=''; x0=P
    if mark:
        A,S=mark
        ay0=min(y for x,y in A); ay1=max(y for x,y in A); m=(b2-(b1-cap))/(ay1-ay0)
        minx=min(x for x,y in A+S)
        T=lambda poly:[(P+(x-minx)*m,(b1-cap)+(y-ay0)*m) for x,y in poly]
        A2,S2=T(A),T(S)
        body+=(polygon(A2,WHITE)+polygon(S2,SIGNAL)) if mode=='dark' else (polygon(S2,SIGNAL)+polygon(A2,INK))
        x0=max(x for x,y in A2+S2)+(0.9 if one_swipe else 1.25)*cap
    d1,l1,r1=line("ACTUALLY",x0,b1,k); d2,l2,r2=line("WORKS",x0,b2,k)
    right=r1
    if not one_swipe:
        bar=chisel_bar(l2,r2,b2,cap)
        shift=x0-min(x for x,y in bar) if not mark else 0   # wordmark alone: bar tip sits on the left margin
        if shift>0:
            d1,l1,r1=line("ACTUALLY",x0+shift,b1,k); d2,l2,r2=line("WORKS",x0+shift,b2,k)
            bar=[(x+shift,y) for x,y in bar]
        body+=polygon(bar,SIGNAL); right=max(r1,max(x for x,y in bar))
        body+=f'<path d="{d1}" fill="{fg}"/><path d="{d2}" fill="{INK}"/>'
    else:
        body+=f'<path d="{d1}" fill="{fg}"/><path d="{d2}" fill="{fg}"/>'
    W=right+P; H=b2+P+(0 if one_swipe else 0.10*cap)
    W=round(W,1); H=round(H,1)
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:g} {H:g}"><rect width="{W:g}" height="{H:g}" fill="{bg}"/>{body}</svg>'
    return svg,W,H
