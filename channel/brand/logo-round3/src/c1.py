from lib import *
import math
def outl(shapes, fill, ol, w):
    # merged silhouette with outer outline
    return f'<g fill="{ol}" stroke="{ol}" stroke-width="{w*2}" stroke-linejoin="round" stroke-linecap="round">{shapes}</g><g fill="{fill}">{shapes}</g>'
def rr(x,y,w,h,r,extra=''): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" {extra}/>'
def eye(cx,cy,rx,ry,px=0,py=0,white=PAPER,ink=INK,pr=0.55):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{white}"/><circle cx="{cx+px}" cy="{cy+py}" r="{rx*pr}" fill="{ink}"/>'

def plug(fg,ink,ac):   # C1 Pluggy
    body = rr(250,400,500,400,150)+rr(335,215,90,230,26)+rr(575,215,90,230,26)
    s = f'<path d="M500 790 C500 900 420 900 400 1010" fill="none" stroke="{ink}" stroke-width="56" stroke-linecap="round"/>'
    s += f'<g fill="{fg}">{body}</g>'
    s += f'<ellipse cx="410" cy="565" rx="40" ry="56" fill="{ink}"/><ellipse cx="590" cy="565" rx="40" ry="56" fill="{ink}"/>'
    s += f'<path d="M400 665 Q500 760 600 665" fill="none" stroke="{ink}" stroke-width="34" stroke-linecap="round"/>'
    return s
def skeptic(white,ink):  # C2 raised eyebrow
    s = eye(325,570,150,185,35,-30,white,ink)+eye(675,570,150,185,35,-30,white,ink)
    s += f'<path d="M185 345 L455 375" stroke="{ink}" stroke-width="64" stroke-linecap="round"/>'
    s += f'<path d="M545 290 Q690 150 835 250" fill="none" stroke="{ink}" stroke-width="64" stroke-linecap="round"/>'
    return s
def aghost(fg,ink,white=PAPER):  # C3 A character with W feet
    d = 'M500 190 L790 800 L645 690 L500 800 L355 690 L210 800 Z'
    s = f'<path d="{d}" fill="{fg}" stroke="{fg}" stroke-width="90" stroke-linejoin="round"/>'
    s += eye(425,520,58,72,12,-8,white,ink,0.6)+eye(575,520,58,72,12,-8,white,ink,0.6)
    return s
def marker(a,b,ring):  # C4 crash-test marker
    R=330
    s = f'<g transform="rotate(-18 500 500)"><circle cx="500" cy="500" r="{R+50}" fill="{ring}"/><circle cx="500" cy="500" r="{R}" fill="{a}"/>'
    s += f'<path d="M500 500 L500 {500-R} A{R} {R} 0 0 1 {500+R} 500 Z" fill="{b}"/><path d="M500 500 L500 {500+R} A{R} {R} 0 0 1 {500-R} 500 Z" fill="{b}"/></g>'
    return s
def dummy(head,ink,a,b):  # C4b test-dummy head
    s = rr(250,200,500,620,230,f'fill="{head}"')
    s += f'<rect x="400" y="790" width="200" height="260" fill="{head}"/><rect x="330" y="880" width="340" height="50" rx="25" fill="{ink}"/>'
    R=105; cx,cy=500,360
    s += f'<circle cx="{cx}" cy="{cy}" r="{R+22}" fill="{ink}"/><circle cx="{cx}" cy="{cy}" r="{R}" fill="{a}"/><path d="M{cx} {cy} L{cx} {cy-R} A{R} {R} 0 0 1 {cx+R} {cy} Z" fill="{b}"/><path d="M{cx} {cy} L{cx} {cy+R} A{R} {R} 0 0 1 {cx-R} {cy} Z" fill="{b}"/>'
    s += f'<circle cx="400" cy="600" r="42" fill="{ink}"/><circle cx="600" cy="600" r="42" fill="{ink}"/><path d="M430 710 Q500 760 570 710" fill="none" stroke="{ink}" stroke-width="30" stroke-linecap="round"/>'
    return s
def finger(fg,ink,cuff):  # C5 "actually" raised finger
    sh = rr(425,150,125,480,62)+rr(330,500,400,330,95)+rr(535,455,105,200,52)+rr(628,480,100,200,50)+f'<rect x="255" y="500" width="130" height="250" rx="62" transform="rotate(-28 320 740)"/>'
    s = f'<rect x="350" y="800" width="360" height="300" fill="{cuff}" stroke="{ink}" stroke-width="30"/>'
    s += outl(sh,fg,ink,30)
    s += f'<path d="M550 600 Q590 650 550 700 M640 610 Q670 650 640 700" fill="none" stroke="{ink}" stroke-width="26" stroke-linecap="round"/>'
    return s
def button(base,dome,ink):  # C6 big button
    s = f'<path d="M150 610 A350 130 0 0 1 850 610 L850 720 A350 130 0 0 1 150 720 Z" fill="{base}"/>'
    s += f'<ellipse cx="500" cy="610" rx="350" ry="130" fill="{base}"/><ellipse cx="500" cy="610" rx="290" ry="100" fill="{ink}"/>'
    s += f'<path d="M240 590 L240 470 A260 190 0 0 1 760 470 L760 590 A260 90 0 0 1 240 590 Z" fill="{dome}"/>'
    s += f'<path d="M330 400 A190 120 0 0 1 480 315" fill="none" stroke="{PAPER}" stroke-width="34" stroke-linecap="round" opacity=".9"/>'
    return s
def aw(fg,bg):  # C7 triangle A containing W
    s = f'<path d="M500 190 L830 790 L170 790 Z" fill="{fg}" stroke="{fg}" stroke-width="100" stroke-linejoin="round"/>'
    s += f'<path d="M330 560 L415 700 L500 580 L585 700 L670 560" fill="none" stroke="{bg}" stroke-width="72" stroke-linejoin="miter" stroke-linecap="butt"/>'
    return s
def bulb(y,ink,base):  # C9
    s = ''.join(f'<path d="M500 500 L{500+470*math.cos(a):.0f} {430+470*math.sin(a):.0f}" stroke="{y}" stroke-width="40" stroke-linecap="round"/>' for a in [math.radians(t) for t in (-150,-120,-90,-60,-30)])
    s += f'<circle cx="500" cy="450" r="250" fill="{y}" stroke="{ink}" stroke-width="0"/><rect x="390" y="640" width="220" height="90" fill="{y}"/>'
    s += rr(385,715,230,55,20,f'fill="{base}"')+rr(400,780,200,50,20,f'fill="{base}"')+rr(440,838,120,40,20,f'fill="{base}"')
    s += f'<circle cx="420" cy="440" r="34" fill="{ink}"/><circle cx="580" cy="440" r="34" fill="{ink}"/><path d="M420 530 Q500 600 580 530" fill="none" stroke="{ink}" stroke-width="30" stroke-linecap="round"/>'
    return s
def power(fg,ac):  # C10 power + !
    R=285; a=math.radians(38)
    x1=500-R*math.sin(a); y1=540-R*math.cos(a); x2=500+R*math.sin(a)
    s = f'<path d="M{x1:.0f} {y1:.0f} A{R} {R} 0 1 0 {x2:.0f} {y1:.0f}" fill="none" stroke="{fg}" stroke-width="100" stroke-linecap="round"/>'
    s += rr(450,130,100,400,50,f'fill="{ac}"')+f'<circle cx="500" cy="640" r="62" fill="{ac}"/>'
    return s
def lever(plate,arm,knob,ink):  # C12
    s = rr(300,330,400,520,90,f'fill="{plate}"')+rr(455,420,90,340,45,f'fill="{ink}"')
    s += f'<path d="M500 640 L650 300" stroke="{arm}" stroke-width="80" stroke-linecap="round"/><circle cx="665" cy="265" r="105" fill="{knob}"/><circle cx="500" cy="640" r="60" fill="{arm}"/>'
    return s
def thumb(fg,ink,cuff):  # C13
    sh = rr(330,440,400,330,95)+f'<rect x="330" y="150" width="140" height="400" rx="70" transform="rotate(14 400 500)"/>'
    s = f'<rect x="190" y="470" width="150" height="330" fill="{cuff}" stroke="{ink}" stroke-width="30"/>'+outl(sh,fg,ink,30)
    s += f'<path d="M520 520 L730 520 M520 600 L730 600 M520 680 L730 680" stroke="{ink}" stroke-width="26" stroke-linecap="round"/>'
    return s
def click(a,b):  # C14 two halves that fit
    s = f'<g transform="rotate(20 500 500)"><circle cx="500" cy="500" r="340" fill="{a}"/><path d="M500 160 A340 340 0 0 1 500 840 L500 610 A110 110 0 1 1 500 390 Z" fill="{b}"/></g>'
    return s
