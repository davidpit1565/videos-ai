from lib import *; from c1 import rr, eye
B='#2447FF'; R='#FF2D2D'
def f1(body,ink,white,brow,small=False,sc=.84):
    d='M500 185 L805 775 L652 660 L500 775 L348 660 L195 775 Z'
    s=f'<path d="{d}" fill="{body}" stroke="{body}" stroke-width="110" stroke-linejoin="round"/>'
    ex,ey=(92,108) if small else (82,100)
    s+=eye(500-ex-3,548,ex,ey,20,-12,white,ink,.56)+eye(500+ex+3,548,ex,ey,20,-12,white,ink,.56)
    if not small: s+=f'<path d="M510 428 Q590 368 668 408" fill="none" stroke="{brow}" stroke-width="38" stroke-linecap="round"/>'
    return f'<g transform="translate(500 520) scale({sc}) translate(-500 -507)">{s}</g>'
def f2(white,ink,brow,small=False):
    w=92 if small else 76
    s=f'<circle cx="330" cy="600" r="170" fill="{white}"/><circle cx="670" cy="600" r="170" fill="{white}"/>'
    s+=f'<circle cx="375" cy="565" r="85" fill="{ink}"/><circle cx="715" cy="565" r="85" fill="{ink}"/>'
    s+=f'<path d="M178 372 L468 392" stroke="{brow}" stroke-width="{w}" stroke-linecap="round"/>'
    s+=f'<path d="M540 292 Q680 190 822 232" fill="none" stroke="{brow}" stroke-width="{w}" stroke-linecap="round"/>'
    return f'<g transform="translate(0 -10)">{s}</g>'
def f3(body,ink,bg,small=False):
    s=f'<path d="M500 800 C500 930 640 880 700 1010" fill="none" stroke="{ink}" stroke-width="58" stroke-linecap="round"/>'
    s+=rr(435,730,130,110,34,f'fill="{ink}"')
    s+=rr(346,196,92,220,20,f'fill="{body}"')+rr(562,196,92,220,20,f'fill="{body}"')
    if not small: s+=f'<circle cx="392" cy="262" r="21" fill="{bg}"/><circle cx="608" cy="262" r="21" fill="{bg}"/>'
    s+=rr(262,372,476,392,140,f'fill="{body}"')
    ex,ey=(46,62) if small else (38,54)
    s+=f'<ellipse cx="415" cy="545" rx="{ex}" ry="{ey}" fill="{ink}"/><ellipse cx="585" cy="545" rx="{ex}" ry="{ey}" fill="{ink}"/>'
    s+=f'<path d="M430 655 Q520 715 600 640" fill="none" stroke="{ink}" stroke-width="{40 if small else 32}" stroke-linecap="round"/>'
    return f'<g transform="rotate(-9 500 500) translate(0 -20)">{s}</g>'
def f4(base,dome,well,hl,tick,small=False):
    s=f'<path d="M150 630 A350 130 0 0 1 850 630 L850 730 A350 130 0 0 1 150 730 Z" fill="{base}"/>'
    s+=f'<ellipse cx="500" cy="630" rx="350" ry="130" fill="{base}"/><ellipse cx="500" cy="630" rx="292" ry="100" fill="{well}"/>'
    s+=f'<path d="M240 610 L240 500 A260 200 0 0 1 760 500 L760 610 A260 90 0 0 1 240 610 Z" fill="{dome}"/>'
    s+=f'<path d="M322 440 A200 130 0 0 1 470 345" fill="none" stroke="{hl}" stroke-width="36" stroke-linecap="round"/>'
    if not small: s+=''.join(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{tick}" stroke-width="34" stroke-linecap="round"/>' for x1,y1,x2,y2 in ((500,215,500,135),(690,262,735,196),(310,262,265,196)))
    return f'<g transform="translate(0 {-40 if small else 0})">{s}</g>'
