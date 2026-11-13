from lib import *; from c1 import rr, eye
import fin1
B='#2447FF'; R='#FF2D2D'
def f1(body,ink,white,brow,small=False,sc=.9,rot=0,sw=130,wide=True):
    d='M500 225 L815 760 L655 650 L500 760 L345 650 L185 760 Z' if wide else 'M500 185 L805 775 L652 660 L500 775 L348 660 L195 775 Z'
    s=f'<path d="{d}" fill="{body}" stroke="{body}" stroke-width="{sw}" stroke-linejoin="round"/>'
    ex,ey=(96,112) if small else (86,102)
    s+=eye(500-ex-3,545,ex,ey,22,-14,white,ink,.56)+eye(500+ex+3,545,ex,ey,22,-14,white,ink,.56)
    if not small: s+=f'<path d="M508 418 Q596 352 684 398" fill="none" stroke="{brow}" stroke-width="44" stroke-linecap="round"/>'
    return f'<g transform="translate(500 505) rotate({rot}) scale({sc}) translate(-500 -500)">{s}</g>'
def f2(white,ink,brow,bg,small=False):
    w=92 if small else 78
    s=f'<circle cx="330" cy="610" r="172" fill="{white}"/><circle cx="670" cy="610" r="172" fill="{white}"/>'
    s+=f'<circle cx="372" cy="600" r="86" fill="{ink}"/><circle cx="716" cy="572" r="86" fill="{ink}"/>'
    # heavy lid on left eye (field colour) + brow resting on it
    s+=f'<path d="M120 380 L560 380 L560 505 L120 478 Z" fill="{bg}"/>'
    s+=f'<path d="M172 462 L478 482" stroke="{brow}" stroke-width="{w}" stroke-linecap="round"/>'
    s+=f'<path d="M548 318 Q690 212 832 262" fill="none" stroke="{brow}" stroke-width="{w}" stroke-linecap="round"/>'
    return f'<g transform="translate(0 -30)">{s}</g>'
def f3(body,ink,bg,small=False):
    return f'<g transform="translate(500 500) scale(1.14) translate(-500 -480)">{fin1.f3(body,ink,bg,small)}</g>'
def f4(base,dome,well,hl,small=False):
    return f'<g transform="translate(500 500) scale(1.1) translate(-500 -520)">{fin1.f4(base,dome,well,hl,hl,True)}</g>'
