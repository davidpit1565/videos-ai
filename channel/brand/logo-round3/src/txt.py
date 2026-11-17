from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import functools, math
F='/tmp/claude-0/-home-user-videos-ai/2effda64-8e71-5ab6-95b7-5d1257c9dd3f/scratchpad/r3/fonts/'
@functools.lru_cache(None)
def load(name, axes=()):
    f=TTFont(F+name)
    if axes: f=instantiateVariableFont(f, dict(axes))
    return f
def glyphs(name, text, size, axes=(), track=0):
    """returns list of (glyphname, x_advance_offset) and total width, scale"""
    f=load(name,axes); cmap=f.getBestCmap(); gs=f.getGlyphSet(); upm=f['head'].unitsPerEm; sc=size/upm
    hmtx=f['hmtx']; x=0; out=[]
    for ch in text:
        g=cmap[ord(ch)]; out.append((g,x)); x+=hmtx[g][0]*sc+track
    return f,gs,out,x-track,sc
def text_path(name, text, size, x, y, axes=(), track=0, anchor='start'):
    f,gs,out,w,sc=glyphs(name,text,size,axes,track)
    x0 = x - (w/2 if anchor=='middle' else w if anchor=='end' else 0)
    pen=SVGPathPen(gs)
    for g,gx in out:
        gs[g].draw(TransformPen(pen,(sc,0,0,-sc,x0+gx,y)))
    return pen.getCommands(), w
def text_on_circle(name, text, size, cx, cy, r, start_deg, axes=(), track=0):
    """text centred at angle start_deg (0=top), clockwise, baseline on radius r"""
    f,gs,out,w,sc=glyphs(name,text,size,axes,track)
    hmtx=f['hmtx']; pen=SVGPathPen(gs)
    for g,gx in out:
        adv=hmtx[g][0]*sc; mid=gx+adv/2 - w/2
        a=math.radians(start_deg)+mid/r
        c,s=math.cos(a),math.sin(a)
        # glyph local: x right, y up(font) ; place so glyph centre at angle a
        px=cx+r*math.sin(a); py=cy-r*math.cos(a)
        # transform: local (u,v) with u along tangent, v outward
        t=(sc*c, sc*s, sc*s, -sc*c, px-(adv/2)*c, py-(adv/2)*s)
        gs[g].draw(TransformPen(pen,t))
    return pen.getCommands()
