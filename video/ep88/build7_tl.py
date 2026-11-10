
# ------------------------------------------------------------ timeline (generated)
D_ = D
rnd = _r.Random(7)
def at(t): return tt(t)

def slam(sel, t, dx=0, dy=0, rot=0, s0=1.35, dur=.3, typed=False):
    """text-safe entrance: torn-paper wipe (clip reveal) at the final position + tiny slam; the text box never leaves the safe area"""
    wid, hei = REG.get(sel[1:], (900, 130))
    sx = min(s0, 1.06); ox = max(-40, min(40, dx * .2)); oy = max(-18, min(18, dy * .15))
    L = [-60, -60, -60, -60]
    if dy < 0 and abs(dy) >= abs(dx): L[2] = hei + 60
    elif dy > 0 and abs(dy) > abs(dx): L[0] = hei + 60
    elif dx > 0: L[3] = wid + 60
    else: L[1] = wid + 60
    st = " ".join(f"{v}px" for v in L)
    js(f"tl.fromTo('{sel}',{{clipPath:'inset({st})',x:{ox},y:{oy},scale:{sx},rotation:'+={rot * .5}'}},{{clipPath:'inset(-60px -60px -60px -60px)',x:0,y:0,scale:1,rotation:'-={rot * .5}',duration:{dur},ease:'expo.out',transformOrigin:'50% 50%'}},{at(t)});")

def settle(sel, t, dx=0, dy=0, rot=0, s0=1.05, dur=.4):
    js(f"tl.fromTo('{sel}',{{x:{dx},y:{dy},scale:{s0},rotation:'+={rot}'}},{{x:0,y:0,scale:1,rotation:'-={rot}',duration:{dur},ease:'expo.out',transformOrigin:'50% 50%'}},{at(t)});")

def drop(sel, t, dy=-420, dx=0, s0=1, dur=.5, ease="back.out(1.25)", rot=0):
    js(f"tl.fromTo('{sel}',{{y:{dy},x:{dx},scale:{s0},opacity:1,rotation:'+={rot}'}},{{y:0,x:0,scale:1,rotation:'-={rot}',duration:{dur},ease:'{ease}',transformOrigin:'50% 50%'}},{at(t)});")

def tapeslap(sel, t):
    js(f"tl.fromTo('{sel}',{{scale:1.7,opacity:0}},{{scale:1,opacity:.86,duration:.14,ease:'power3.in'}},{at(t)});")

def thump(sel, t, s0=2.1, op=.9, dur=.16):
    js(f"tl.fromTo('{sel}',{{scale:{s0},opacity:0}},{{scale:1,opacity:{op},duration:{dur},ease:'power4.in',transformOrigin:'50% 50%'}},{at(t)});")

def fly(i, t, y0, y1, dirn=1, dur=.7, rot0=-25, rot1=15, s=1):
    x0, x1 = (1250, -420) if dirn > 0 else (-420, 1250)
    js(f"tl.fromTo('#fl{i}',{{x:{x0},y:{y0},rotation:{rot0},opacity:1,scale:{s}}},{{x:{x1},y:{y1},rotation:{rot1},duration:{dur},ease:'power1.inOut'}},{at(t)});")
    js(f"tl.set('#fl{i}',{{opacity:0}},{at(t + dur + .02)});")
    sfx("whoosh_c.ogg", t + .05, -9)

def fgcross(i, t, y, dur=1.0, dirn=1):
    x0, x1 = (1300, -700) if dirn > 0 else (-700, 1300)
    js(f"tl.fromTo('#fg{i}',{{x:{x0},y:{y},rotation:-8,opacity:1}},{{x:{x1},y:{y + 40},rotation:10,duration:{dur},ease:'sine.inOut'}},{at(t)});")
    js(f"tl.set('#fg{i}',{{opacity:0}},{at(t + dur + .02)});")

def swap(old, new, t, k):
    """newsprint sheet sweeps over the whole frame (alternating direction); scenes swap while it covers the picture (no blank dips)"""
    sh = "sheetA" if k % 2 == 0 else "sheetB"
    r = (-2.5, 2.0, -1.5)[k % 3]
    xa, xb = (1160, -1560) if k % 2 == 0 else (-1560, 1160)
    js(f"tl.fromTo('#{sh}',{{x:{xa},y:{[-80, -140, -30][k % 3]},rotation:{r},opacity:1}},{{x:{xb},y:{[-120, -60, -100][k % 3]},rotation:{-r},duration:.22,ease:'power2.inOut'}},{at(t - .11)});")
    js(f"tl.set('#{sh}',{{opacity:0}},{at(t + .13)});")
    if old: js(f"tl.set('#{old}',{{autoAlpha:0}},{at(t - .02)});")
    js(f"tl.set('#{new}',{{autoAlpha:1}},{at(t - .01)});")
    sfx(("whoosh_b.ogg", "whoosh_a.ogg")[k % 2], t - .13, -2)

def usweep(ush, t, k, mid=None):
    """sweep UNDER the strips: the strips stay readable while the picture behind them changes. mid = callable(t_cover) schedules the swap"""
    xa, xb = (1160, -1560) if k % 2 == 0 else (-1560, 1160)
    r = (-2.0, 1.6)[k % 2]
    js(f"tl.fromTo('#{ush}',{{x:{xa},y:-100,rotation:{r},opacity:1}},{{x:{xb},y:-80,rotation:{-r},duration:.24,ease:'power2.inOut'}},{at(t)});")
    js(f"tl.set('#{ush}',{{opacity:0}},{at(t + .26)});")
    sfx("whoosh_a.ogg" if k % 2 == 0 else "whoosh_b.ogg", t, -2)
    if mid: mid(t + .12)

def cam(cid, t0, t1, s0=1.0, s1=1.025, r0=0, r1=0, x0=0, x1=0, y0=0, y1=0, org="540px 760px"):
    js(f"tl.fromTo('#{cid}',{{scale:{s0},rotation:{r0},x:{x0},y:{y0}}},{{scale:{s1},rotation:{r1},x:{x1},y:{y1},duration:{max(.3, t1 - t0):.3f},ease:'sine.inOut',transformOrigin:'{org}'}},{at(t0)});")

def scraps(sid, s, e, final=False, entrance=True):
    """3 depth layers: far/mid/near drift at different speeds; entrance = every scrap slaps down (scale 1.14 -> 1) a few frames apart"""
    spd = {"far": 14, "mid": 30, "near": 64}
    for i, (eid, layer, x, y, rot) in enumerate(SSET[sid]):
        dx = rnd.choice((-1, 1)) * spd[layer] * rnd.uniform(.6, 1.0); dy = rnd.choice((-1, 1)) * spd[layer] * rnd.uniform(.3, .8); dr = rnd.uniform(.6, 1.6) * rnd.choice((-1, 1))
        dur = (e - s) + .6
        if final:
            js(f"tl.fromTo('#{eid}',{{x:{dx:.1f},y:{dy:.1f},rotation:{rot + dr:.2f}}},{{x:{-dx:.1f},y:{-dy:.1f},rotation:{rot - dr:.2f},duration:{dur:.3f},ease:'sine.out'}},{at(s)});")
        else:
            js(f"tl.fromTo('#{eid}',{{x:{-dx:.1f},y:{-dy:.1f},rotation:{rot - dr:.2f}}},{{x:{dx:.1f},y:{dy:.1f},rotation:{rot + dr:.2f},duration:{dur:.3f},ease:'none'}},{at(s)});")
        if entrance and not final and sid != "s1":
            js(f"tl.fromTo('#{eid}',{{scale:1.14}},{{scale:1,duration:.42,ease:'expo.out',transformOrigin:'50% 50%'}},{at(s + .02 + i * .045)});")
            if i % 3 == 0: sfx("tick.ogg", s + .04 + i * .045, -8)

# --- global
js(f"tl.fromTo('#world',{{scale:1,rotation:-.25}},{{scale:1.014,rotation:.25,duration:{D_ / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1,transformOrigin:'540px 960px'}},0);")
js(f"tl.fromTo('#bgimg',{{x:0}},{{x:-300,duration:{D_ / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1}},0);")
g_t = 0.0
while g_t < D_:
    js(f"tl.set('#grain',{{x:{rnd.randint(-30, 30)},y:{rnd.randint(-30, 30)}}},{at(g_t)});"); g_t += 1 / 12

# --- HOOK (frame 0 is settled and readable: only small settles, nothing fades in)
t0 = 0.0
settle("#hA", t0, dx=-26, rot=.8, s0=1.03); settle("#hB", t0 + .05, dx=26, rot=-.8, s0=1.03)
js(f"tl.fromTo('#fbs',{{scale:.8,rotation:-30}},{{scale:1,rotation:-8,duration:.5,ease:'back.out(2.2)'}},{at(t0)});")
nl = 11
for k in range(nl):
    js(f"tl.fromTo('#rl{k}',{{scale:1.16,rotation:'+={(-1) ** k * 5}'}},{{scale:1,rotation:'-={(-1) ** k * 5}',duration:.42,ease:'expo.out',transformOrigin:'50% 50%'}},{at(t0 + .03 * k)});")
    js(f"tl.to('#rl{k}',{{y:{(-1) ** k * 5},duration:.9,ease:'sine.inOut',yoyo:true,repeat:2}},{at(t0 + .6 + .05 * k)});")
for sel, dy0, rr_ in (("pa", 40, -8), ("pc", 46, 8), ("pb", 30, -3)):
    drop(f"#{sel}", t0, dy=dy0, dur=.5, ease="power3.out", rot=rr_)
for j, tp_ in enumerate(("pa", "pb", "pc")):
    tapeslap(f"#{tp_}tp", t0 + .38 + j * .09); sfx("tick.ogg", t0 + .38 + j * .09, -4)
thump("#stH", t0 + .7, 1.8, .8, .16); sfx("pop_a.ogg", t0 + .72, -4)
sfx("impactpunch.ogg", t0 + .04, 0); sfx("subhit.ogg", t0 + .04, -3); sfx("whoosh_a.ogg", t0, -2)
js(f"tl.set('#hcam',{{x:0}},0);")
# hero swap under a sweep (strips + ransom row stay readable)
sw = W(1, 5) - .25
def hero_swap(tc):
    js(f"tl.set(['#pa','#pb','#pc'],{{autoAlpha:0}},{at(tc)});")
    for nm in ("pax", "pbx", "pcx"):
        js(f"tl.set('#{nm}',{{autoAlpha:1}},{at(tc)});")
    for j, nm in enumerate(("pax", "pbx", "pcx")):
        js(f"tl.fromTo('#{nm}',{{scale:1.12,rotation:'+={(-6, 4, 6)[j]}'}},{{scale:1,rotation:'-={(-6, 4, 6)[j]}',duration:.4,ease:'expo.out',transformOrigin:'50% 50%'}},{at(tc + .02 + j * .05)});")
        tapeslap(f"#{nm}tp", tc + .15 + j * .07)
    sfx("impactsoft.ogg", tc + .08, -3)
js(f"tl.set(['#pax','#pbx','#pcx'],{{autoAlpha:0}},0);")
usweep("ush0", sw, 0, hero_swap)
thump("#stHx", W(1, 6) + .02, 2.1, .92, .18); sfx("impactpunch.ogg", W(1, 6) + .04, -2)
for j in range(2):
    js(f"tl.to('#hA',{{y:-5,duration:.6,ease:'sine.inOut',yoyo:true,repeat:1}},{at(.7 + j * 1.3)});")
fly(0, .35, 1380, 1480, 1, .8); fly(1, .95, 1600, 1520, -1, .8, 20, -10)
fgcross(0, 1.7, 1420, 1.0, 1); fly(2, 2.05, 1330, 1450, 1, .7)
cam("hcam", 0, T["s2"] + .1, 1.0, 1.03, -.4, .5)
scraps("s1", 0, T["s2"] + .1, entrance=False)
sfx("click_a.ogg", T["slam1"], -4)

# --- S2
s = T["s2"]; swap("s1", "s2", s, 0); scraps("s2", s, T["s3"])
slam("#t2", s + .02, dx=300, rot=2, s0=1.1, dur=.38); sfx("impactsoft.ogg", s + .1, -6)
slam("#dlg2", s + .1, dy=300, rot=-1, s0=1.06, dur=.45); sfx("pop_b.ogg", s + .5, -3)
for j, d in enumerate(("d1", "d2", "d3")):
    drop(f"#{d}", s + .3 + j * .12, dy=-340, dx=(-40, 0, 40)[j], dur=.4, ease="power3.out", rot=(-12, 6, 14)[j]); sfx("tick.ogg", s + .6 + j * .12, -3)
slam("#nb", s + .62, dx=-320, s0=1.0, dur=.3)
slam("#b2", s + .74, dx=0, dy=-40, rot=-3, s0=1.06, dur=.34); sfx("impactsoft.ogg", s + .85, -5)
js(f"tl.fromTo('#fing',{{opacity:0,y:60}},{{opacity:1,y:0,duration:.4,ease:'power2.out'}},{at(T['tapAllow'] - .4)});")
js(f"tl.to('#b2',{{scale:.93,duration:.14,ease:'sine.inOut',transformOrigin:'50% 50%'}},{at(T['tapAllow'])});")
js(f"tl.fromTo('#ring',{{opacity:.95,scale:.5}},{{opacity:0,scale:2.6,duration:.7,ease:'power2.out'}},{at(T['tapAllow'] + .02)});")
js(f"tl.to('#b2',{{scale:1,duration:.3,ease:'sine.inOut'}},{at(T['tapAllow'] + .14)});")
js(f"tl.to('#fing',{{opacity:0,duration:.3}},{at(T['tapAllow'] + .45)});")
sfx("select.ogg", T["tapAllow"], 0); sfx("pop_b.ogg", T["tapAllow"] + .06, -3)
fly(3, s + .5, 1370, 1300, -1, .8, 15, -20); fgcross(1, s + 1.3, 1500, 1.1, -1); fly(4, s + 1.8, 1560, 1640, 1, .7)
cam("c2", s, T["s3"], 1.0, 1.02, .6, -.3, 0, -12)
js("tl.set('#ss_s2b',{autoAlpha:0},0);")
def s2_swap(tc):
    js(f"tl.set('#ss_s2',{{autoAlpha:0}},{at(tc)});"); js(f"tl.set('#ss_s2b',{{autoAlpha:1}},{at(tc)});"); sfx("impactsoft.ogg", tc + .05, -5)
usweep("ush2", T["tapAllow"] + .55, 1, s2_swap); scraps("s2b", T["tapAllow"] + .7, T["s3"])

# --- S3
s = T["s3"]; swap("s2", "s3", s, 1); scraps("s3", s, T["p1"])
slam("#t3a", s + .02, dx=-300, rot=1, s0=1.1, dur=.38)
slam("#t3b", s + .18, dx=300, rot=-1, s0=1.1, dur=.38)
slam("#tgp", s + .3, dy=420, rot=1, s0=1.06, dur=.5); sfx("pop_b.ogg", s + .6, -3)
slam("#tlab", s + .55, dy=140, s0=1.0, dur=.35); sfx("tick.ogg", s + .7, -3)
js(f"tl.to('#bigtg i',{{x:-18,duration:.35,ease:'sine.inOut',yoyo:true,repeat:3}},{at(s + .9)});")
fly(5, s + .45, 1400, 1330, 1, .75); fgcross(2, s + .9, 1520, 1.0, 1)
sfx("toggle.ogg", s + .3, -8)
cam("c3", s, T["p1"], 1.03, 1.0, -.4, .3, 0, 0, 0, 0, "540px 900px")

# --- steps
steps = [("p1", "p2", "pc1", "pn1", ["sl10", "sl11"], "ui1", "mk1", "tapr1"), ("p2", "p3", "pc2", "pn2", ["sl20", "sl21"], "ui2", "mk2", "tapr2"),
         ("p3", "p4", "pc3", "pn3", ["sl30"], "ui3", "mk3", "tapr3"), ("p4", "s5", "pc4", "pn4", ["sl40", "sl41", "sl42"], "ui4", "mk4", "tapr4")]
CAMS = [dict(s0=1.0, s1=1.03, r0=.5, r1=-.4, org="300px 600px"), dict(s0=1.0, s1=1.025, r0=-.3, r1=.4, x0=10, x1=-10, y0=0, y1=-12), dict(s0=1.03, s1=1.0, r0=.4, r1=-.2), dict(s0=1.0, s1=1.03, x0=-12, x1=12)]
prev = "s3"
for i, (a, b, cm, pn, labs, ui, mk, tr) in enumerate(steps):
    s = T[a]; e = T[b]
    swap(prev, a, s, 2 + i); prev = a; scraps(a, s, e + .1)
    js(f"tl.fromTo('#{pn}',{{scale:1.25,opacity:0,x:-30}},{{scale:1,opacity:.95,x:0,duration:.34,ease:'expo.out',transformOrigin:'30% 50%'}},{at(s + .02)});")
    for j, l in enumerate(labs): slam("#" + l, s + .08 + j * .07, dx=(220, -220)[i % 2], rot=-1, s0=1.0, dur=.3)
    slam("#" + ui, s + .12, dy=90, rot=1, s0=1.05, dur=.4)
    js(f"tl.fromTo('#{mk} path',{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.42,ease:'power2.inOut'}},{at(s + .5)});")
    js(f"tl.fromTo('#{tr}',{{opacity:.9,scale:.4}},{{opacity:0,scale:2.2,duration:.5,ease:'power2.out'}},{at(s + .5)});")
    sfx("tick.ogg", s + .5, -1); sfx("pop_b.ogg", s + .14, -6)
    if i % 2 == 0: fly(i, s + .25, 1360 + i * 20, 1420, 1, .7)
    else: fgcross(i % 3, s + .3, 1480, .9, -1)
    cam(cm, s, e + .1, **CAMS[i])
    if i == 3: js(f"tl.to('#{ui}',{{y:-6,duration:.9,ease:'sine.inOut'}},{at(s + .7)});")

# --- S5 OFF (the proof)
s = T["s5"]; swap("p4", "s5", s, 6); scraps("s5", s, T["s6"])
slam("#t5", s + .02, dy=-130, rot=-2, s0=1.1, dur=.36)
slam("#tgp2", s + .1, dy=360, rot=1, s0=1.06, dur=.5)
fl = T["flip"]
js(f"tl.to('#bigtg2 i',{{right:384,duration:.34,ease:'power3.inOut'}},{at(fl)});")
js(f"tl.to('#bigtg2',{{backgroundColor:'#9BE22E',duration:.34,ease:'power3.inOut'}},{at(fl)});")
js(f"tl.fromTo('#bigtg2',{{boxShadow:'0 0 0 0 rgba(155,226,46,.9)'}},{{boxShadow:'0 0 0 50px rgba(155,226,46,0)',duration:.6,ease:'power2.out',immediateRender:false}},{at(fl + .3)});")
js(f"tl.fromTo('#burst',{{opacity:.8,scale:.35}},{{opacity:0,scale:2.4,duration:.6,ease:'power2.out',transformOrigin:'50% 50%'}},{at(fl + .25)});")
for j in range(3):
    js(f"tl.set('#scr{j}',{{opacity:1}},{at(fl + .34 + j * .07)});"); js(f"tl.set('#scr{j}',{{opacity:0}},{at(fl + .34 + j * .07 + .07)});")
js(f"tl.fromTo('#offf',{{scale:1.5,opacity:0}},{{scale:1,opacity:1,duration:.34,ease:'expo.out',transformOrigin:'50% 50%'}},{at(fl + .55)});")
js(f"tl.to('#tgp2',{{y:-8,duration:{T['s6'] - T['s5']:.3f},ease:'sine.inOut'}},{at(s + .6)});")
sfx("toggle.ogg", fl + .22, 0); sfx("ding.ogg", fl + .32, -2); sfx("impactsoft.ogg", fl + .38, -5); sfx("pop_a.ogg", fl + .6, -3)
fly(0, fl + .1, 1300, 1560, 1, .6, -10, 30); fly(1, fl + .15, 1300, 1620, -1, .6, 10, -30); fly(2, fl + .2, 1320, 1700, 1, .7)
cam("c5", s, T["s6"], 1.0, 1.035, -.3, .4, 0, 0, 0, 0, "540px 880px")

# --- S6 Meta
s = T["s6"]; swap("s5", "s6", s, 7); scraps("s6", s, T["s7"])
slam("#t6a", s + .02, dy=-100, rot=2, s0=1.1, dur=.34)
slam("#pin6", s + .1, dy=60, rot=1, s0=1.06, dur=.42); sfx("pop_b.ogg", s + .45, -3)
js(f"tl.fromTo('#optin',{{scale:1.015}},{{scale:1,duration:.4,ease:'expo.out',transformOrigin:'50% 50%'}},{at(s + .3)});")
slam("#t6b", s + .6, dx=300, rot=-1, s0=1.0, dur=.34); sfx("impactsoft.ogg", s + .65, -6)
slam("#t6c", s + 1.0, dy=60, s0=1.0, dur=.3)
sfx("pop_a.ogg", W(4, 2), -3)
fly(3, s + .4, 1380, 1480, 1, .8); fgcross(0, s + .9, 1540, 1.1, -1); fly(4, s + 1.5, 1330, 1450, -1, .7, 10, -20)
cam("c6", s, T["s7"], 1.02, 1.0, -.5, .5)
js("tl.set('#ss_s6b',{autoAlpha:0},0);")
def s6_swap(tc):
    js(f"tl.set('#ss_s6',{{autoAlpha:0}},{at(tc)});"); js(f"tl.set('#ss_s6b',{{autoAlpha:1}},{at(tc)});")
    sfx("impactsoft.ogg", tc + .05, -5)
usweep("ush1", s + 1.55, 1, s6_swap); scraps("s6b", s + 1.7, T["s7"])

# --- S7 send
s = T["s7"]; swap("s6", "s7", s, 8); scraps("s7", s, T["end"])
slam("#t7a", s + .02, dx=-280, rot=1, s0=1.1, dur=.34); slam("#t7b", s + .16, dx=280, rot=-1, s0=1.1, dur=.34)
slam("#outb", s + .3, dx=300, rot=3, s0=1.06, dur=.4); sfx("pop_b.ogg", s + .65, -3)
js(f"tl.fromTo('#mav',{{opacity:0,scale:.5}},{{opacity:1,scale:1,duration:.38,ease:'back.out(2)'}},{at(s + 1.0)});")
js(f"tl.fromTo('#dots2',{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:.3,ease:'power2.out'}},{at(s + 1.1)});")
js(f"tl.to('#dots2 i',{{y:-10,duration:.26,ease:'sine.inOut',yoyo:true,repeat:3,stagger:.09}},{at(s + 1.2)});")
js(f"tl.to('#dots2',{{opacity:0,duration:.16}},{at(s + 1.72)});")
for k in (1, 2, 3):
    slam(f"#al{k}", s + 1.78 + (k - 1) * .26, dy=-70, rot=(4, -4, 4)[k - 1], s0=1.06, dur=.3); sfx("pop_b.ogg", s + 1.9 + (k - 1) * .26, -3)
sfx("riser.ogg", s - 2.2, -7); sfx("ding.ogg", E(5) - .1, -6)
fly(5, s + .5, 1350, 1440, 1, .8); fgcross(1, s + 1.2, 1520, 1.0, 1)
cam("c7", s, T["end"], 1.0, 1.03, -.3, .3, 12, -12)
js("tl.set('#ss_s7b',{autoAlpha:0},0);")
def s7_swap(tc):
    js(f"tl.set('#ss_s7',{{autoAlpha:0}},{at(tc)});"); js(f"tl.set('#ss_s7b',{{autoAlpha:1}},{at(tc)});"); sfx("impactsoft.ogg", tc + .05, -5)
usweep("ush3", s + .62, 0, s7_swap); scraps("s7b", s + .77, T["end"])

# --- loop back to frame 0
swap("s7", "sH", T["loop"], 9)
sfx("whoosh_c.ogg", T["loop"] - .1, -5)
scraps("sH", T["loop"], D_, final=True)
js(f"tl.fromTo('#hcamH',{{scale:1.03,rotation:.5}},{{scale:1,rotation:0,duration:{D_ - T['loop']:.3f},ease:'sine.out',transformOrigin:'540px 760px'}},{at(T['loop'])});")
js(f"tl.set('#sH',{{autoAlpha:0}},0);")

JS = "const D2=" + str(D_) + ";\n" + "\n".join(J)
json.dump([dict(f=f, t=t, g=g) for f, t, g in SFX if t < D_ and t >= 0], open(H + "/sfx7.json", "w"), indent=1)

html = open(H + "/shell8.html").read()
html = (html.replace("__STYLES__", styles).replace("__MARKUP__", markup).replace("__CHROME__", "").replace("__SCRIPTS__", "")
        .replace("__D__", str(D_)).replace("__CUES__", json.dumps(dict(lines=lines, D=D_)))
        .replace("__CALLS__", JS).replace("__NSC__", "1"))
html = re.sub(r'<div class="abs clip" id="gd".*?</div>', '', html, flags=re.S)
os.makedirs(H + "/hf", exist_ok=True)
open(H + "/hf/index.html", "w").write(html)
print("D=", D_, [(l["n"], l["start"], l["end"]) for l in lines])
print("scenes", {k: round(float(v), 2) for k, v in B.items()}, "js lines", len(J), "sfx", len(SFX))
if "--render" in sys.argv:
    name = sys.argv[sys.argv.index("--render") + 1]
    env = dict(os.environ, HYPERFRAMES_NO_TELEMETRY="1", DO_NOT_TRACK="1")
    r = subprocess.run(["npx", "--no-install", "hyperframes", "render", "-o", f"{H}/out/{name}.mp4", "--format", "mp4", "--quiet"],
                       cwd=H + "/hf", env=env, capture_output=True, text=True, timeout=3000)
    print(r.stdout[-400:], r.stderr[-800:])
