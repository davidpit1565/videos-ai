#!/usr/bin/env python3
"""Joke reel 'POV: your team is three AIs' (not a numbered episode; trial candidate Q3 of channel/queued-ideas.md).
Our own drawing, our own gag (three different answers), our own voice; premise inspired by a trend format (credited in the caption).
Reads voice/narration-cues.json (3 lines), writes hf/index.html, cues.json, sfx.json."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(H + "/voice/narration-cues.json"))
c1, c2, c3 = C[0], C[1], C[2]
D = round(c3["end"] + 1.3, 2)
TC = round(c1["end"] + 0.45, 2)          # the cut to the backyard
T = dict(D=D, TC=TC, l1=c1["start"], l1e=c1["end"], l2=c2["start"], l2e=c2["end"], l3=c3["start"], l3e=c3["end"],
         b1=round(c2["end"] + 0.3, 2), b2=round(c2["end"] + 0.85, 2), b3=round(c2["end"] + 1.4, 2))
INK = "#161412"
def eyes(): return '<circle cx="-22" cy="-398" r="7" fill="#161412"/><circle cx="22" cy="-398" r="7" fill="#161412"/>'
def person(pid, x, feet, s, head, arms_n, arms_a="", extra=""):
    return (f'<g transform="translate({x},{feet}) scale({s})"><g id="{pid}"><g class="sw" id="{pid}s">'
            f'<g stroke="{INK}" stroke-width="17" stroke-linecap="round" stroke-linejoin="round" fill="none">'
            f'<path d="M0 -190 L-46 0 M0 -190 L46 0 M0 -190 L0 -335"/>'
            f'<g class="an">{arms_n}</g><g class="aa" opacity="0">{arms_a}</g></g>{head}{extra}</g></g></g>')
NEUTRAL = '<path d="M0 -312 L-72 -235 M0 -312 L72 -235" stroke="#161412" stroke-width="17" stroke-linecap="round" fill="none"/>'
def head_plain(mouth='<path d="M-20 -372 Q0 -358 20 -372" stroke="#161412" stroke-width="7" fill="none" stroke-linecap="round" class="mouth"/>'):
    return f'<circle cx="0" cy="-392" r="62" fill="#fff" stroke="{INK}" stroke-width="17"/>{eyes()}{mouth}'
def head_logo(f):
    return (f'<circle cx="0" cy="-392" r="66" fill="#fff" stroke="{INK}" stroke-width="17"/>'
            f'<image href="assets/{f}" x="-40" y="-432" width="80" height="80" preserveAspectRatio="xMidYMid meet"/>')
PHONE = f'<g class="phone"><rect x="56" y="-262" width="34" height="58" rx="7" fill="#2b2a2e" stroke="{INK}" stroke-width="6" transform="rotate(14 70 -235)"/></g>'
ARMS_PHONE = '<path d="M0 -312 L-72 -235 M0 -312 L58 -262" stroke="#161412" stroke-width="17" stroke-linecap="round" fill="none"/>'
POSE_UP = '<path d="M0 -312 L-72 -235 M0 -312 L72 -378 L84 -440" stroke="#161412" stroke-width="17" stroke-linecap="round" stroke-linejoin="round" fill="none"/><circle cx="86" cy="-452" r="15" fill="#161412"/>'
POSE_X = '<path d="M0 -300 L-60 -255 L42 -288 M0 -300 L60 -255 L-42 -288" stroke="#161412" stroke-width="17" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
POSE_SHRUG = '<path d="M0 -312 L-88 -280 L-118 -335 M0 -312 L88 -280 L118 -335" stroke="#161412" stroke-width="17" stroke-linecap="round" stroke-linejoin="round" fill="none"/><circle cx="-120" cy="-344" r="12" fill="#161412"/><circle cx="120" cy="-344" r="12" fill="#161412"/>'
def bubble(bid, cx, y, lines, w=186):
    h = 76 + 54 * (len(lines) - 1)
    tx = "".join(f'<tspan x="{cx}" dy="{0 if i == 0 else 54}">{t}</tspan>' for i, t in enumerate(lines))
    return (f'<g id="{bid}" opacity="0"><path d="M{cx - 18} {y + h - 4} L{cx} {y + h + 34} L{cx + 20} {y + h - 4} Z" fill="#fff" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<rect x="{cx - w // 2}" y="{y}" width="{w}" height="{h}" rx="30" fill="#fff" stroke="{INK}" stroke-width="7"/>'
            f'<rect x="{cx - w // 2 + 5}" y="{y + h - 12}" width="{w - 10}" height="14" fill="#fff"/>'
            f'<text x="{cx}" y="{y + 56}" text-anchor="middle" font-size="40" font-weight="900" fill="{INK}" font-family="IDisp,Inter,Arial,sans-serif">{tx}</text></g>')
def title(tid, l1, l2):
    t = lambda y, s: f'<text x="540" y="{y}" text-anchor="middle" font-size="86" font-weight="900" font-family="IDisp,Inter,Arial,sans-serif" fill="{INK}" stroke="#fff" stroke-width="16" paint-order="stroke" stroke-linejoin="round">{s}</text>'
    return f'<g id="{tid}" opacity="0">{t(352, l1)}{t(464, l2)}</g>'
planks = "".join(f'<path d="M{x} 1250 L{x - 60 + (x % 3) * 20} 1920" stroke="#7a4d2a" stroke-width="3" opacity=".35"/>' for x in range(-100, 1180, 130))
fence = "".join(f'<rect x="{x}" y="770" width="92" height="330" rx="10" fill="{"#c9a36b" if (x // 100) % 2 else "#d4b07a"}" stroke="#8a6a3c" stroke-width="4"/>' for x in range(-20, 1100, 100))
grass = "".join(f'<path d="M{x} 1110 q6 -26 12 0 M{x + 40} 1160 q6 -30 14 0" stroke="#3f8a30" stroke-width="5" fill="none" stroke-linecap="round"/>' for x in range(10, 1080, 70))
SVG = f'''<svg id="stage" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
<defs>
<filter id="paint" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.011" numOctaves="2" seed="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="16"/></filter>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="2"/><feColorMatrix values="0 0 0 0 .3  0 0 0 0 .25  0 0 0 0 .2  0 0 0 .22 0"/></filter>
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3dcb8"/><stop offset="1" stop-color="#e2bd8c"/></linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b17c4d"/><stop offset="1" stop-color="#8b5c36"/></linearGradient>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8ecbff"/><stop offset="1" stop-color="#d9f1ff"/></linearGradient>
<linearGradient id="lawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#86c65f"/><stop offset="1" stop-color="#4c9638"/></linearGradient>
</defs>
<g id="room" filter="url(#paint)">
<rect x="-30" y="-30" width="1140" height="1300" fill="url(#wall)"/><rect x="-30" y="1240" width="1140" height="720" fill="url(#floor)"/>{planks}
<rect x="610" y="470" width="300" height="360" rx="14" fill="url(#sky)" stroke="#fff" stroke-width="22"/><path d="M760 470 V830 M610 650 H910" stroke="#fff" stroke-width="14"/>
<ellipse cx="700" cy="560" rx="60" ry="26" fill="#fff" opacity=".85"/>
<rect x="70" y="560" width="330" height="190" rx="10" fill="#f4efe4" stroke="#6b4a2c" stroke-width="16"/><image href="assets/chatgpt.svg" x="92" y="600" width="88" height="88"/><image href="assets/gemini.svg" x="196" y="600" width="88" height="88"/><image href="assets/claude.svg" x="300" y="600" width="88" height="88"/>
<ellipse cx="540" cy="1275" rx="380" ry="80" fill="#6f8fc2" opacity=".85"/>
<rect x="850" y="1060" width="110" height="150" rx="14" fill="#b4673f"/><g fill="#4f9a3a"><ellipse cx="905" cy="1010" rx="58" ry="80"/><ellipse cx="860" cy="1040" rx="40" ry="70"/><ellipse cx="950" cy="1040" rx="40" ry="70"/></g>
</g>
<g id="yard" filter="url(#paint)" opacity="0">
<rect x="-30" y="-30" width="1140" height="1130" fill="url(#sky)"/><ellipse cx="260" cy="470" rx="150" ry="46" fill="#fff" opacity=".9"/><ellipse cx="800" cy="560" rx="190" ry="54" fill="#fff" opacity=".9"/>
{fence}<rect x="-30" y="1070" width="1140" height="880" fill="url(#lawn)"/>{grass}
<rect x="110" y="590" width="46" height="260" fill="#7a5530"/><circle cx="130" cy="560" r="130" fill="#58a844"/><circle cx="60" cy="620" r="90" fill="#4e9a3c"/><circle cx="210" cy="620" r="90" fill="#62b14c"/>
</g>
<rect width="1080" height="1920" filter="url(#grain)" opacity=".55" pointer-events="none"/>
{title("t1", "POV: you ask", "your AI team")}{title("t2", "POV: your team", "is three AIs")}
{person("me", 540, 1275, 1.55, head_plain(), ARMS_PHONE, "", PHONE)}
{person("a1", 395, 1240, 1.2, head_logo("chatgpt.svg"), NEUTRAL, POSE_UP)}
{person("a2", 605, 1240, 1.2, head_logo("gemini.svg"), NEUTRAL, POSE_X)}
{person("a3", 815, 1240, 1.2, head_logo("claude.svg"), NEUTRAL, POSE_SHRUG)}
{bubble("q1", 395, 520, ["Yes!"], 188)}{bubble("q2", 605, 520, ["No."], 188)}{bubble("q3", 815, 490, ["It", "depends."], 188)}
</svg>'''
JS = '''
gsap.registerPlugin(CustomEase);
const T=__T__, D=T.D, ease=CustomEase.create("e","0.16,1,0.3,1"), soft=CustomEase.create("s","0.65,0,0.35,1");
const tl=gsap.timeline({paused:true});
gsap.set(['#a1','#a2','#a3'],{autoAlpha:0}); gsap.set('#t1',{opacity:0}); 
/* frame 0 is complete: the room, the figure with the phone, the headline */
tl.set('#t1',{opacity:1},0).from('#t1 text',{y:30,opacity:0,duration:.5,ease,stagger:.12,immediateRender:false},.05)
  .fromTo('#me',{y:0},{y:-10,duration:.7,yoyo:true,repeat:Math.ceil(T.TC/.7),ease:'sine.inOut'},0)
  .fromTo('#mes',{rotation:-2.5,transformOrigin:'50% 100%'},{rotation:2.5,duration:.9,yoyo:true,repeat:Math.ceil(T.TC/.9),ease:'sine.inOut'},0)
  .fromTo('#room',{scale:1,transformOrigin:'50% 55%'},{scale:1.04,duration:T.TC,ease:'sine.inOut'},0);
/* the cut: the room pushes out, the backyard pushes in, headline swaps */
tl.to('#t1',{opacity:0,duration:.18},T.TC-.12).to('#room',{scale:1.32,opacity:0,duration:.34,ease:'power2.in'},T.TC-.12)
  .fromTo('#yard',{scale:1.18,opacity:0,transformOrigin:'50% 60%'},{scale:1,opacity:1,duration:.45,ease},T.TC-.06)
  .set('#t2',{opacity:1},T.TC+.1).from('#t2 text',{y:30,opacity:0,duration:.5,ease,stagger:.12,immediateRender:false},T.TC+.1)
  .to('#me',{x:-245,y:0,scale:.82,transformOrigin:'50% 100%',duration:.5,ease:soft},T.TC-.05);
['#a1','#a2','#a3'].forEach((id,i)=>{ const at=T.TC+.25+i*.16;
  tl.fromTo(id,{autoAlpha:0,scale:.2,transformOrigin:'50% 100%'},{autoAlpha:1,scale:1,duration:.45,ease,immediateRender:false},at)
    .fromTo(id+'s',{rotation:-4,transformOrigin:'50% 100%'},{rotation:4,duration:.42+i*.04,yoyo:true,repeat:Math.ceil((D-at)/(.42+i*.04)),ease:'sine.inOut'},at+.4)
    .fromTo(id,{y:0},{y:-12,duration:.21+i*.02,yoyo:true,repeat:Math.ceil((D-at)/(.21+i*.02)),ease:'sine.inOut'},at+.4); });
/* the answers: three different ones */
[['#q1','#a1',T.b1],['#q2','#a2',T.b2],['#q3','#a3',T.b3]].forEach(([q,a,at])=>{
  tl.fromTo(q,{opacity:0,scale:.5,transformOrigin:'50% 100%'},{opacity:1,scale:1,duration:.4,ease,immediateRender:false},at)
    .to(a+' .an',{opacity:0,duration:.05},at).to(a+' .aa',{opacity:1,duration:.05},at); });
/* the figure on the left reacts at the end: shrinks a little */
tl.to('#me',{y:30,scale:1.08,duration:.7,ease:soft},T.l3-.1).to('#me .mouth',{opacity:0,duration:.1},T.l3);
tl.to({},{duration:.001},D-.001);
window.__timelines=window.__timelines||{}; window.__timelines["main"]=tl; tl.seek(0);
window.__reel={duration:D,seek:t=>{tl.seek(t)}};
'''.replace("__T__", json.dumps(T))
CDN = "https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/"
html = f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="{CDN}gsap.min.js"></script><script src="{CDN}CustomEase.min.js"></script>
<style>@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Black.otf");font-weight:900}}
*{{margin:0;padding:0}}html,body{{width:1080px;height:1920px;overflow:hidden;background:#e8d5b5}}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">{SVG}</div>
<script>{JS}</script></body></html>'''
open(H + "/hf/index.html", "w").write(html)
os.makedirs(H + "/out", exist_ok=True)
sfx = [dict(f="whoosh_b.ogg", t=round(T["TC"] - .2, 2), g=-10), dict(f="pop_a.ogg", t=round(T["TC"] + .25, 2), g=-14), dict(f="pop_b.ogg", t=round(T["TC"] + .41, 2), g=-14),
       dict(f="pop_a.ogg", t=round(T["TC"] + .57, 2), g=-14), dict(f="select.ogg", t=T["b1"], g=-11), dict(f="toggle.ogg", t=T["b2"], g=-11), dict(f="tick.ogg", t=T["b3"], g=-9),
       dict(f="impactsoft.ogg", t=T["l3"] - .05, g=-15)]
json.dump(sfx, open(H + "/sfx.json", "w"), indent=1)
json.dump(dict(lines=[dict(n=i + 1, text=c["line"], start=c["start"], end=c["end"]) for i, c in enumerate(C)], D=D), open(H + "/cues.json", "w"), indent=1)
print("D", D, T)
