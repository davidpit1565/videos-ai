from lib import *; from c1 import *; from txt import *
BR='BricolageGrotesque[opsz,wdth,wght].ttf'
def cyclops(fg,ink,white=PAPER):  # N1 A with eye counter
    s=f'<path d="M500 200 L800 800 L200 800 Z" fill="{fg}" stroke="{fg}" stroke-width="110" stroke-linejoin="round"/>'
    s+=f'<path d="M400 860 L500 700 L600 860 Z" fill="{ink}"/>'
    s+=f'<circle cx="500" cy="520" r="105" fill="{white}"/><circle cx="525" cy="495" r="55" fill="{ink}"/>'
    return s
def seal(fg,ink,inner):  # N2
    s=f'<circle cx="500" cy="500" r="430" fill="none" stroke="{fg}" stroke-width="26"/><circle cx="500" cy="500" r="270" fill="none" stroke="{fg}" stroke-width="14"/>'
    s+=f'<path d="{text_on_circle(BR,"ACTUALLY WORKS",100,500,500,312,0,(("wght",800),("wdth",100),("opsz",96)),10)}" fill="{fg}"/>'
    s+=f'<path d="{text_on_circle(BR,"TESTED",70,500,500,-378,180,(("wght",800),("wdth",100),("opsz",96)),14)}" fill="{fg}"/>'
    s+=f'<g transform="translate(500 510) scale(.42) translate(-500 -500)">{inner}</g>'
    return s
def typ(text,fg,ac,size=760):
    d,w=text_path(BR,text[0],size,0,0,(("wght",800),("wdth",100),("opsz",96)))
    d2,w2=text_path(BR,text[1],size,w+10,0,(("wght",800),("wdth",100),("opsz",96)))
    tot=w+10+w2
    return f'<g transform="translate({500-tot/2} 740)"><path d="{d}" fill="{fg}"/><path d="{d2}" fill="{ac}"/></g>'
def aplug(fg,ink,white=PAPER):  # N21 A whose legs are prongs
    s=f'<path d="M560 250 C640 120 760 150 740 40" fill="none" stroke="{ink}" stroke-width="50" stroke-linecap="round"/>'
    s+=rr(345,600,95,250,24,f'fill="{ink}"')+rr(560,600,95,250,24,f'fill="{ink}"')
    s+=f'<path d="M500 250 L720 640 L280 640 Z" fill="{fg}" stroke="{fg}" stroke-width="120" stroke-linejoin="round"/>'
    s+=eye(435,520,52,66,10,-8,white,ink,.6)+eye(565,520,52,66,10,-8,white,ink,.6)
    return s
def achar(fg,ink,white=PAPER,brow=None):  # A-ghost v2 bigger eyes + brow
    d='M500 200 L800 790 L650 670 L500 790 L350 670 L200 790 Z'
    s=f'<path d="{d}" fill="{fg}" stroke="{fg}" stroke-width="110" stroke-linejoin="round"/>'
    s+=eye(418,545,78,96,18,-14,white,ink,.58)+eye(582,545,78,96,18,-14,white,ink,.58)
    if brow: s+=f'<path d="M520 425 Q600 370 672 415" fill="none" stroke="{brow}" stroke-width="34" stroke-linecap="round"/><path d="M335 440 L480 452" stroke="{brow}" stroke-width="34" stroke-linecap="round"/>'
    return s
def eyes2(white,ink,brow):  # skeptic v2: strict geometry
    s=f'<circle cx="335" cy="590" r="165" fill="{white}"/><circle cx="665" cy="590" r="165" fill="{white}"/>'
    s+=f'<circle cx="385" cy="560" r="82" fill="{ink}"/><circle cx="715" cy="560" r="82" fill="{ink}"/>'
    s+=f'<path d="M180 385 L480 385" stroke="{brow}" stroke-width="74" stroke-linecap="round"/>'
    s+=f'<path d="M530 300 L800 215" stroke="{brow}" stroke-width="74" stroke-linecap="round"/>'
    return s
