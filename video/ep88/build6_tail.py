# ---- round 6: markup + generated timeline. Real scans (CC0/PD), torn pieces with fibre rim + baked shadow (p6lib), halftone photos, newsprint sheet transitions.
import random as _r
sys.path.insert(0, H)
import p6lib
PAD = p6lib.PAD
YEL, BLK, CRM, WHT = (242, 194, 48), (23, 19, 15), (255, 255, 255), (251, 246, 234)
J = []          # generated javascript lines
SFX = []        # (file, time, gain)
def js(s): J.append(s)
def sfx(f, t, g=0): SFX.append((f, round(t, 3), g))
def tt(t): return f"{t:.3f}"

def pimg(w, h, kind, color, seed, amp=7, rim=True, shadow=True, step=26):
    rel, pad = p6lib.make_piece(w, h, kind, color, seed, amp, rim, shadow, step)
    return f'<img class="pbg" src="{rel}" style="left:{-pad}px;top:{-pad}px;width:{w + 2 * pad}px;height:{h + 2 * pad}px">'

REG = {}
def P(inner, id, x, y, w, h, rot=0, kind="news", color=CRM, seed=1, amp=7, z=3, cls="", extra=""):
    REG[id] = (w, h)
    return (f'<div class="pcw {cls}" id="{id}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:{z}">'
            f'{pimg(w, h, kind, color, seed, amp)}{inner}{extra}</div>')

def strip(id, text, x, y, w, h, rot, color=YEL, tcolor="#17130F", font="BS", size=120, seed=1, z=4, left=None, align="center"):
    inner = (f'<div class="stx" id="{id}t" style="font-family:{font};font-size:{size}px;line-height:{h}px;color:{tcolor};text-align:{align};'
             f'{("left:%dpx;transform:none;" % left) if left else ""}">{text}</div>')
    return P(inner, id, x, y, w, h, rot, "card", color, seed, 6, z)

def tape(id, x, y, rot, w=150, h=46, seed=0):
    rel, pad = p6lib.make_piece(w, h, "card", (228, 208, 150), 900 + seed, 3, False, True, 18)
    return (f'<img class="tape" id="{id}" src="{rel}" style="left:{x - pad}px;top:{y - pad}px;width:{w + 2 * pad}px;height:{h + 2 * pad}px;transform:rotate({rot}deg)">')

def print_(photo, id, x, y, w, h, rot, z=3, stamp=None, tp=True, seed=40):
    st = ""
    if stamp:
        st = f'<div class="stamp" id="{id}s" style="{"left:14px;" if stamp == "L" else "left:auto;right:14px;"}bottom:14px">NEVER POSTED</div>'
    inner = (f'<img class="phimg" src="assets/p6/pht_{photo}.jpg" style="left:14px;top:14px;width:{w - 28}px;height:{h - 64}px">'
             f'<div class="pvig" style="left:14px;top:14px;width:{w - 28}px;height:{h - 64}px"></div>{st}')
    t_ = tape(id + "tp", w // 2 - 75, -18, -4, seed=seed) if tp else ""
    return P(inner, id, x, y, w, h, rot, "card", WHT, seed, 3, z, "prn", t_)

def fbsticker(id, x, y, size, rot):
    return f'<div class="fbs" id="{id}" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px;transform:rotate({rot}deg)"><img src="assets/facebook.svg"></div>'

def hookblock(s):
    return (f'<div class="cam" id="hcam{s}">'
            + strip(f"hA{s}", "FACEBOOK CAN LOOK", 90, 290, 900, 132, -1.2, YEL, size=91, seed=3, left=190, align="left")
            + strip(f"hB{s}", "THROUGH PHOTOS YOU", 90, 436, 900, 130, 1.0, YEL, size=104, seed=5, z=5)
            + strip(f"hC{s}", "never posted", 190, 580, 700, 116, -1.8, BLK, "#fff", "Gloock", 90, 7, z=6)
            + print_("beach", f"pr1{s}", 92, 752, 320, 420, -8, 3, "L", True, 41) + print_("desk", f"pr3{s}", 668, 762, 320, 420, 9, 3, "R", True, 43)
            + print_("cake", f"pr2{s}", 345, 722, 390, 480, 2, 4, None, True, 42)
            + fbsticker(f"fbs{s}", 100, 298, 112, -8) + '</div>')

def uiblock(n):
    if n == 1:
        body = ('<div class="fbtop"><div class="fbsm"><img src="assets/facebook.svg"></div><div class="avt" id="hot1"><i class="avh"></i><i class="avb"></i></div></div>'
                '<u class="sk" style="top:230px;width:70%"></u><u class="sk" style="top:276px;width:52%"></u><u class="sk" style="top:360px;width:62%"></u><u class="sk" style="top:406px;width:40%"></u><div class="circ" id="circ1" style="right:30px;top:6px;width:200px;height:170px"></div>')
    elif n == 2:
        body = ('<u class="sk" style="top:50px;width:46%"></u><u class="sk" style="top:150px;width:58%"></u>'
                '<div class="hrow" id="hot2" style="top:236px"><b>Settings &amp; Privacy</b></div><u class="sk" style="top:370px;width:52%"></u><u class="sk" style="top:420px;width:40%"></u><div class="circ" id="circ2" style="left:20px;top:222px;width:850px;height:120px"></div>')
    elif n == 3:
        body = ('<u class="sk" style="top:60px;width:50%"></u><div class="hrow" id="hot3" style="top:160px"><i class="gear"></i><b>Settings</b></div>'
                '<u class="sk" style="top:310px;width:60%"></u><u class="sk" style="top:360px;width:44%"></u><div class="circ" id="circ3" style="left:20px;top:146px;width:850px;height:120px"></div>')
    else:
        body = ('<u class="sk" style="top:36px;width:56%"></u><div class="hrow tall" id="hot4" style="top:120px"><b>Camera roll sharing suggestions</b><div class="tg2 on" id="tg4"><i></i></div></div>'
                '<u class="sk" style="top:330px;width:48%"></u><div class="uinote">menu names can differ by app version</div><div class="circ" id="circ4" style="left:20px;top:104px;width:850px;height:200px"></div>')
    tp = tape(f"uitp{n}", 60, -16, -5, seed=10 + n) + tape(f"uitq{n}", 700, -16, 4, seed=20 + n)
    return P(f'<div class="uibody">{body}</div><div class="tapr" id="tapr{n}"></div>', f"ui{n}", 90, 760, 900, 466, 0.6 * (-1) ** n, "news", CRM, 20 + n, 6, 3, "", tp)

def stepscene(n, lines):
    lab = "".join(strip(f"sl{n}{i}", t, 360 - i * 6, 338 + i * 130, 620 + (i % 2) * 12, 112, (-1.5, 1.2, -.8)[i], YEL if i != 1 else BLK, "#17130F" if i != 1 else "#fff", "BS", 92, 60 + n * 3 + i, z=5) for i, t in enumerate(lines))
    return (f'<div class="sc" id="p{n}"><div class="cam" id="pc{n}"><div class="pnum" id="pn{n}">{n}</div>{lab}'
            f'<div class="of4" id="of{n}">STEP {n} OF 4</div>{uiblock(n)}</div></div>')

def bigtoggle(id, x, y, w, h, on=True):
    return f'<div class="btg {"on" if on else ""}" id="{id}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{h // 2}px"><i style="width:{h - 48}px;height:{h - 48}px"></i></div>'

def chat():
    return (P('<div class="mini"><b>Camera roll sharing suggestions</b><div class="tg2" id="tg7"><i></i></div></div>', "outb", 110, 650, 860, 240, 1.0, "news", CRM, 91, 6, 3)
            + '<div class="mavt" id="mav">M</div><div class="dots2" id="dots2"><i></i><i></i><i></i></div>'
            + "".join(strip(f"al{k}", "ALLOW", 250 + (k - 1) * 255, 1070, 235, 112, (-3, 2, -2)[k - 1], YEL, size=88, seed=70 + k, z=6) for k in (1, 2, 3)))

# ---- decor (whole frame, data-decor): newsprint scraps, bottom prints, flyers, foreground blur
NEWS_DECOR = [(-80, 120, 560, 420, -4), (560, 40, 600, 440, 5), (-60, 1290, 520, 430, 3), (500, 1340, 640, 460, -3), (180, 1590, 700, 420, 2), (-110, 760, 300, 360, 6), (890, 800, 300, 380, -5), (330, 20, 380, 220, 2)]
decor = "".join(f'<div class="dc" id="nd{i}" data-decor style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({r}deg)">{pimg(w, h, "news", CRM, 100 + i, 9)}</div>' for i, (x, y, w, h, r) in enumerate(NEWS_DECOR))
decor_prints = (print_("beach", "dp1", 30, 1390, 290, 380, -9, 2, None, True, 61) + print_("cake", "dp2", 730, 1440, 290, 380, 8, 2, None, True, 62) + print_("desk", "dp3", 400, 1560, 280, 360, 3, 2, None, True, 63))
flyers = "".join(f'<div class="dc fly" id="fl{i}" data-decor style="left:0;top:0;width:{w}px;height:{h}px">{pimg(w, h, "news", CRM, 300 + i, 6)}</div>' for i, (w, h) in enumerate(((220, 150), (260, 170), (180, 130), (240, 160), (200, 140), (170, 120))))
fgl = "".join(f'<img class="fgs" id="fg{i}" data-decor src="assets/p6/fg{i}.png">' for i in range(3))

markup = f'''
<div id="world">
<div class="bgl" id="bgl" data-decor><img class="bgimg" id="bgimg" src="assets/p6/bg_card.jpg"></div>
<div id="npl" data-decor>{decor}</div>
<div id="dpr" data-decor>{decor_prints}</div>
<div id="flys" data-decor>{flyers}</div>
<div class="sc" id="s1" style="opacity:1;visibility:visible">{hookblock("")}</div>
<div class="sc" id="s2"><div class="cam" id="c2">
 {strip("t2", "ONLY IF YOU TAPPED", 90, 300, 900, 150, -1.2, YEL, size=112, seed=11, z=5)}
 {P('<div class="mp"></div>', "dlg2", 90, 520, 900, 660, 0.5, "news", CRM, 12, 8, 2)}
 <div id="stk">{print_("beach", "d1", 160, 560, 240, 320, -8, 3, None, False, 51)}{print_("cake", "d2", 360, 540, 260, 340, 2, 4, None, False, 52)}{print_("desk", "d3", 580, 560, 240, 320, 9, 3, None, False, 53)}</div>
 {strip("nb", "Not now", 125, 940, 280, 190, 0, (216, 207, 184), "#5d554a", "IDisp", 54, 21, z=4)}
 {strip("b2", "ALLOW", 430, 930, 470, 210, -1.5, BLK, "#fff", "BS", 190, 22, z=5)}
 <div class="ring" id="ring"></div><div class="fing" id="fing"></div><div class="tiny" id="ill2">illustration</div></div></div>
<div class="sc" id="s3"><div class="cam" id="c3">
 {strip("t3a", "HERE'S HOW", 90, 292, 900, 178, -1.2, YEL, size=150, seed=31, z=5)}
 {strip("t3b", "to stop it", 190, 488, 700, 170, 1.4, BLK, "#fff", "Gloock", 130, 32, z=6)}
 {P(bigtoggle("bigtg", 70, 35, 700, 330, True), "tgp", 110, 690, 860, 400, -.8, "news", CRM, 33, 8, 2)}
 {strip("tlab", "Camera roll sharing suggestions", 90, 1120, 900, 80, 0.8, YEL, size=32, font="PlexM", seed=34, z=5)}</div></div>
{stepscene(1, ["PROFILE", "PICTURE"])}
{stepscene(2, ["SETTINGS &amp;", "PRIVACY"])}
{stepscene(3, ["SETTINGS"])}
{stepscene(4, ["CAMERA ROLL", "SHARING", "SUGGESTIONS"])}
<div class="sc" id="s5"><div class="cam" id="c5">
 {strip("t5", "SWITCH IT OFF", 90, 300, 900, 170, -1.2, YEL, size=150, seed=51, z=5)}
 {P(bigtoggle("bigtg2", 50, 50, 780, 420, True), "tgp2", 100, 520, 880, 520, .6, "news", CRM, 52, 8, 2)}
 <div class="burst" id="burst"></div>
 <div class="offst" id="offw"><span class="scr" id="scr0">X#7</span><span class="scr" id="scr1">0F?</span><span class="scr" id="scr2">OF#</span><span class="offf" id="offf">OFF</span></div></div></div>
<div class="sc" id="s6"><div class="cam" id="c6">
 {strip("t6a", "META SAYS", 290, 296, 500, 110, -2, BLK, "#fff", "Gloock", 70, 61, z=6)}
 {P('<div class="optin" id="optin">OPT-IN</div>', "pin6", 110, 440, 860, 420, -1, "news", CRM, 62, 8, 3)}
 {strip("t6b", "NOT USED FOR ADS", 90, 890, 900, 150, 1.0, YEL, size=120, seed=63, z=5)}
 {strip("t6c", "Meta newsroom, April 2026 · EU and UK", 140, 1090, 800, 64, -0.6, (234, 223, 194), "#3b342a", "IDisp", 30, 64, z=4)}</div></div>
<div class="sc" id="s7"><div class="cam" id="c7">
 {strip("t7a", "SEND THIS TO SOMEONE", 90, 292, 900, 120, -1.0, YEL, size=92, seed=71, z=5)}
 {strip("t7b", "who always taps Allow", 120, 426, 840, 120, 1.0, BLK, "#fff", "Gloock", 76, 72, z=6)}
 {chat()}</div></div>
<div class="sc" id="sH">{hookblock("H")}</div>
<div id="fgl" data-decor>{fgl}</div>
</div>
<img class="sheet" id="sheetA" data-decor src="assets/p6/sheet0.png"><img class="sheet" id="sheetB" data-decor src="assets/p6/sheet1.png">
<img class="grain" id="grain" data-decor src="assets/p6/grain.jpg">
'''

styles = r'''
@font-face{font-family:"BS";src:url("assets/fonts/BigShoulders-Bold.ttf");font-weight:700}
@font-face{font-family:"Gloock";src:url("assets/fonts/Gloock-Regular.ttf")}
@font-face{font-family:"PlexM";src:url("assets/fonts/IBMPlexMono-Bold.ttf");font-weight:700}
:root{--ink:#17130F;--yel:#F2C230;--red:#B6402B;--lime:#9BE22E}
html,body,#root{background:#8c6f48}
#world{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 960px}
.bgl{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden;background:#a07f52}
.bgimg{position:absolute;left:-900px;top:0;width:2880px;height:1920px}
#npl,#dpr,#flys,#fgl{position:absolute;left:0;top:0;width:1080px;height:1920px;pointer-events:none}
.dc{position:absolute;opacity:.82}
#dpr{opacity:.5}
.dc.fly{opacity:0}
.fgs{position:absolute;left:0;top:0;opacity:0}
.sc{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0;visibility:hidden}
.cam{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 760px}
.pcw{position:absolute}
.pbg{position:absolute;max-width:none;pointer-events:none}
.stx{position:absolute;left:50%;transform:translateX(-50%);top:0;width:auto;height:100%;white-space:nowrap;letter-spacing:-.005em;text-transform:uppercase;font-weight:700}
.stx[style*="Gloock"]{text-transform:none;letter-spacing:-.01em}
.stx[style*="PlexM"]{letter-spacing:-.02em}
.tape{position:absolute;max-width:none;opacity:.88;z-index:12}
.phimg{position:absolute;max-width:none}
.pvig{position:absolute;background:radial-gradient(120% 90% at 50% 40%,transparent 60%,rgba(0,0,0,.28))}
.stamp{position:absolute;font:700 21px BS;letter-spacing:.06em;color:var(--red);border:3px solid var(--red);padding:1px 8px 2px;border-radius:6px;mix-blend-mode:multiply;opacity:.8;white-space:nowrap;transform:rotate(-2deg)}
.fbs{position:absolute;z-index:20;border-radius:50%;background:#fff;box-shadow:0 0 0 6px #fff,0 8px 20px rgba(30,18,6,.45);overflow:hidden}.fbs img{width:100%;height:100%;padding:6px}
.pnum{position:absolute;left:92px;top:340px;font:700 440px BS;line-height:400px;color:var(--red);opacity:.95;letter-spacing:-.02em}
.of4{position:absolute;left:360px;top:288px;font:700 26px PlexM;letter-spacing:.1em;color:#3b2a14}
.uibody{position:absolute;inset:0}
.sk{display:block;position:absolute;left:44px;height:24px;border-radius:12px;background:#CFC3A6;text-decoration:none}
.fbtop{position:absolute;left:0;top:0;width:100%;height:180px;background:rgba(239,231,210,.8)}
.fbsm{position:absolute;left:34px;top:34px;width:112px;height:112px;border-radius:50%;background:#fff;box-shadow:0 4px 10px rgba(30,18,6,.3);overflow:hidden}.fbsm img{width:100%;height:100%;padding:6px}
.avt{position:absolute;right:50px;top:14px;width:150px;height:150px;border-radius:50%;background:linear-gradient(160deg,#C99A62,#8C5A2B);overflow:hidden}
.avh{position:absolute;left:50px;top:28px;width:50px;height:50px;border-radius:50%;background:#F5E7CB}.avb{position:absolute;left:28px;top:90px;width:94px;height:80px;border-radius:50% 50% 0 0;background:#F5E7CB}
.hrow{position:absolute;left:30px;right:30px;height:100px;border-radius:14px;background:linear-gradient(transparent 12%,rgba(242,194,48,.95) 12%,rgba(242,194,48,.95) 88%,transparent 88%);display:flex;align-items:center;padding:0 24px;gap:20px}
.hrow b{font:700 66px BS;letter-spacing:.005em;text-transform:uppercase}
.hrow.tall{height:190px}.hrow.tall b{font-size:58px;line-height:60px;flex:1}
.circ{position:absolute;border:9px solid var(--red);border-radius:50%/60%;transform:rotate(-2deg);opacity:0}
.tapr{position:absolute;right:120px;top:130px;width:90px;height:90px;border-radius:50%;border:8px solid var(--red);opacity:0}
.gear{display:block;width:52px;height:52px;border-radius:50%;border:11px solid #4a3a26;box-sizing:border-box}
.tg2{position:relative;width:150px;height:84px;border-radius:42px;background:#CBBFA3;flex:none}
.tg2 i{position:absolute;left:5px;top:5px;width:74px;height:74px;border-radius:50%;background:#fff;box-shadow:0 4px 10px rgba(14,14,14,.35)}
.tg2.on{background:#2a2118}.tg2.on i{left:auto;right:5px}
.uinote{position:absolute;left:0;width:100%;bottom:70px;text-align:center;font:700 26px PlexM;color:#4a3a26}
.btg{position:absolute;background:#CBBFA3;box-shadow:inset 0 -10px 0 rgba(0,0,0,.10)}
.btg i{position:absolute;left:24px;top:24px;border-radius:50%;background:#fff;box-shadow:0 12px 26px rgba(14,14,14,.4)}
.btg.on{background:#2a2118}.btg.on i{left:auto;right:24px}
.mini{position:absolute;inset:0;display:flex;align-items:center;justify-content:space-between;padding:0 50px;gap:20px}
.mini b{font:700 68px BS;line-height:68px;text-transform:uppercase}
.mini .tg2{width:190px;height:106px;border-radius:53px}.mini .tg2 i{width:94px;height:94px}
.mp{position:absolute;inset:0}
.optin{position:absolute;left:0;top:0;width:100%;height:100%;font:400 250px Gloock;line-height:430px;text-align:center;color:var(--ink);letter-spacing:-.03em}
.offst{position:absolute;left:90px;top:1050px;width:900px;height:140px;text-align:center;font-family:BS;font-weight:700;font-size:170px;line-height:140px}
.offst span{position:absolute;left:0;width:100%;top:0;opacity:0}
.offf{background:var(--lime);color:var(--ink);border:8px solid var(--ink);border-radius:30px;padding:0 60px;width:auto!important;left:50%!important;transform:translateX(-50%) rotate(-4deg)!important;box-shadow:8px 10px 0 var(--ink)}
.offst .scr{color:#4a3a26}
.burst{position:absolute;left:340px;top:640px;width:400px;height:400px;border-radius:50%;background:radial-gradient(circle,rgba(30,18,6,.55) 2.4px,transparent 3px) 0 0/16px 16px;-webkit-mask-image:radial-gradient(circle,transparent 30%,#000 60%,transparent 100%);opacity:0}
.mavt{position:absolute;left:100px;top:1080px;width:120px;height:120px;border-radius:50%;background:var(--yel);font:700 90px BS;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 6px #fff,0 8px 20px rgba(30,18,6,.45);opacity:0}
.dots2{position:absolute;left:250px;top:1086px;width:230px;height:112px;background:#FBF8EF;border-radius:50px 50px 50px 12px;box-shadow:0 8px 18px rgba(30,18,6,.4);display:flex;align-items:center;justify-content:center;gap:18px;opacity:0}
.dots2 i{display:block;width:26px;height:26px;border-radius:50%;background:var(--ink)}
.ring{position:absolute;left:720px;top:940px;width:110px;height:110px;border-radius:50%;border:10px solid var(--red);opacity:0;z-index:30}
.fing{position:absolute;left:740px;top:1020px;width:100px;height:100px;border-radius:50%;background:rgba(23,19,15,.8);opacity:0;z-index:30}
.tiny{position:absolute;left:65px;width:950px;text-align:center;font:700 26px PlexM;letter-spacing:.06em;color:#3b2a14;text-transform:uppercase}
#ill2{top:1196px}
.sheet{position:absolute;left:0;top:-120px;width:1470px;height:2290px;max-width:none;z-index:80;opacity:0;pointer-events:none}
.grain{position:absolute;left:-40px;top:-40px;width:1160px;height:2000px;max-width:none;mix-blend-mode:overlay;opacity:.38;z-index:90;pointer-events:none}
'''

# ------------------------------------------------------------ timeline (generated)
D_ = D
rnd = _r.Random(6)
def at(t): return tt(t)
EA, EX = "sine.inOut", "expo.out"

def slam(sel, t, dx=0, dy=0, rot=0, s0=1.35, dur=.3, typed=False):
    """text-safe entrance: torn-paper wipe at the final position (clip reveal) + tiny slam; the text box never leaves the safe area"""
    wid, hei = REG.get(sel[1:], (900, 130))
    sx = min(s0, 1.06); ox = max(-40, min(40, dx * .2)); oy = max(-18, min(18, dy * .15))
    L = [-60, -60, -60, -60]   # top right bottom left
    if dy < 0 and abs(dy) >= abs(dx): L[2] = hei + 60
    elif dy > 0 and abs(dy) > abs(dx): L[0] = hei + 60
    elif dx > 0: L[3] = wid + 60
    else: L[1] = wid + 60
    st = " ".join(f"{v}px" for v in L)
    js(f"tl.fromTo('{sel}',{{clipPath:'inset({st})',x:{ox},y:{oy},scale:{sx},rotation:'+={rot * .5}'}},{{clipPath:'inset(-60px -60px -60px -60px)',x:0,y:0,scale:1,rotation:'-={rot * .5}',duration:{dur},ease:'expo.out',transformOrigin:'50% 50%'}},{at(t)});")

def settle(sel, t, dx=0, dy=0, rot=0, s0=1.05, dur=.4):
    """hook strips are readable from frame 0: they only settle (no fade-in)"""
    js(f"tl.fromTo('{sel}',{{x:{dx},y:{dy},scale:{s0},rotation:'+={rot}'}},{{x:0,y:0,scale:1,rotation:'-={rot}',duration:{dur},ease:'expo.out',transformOrigin:'50% 50%'}},{at(t)});")

def drop(sel, t, dy=-420, dx=0, s0=1, dur=.5, ease="back.out(1.25)", rot=0):
    js(f"tl.fromTo('{sel}',{{y:{dy},x:{dx},scale:{s0},opacity:1,rotation:'+={rot}'}},{{y:0,x:0,scale:1,rotation:'-={rot}',duration:{dur},ease:'{ease}',transformOrigin:'50% 50%'}},{at(t)});")

def tapeslap(sel, t):
    js(f"tl.fromTo('{sel}',{{scale:1.7,opacity:0}},{{scale:1,opacity:.88,duration:.14,ease:'power3.in'}},{at(t)});")

def fly(i, t, y0, y1, dirn=1, dur=.7, rot0=-25, rot1=15, s=1):
    x0, x1 = (1250, -320) if dirn > 0 else (-320, 1250)
    js(f"tl.fromTo('#fl{i}',{{x:{x0},y:{y0},rotation:{rot0},opacity:1,scale:{s}}},{{x:{x1},y:{y1},rotation:{rot1},duration:{dur},ease:'power1.inOut'}},{at(t)});")
    js(f"tl.set('#fl{i}',{{opacity:0}},{at(t + dur + .02)});")
    sfx("whoosh_c.ogg", t + .05, -9)

def fgcross(i, t, y, dur=1.0, dirn=1):
    x0, x1 = (1300, -700) if dirn > 0 else (-700, 1300)
    js(f"tl.fromTo('#fg{i}',{{x:{x0},y:{y},rotation:-8,opacity:1}},{{x:{x1},y:{y + 40},rotation:10,duration:{dur},ease:'sine.inOut'}},{at(t)});")
    js(f"tl.set('#fg{i}',{{opacity:0}},{at(t + dur + .02)});")

def swap(old, new, t, k):
    """newsprint sheet sweeps right->left over the frame; scenes are swapped while it covers the picture (no blank dips)"""
    sh = "sheetA" if k % 2 == 0 else "sheetB"
    r = (-2.5, 2.0, -1.5)[k % 3]
    js(f"tl.fromTo('#{sh}',{{x:1160,y:{[-80, -140, -30][k % 3]},rotation:{r},opacity:1}},{{x:-1560,y:{[-120, -60, -100][k % 3]},rotation:{-r},duration:.4,ease:'power2.inOut'}},{at(t - .2)});")
    js(f"tl.set('#{sh}',{{opacity:0}},{at(t + .22)});")
    if old: js(f"tl.set('#{old}',{{autoAlpha:0}},{at(t - .02)});")
    js(f"tl.set('#{new}',{{autoAlpha:1}},{at(t - .01)});")
    sfx(("whoosh_b.ogg", "whoosh_a.ogg")[k % 2], t - .22, -2)

def push(cam, t0, t1, r0=0, r1=0, s1=1.025):
    js(f"tl.fromTo('#{cam}',{{scale:1,rotation:{r0}}},{{scale:{s1},rotation:{r1},duration:{max(.3, t1 - t0):.3f},ease:'sine.inOut',transformOrigin:'540px 760px'}},{at(t0)});")

def cap_tap(i, t, sfxn="tick.ogg"):
    sfx(sfxn, t, -2)

# --- global
js(f"tl.fromTo('#world',{{scale:1,rotation:-.25}},{{scale:1.014,rotation:.25,duration:{D_ / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1,transformOrigin:'540px 960px'}},0);")
js(f"tl.fromTo('#bgimg',{{x:0}},{{x:-300,duration:{D_ / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1}},0);")
for i, (dx, dy) in enumerate(((60, -30), (-70, 20), (40, 35), (-50, -25), (80, 15), (-30, 40), (35, -40), (-60, -20))):
    js(f"tl.fromTo('#nd{i}',{{x:0,y:0}},{{x:{dx},y:{dy},duration:{D_ / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1}},0);")
for i, (dx, dy) in enumerate(((50, -20), (-60, 15), (40, 30))):
    js(f"tl.fromTo('#dp{i + 1}',{{x:0,y:0}},{{x:{dx},y:{dy},duration:{D_ / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1}},0);")
# film grain: jitter at 12 fps (small offsets, soft)
g_t = 0.0
while g_t < D_:
    js(f"tl.set('#grain',{{x:{rnd.randint(-30, 30)},y:{rnd.randint(-30, 30)}}},{at(g_t)});"); g_t += 1 / 12

# --- HOOK
def hook(s, t0, t1, final=False):
    k = "" if not final else "H"
    if final:
        js(f"tl.fromTo('#hcam{k}',{{scale:1.035,rotation:.4}},{{scale:1,rotation:0,duration:{t1 - t0:.3f},ease:'sine.inOut',transformOrigin:'540px 760px'}},{at(t0)});")
        return
    settle(f"#hA{k}", t0, dx=-30, rot=1, s0=1.04); settle(f"#hB{k}", t0 + .05, dx=30, rot=-1, s0=1.04); settle(f"#hC{k}", t0 + .1, dy=-14, rot=1.5, s0=1.05)
    js(f"tl.fromTo('#fbs{k}',{{scale:.5,rotation:-48,opacity:1}},{{scale:1,rotation:-8,duration:.5,ease:'back.out(2.2)'}},{at(t0)});")
    drop(f"#pr1{k}", t0, dy=150, dur=.55, ease="power3.out", rot=-10)
    drop(f"#pr3{k}", t0 + .07, dy=170, dur=.55, ease="power3.out", rot=10)
    drop(f"#pr2{k}", t0 + .14, dy=130, s0=.9, dur=.55, ease="power3.out", rot=-3)
    for j, tp_ in enumerate(("pr1", "pr2", "pr3")):
        tapeslap(f"#{tp_}{k}tp", t0 + .5 + j * .1); sfx("tick.ogg", t0 + .5 + j * .1, -4)
    for j, st in enumerate(("pr1", "pr3")):
        js(f"tl.fromTo('#{st}{k}s',{{scale:2.0,opacity:0}},{{scale:1,opacity:.8,duration:.16,ease:'power4.in'}},{at(t0 + .9 + j * .2)});")
        sfx("pop_a.ogg", t0 + .92 + j * .2, -3)
    sfx("impactpunch.ogg", t0 + .04, 0); sfx("subhit.ogg", t0 + .04, -3); sfx("whoosh_a.ogg", t0, -2)
    # continuous life
    for j, (sel, a) in enumerate((("pr1", -12), ("pr3", -10), ("pr2", -14))):
        js(f"tl.to('#{sel}{k}',{{y:{a},duration:1.2,ease:'sine.inOut',yoyo:true,repeat:{max(1, int((t1 - t0 - .7) / 1.2) - 1)}}},{at(t0 + .75 + j * .1)});")
    js(f"tl.to('#pr2{k}',{{scale:1.06,rotation:-1,duration:.5,ease:'sine.inOut',yoyo:true,repeat:1}},{at(t0 + 1.35)});")
    js(f"tl.to('#hA{k}',{{y:-5,duration:.6,ease:'sine.inOut',yoyo:true,repeat:1}},{at(t0 + .7)});")
    js(f"tl.to('#hB{k}',{{y:3,duration:.6,ease:'sine.inOut',yoyo:true,repeat:1}},{at(t0 + .8)});")
    js(f"tl.fromTo('#hC{k}',{{scale:1.07}},{{scale:1,duration:.5,ease:'expo.out',immediateRender:false,transformOrigin:'50% 50%'}},{at(T['slam1'])});")
    fly(0, t0 + .35, 1380, 1480, 1, .8); fly(1, t0 + 1.05, 1600, 1520, -1, .8, 20, -10)
    fgcross(0, t0 + 1.7, 1420, 1.0, 1); fly(2, t0 + 2.05, 1330, 1450, 1, .7)
    push("hcam", t0, t1, -.4, .5, 1.035)
hook("", 0, T["s2"] + .1)
sfx("click_a.ogg", T["slam1"], -4)

# --- S2
s = T["s2"]; swap("s1", "s2", s, 0)
slam("#t2", s + .02, dy=-130, rot=2, s0=1.3, dur=.38, typed=True); sfx("impactsoft.ogg", s + .1, -6)
drop("#dlg2", s + .12, dy=-520, dur=.55, ease="back.out(1.15)"); sfx("pop_b.ogg", s + .5, -3)
for j, d in enumerate(("d1", "d2", "d3")):
    drop(f"#{d}", s + .3 + j * .12, dy=-340, dx=(-40, 0, 40)[j], dur=.4, ease="power3.out", rot=(-12, 6, 14)[j]); sfx("tick.ogg", s + .6 + j * .12, -3)
slam("#nb", s + .62, dx=-320, s0=1.0, dur=.3)
slam("#b2", s + .74, dx=0, dy=-40, rot=-3, s0=1.06, dur=.34); sfx("impactsoft.ogg", s + .85, -5)
js(f"tl.fromTo('#fing',{{opacity:0,y:60}},{{opacity:1,y:0,duration:.4,ease:'power2.out'}},{at(T['tapAllow'] - .4)});")
js(f"tl.to('#b2',{{scale:.93,duration:.14,ease:'sine.inOut',transformOrigin:'50% 50%'}},{at(T['tapAllow'])});")
js(f"tl.fromTo('#ring',{{opacity:.95,scale:.5}},{{opacity:0,scale:2.6,duration:.7,ease:'power2.out'}},{at(T['tapAllow'] + .02)});")
js(f"tl.to('#b2',{{scale:1,duration:.3,ease:'sine.inOut'}},{at(T['tapAllow'] + .14)});")
js(f"tl.to('#fing',{{opacity:0,duration:.3}},{at(T['tapAllow'] + .45)});")
js(f"tl.fromTo('#ill2',{{opacity:0}},{{opacity:1,duration:.3}},{at(s + .7)});")
sfx("select.ogg", T["tapAllow"], 0); sfx("pop_b.ogg", T["tapAllow"] + .06, -3)
fly(3, s + .5, 1370, 1300, -1, .8, 15, -20); fgcross(1, s + 1.3, 1500, 1.1, -1); fly(4, s + 1.8, 1560, 1640, 1, .7)
push("c2", s, T["s3"], .3, -.4)

# --- S3
s = T["s3"]; swap("s2", "s3", s, 1)
slam("#t3a", s + .02, dx=-300, rot=1, s0=1.1, dur=.38, typed=True)
slam("#t3b", s + .18, dx=300, rot=-1, s0=1.1, dur=.38)
drop("#tgp", s + .3, dy=420, dur=.55, ease="back.out(1.3)"); sfx("pop_b.ogg", s + .6, -3)
slam("#tlab", s + .55, dy=140, s0=1.0, dur=.35); sfx("tick.ogg", s + .7, -3)
js(f"tl.to('#bigtg i',{{x:-18,duration:.35,ease:'sine.inOut',yoyo:true,repeat:3}},{at(s + .9)});")
fly(5, s + .45, 1400, 1330, 1, .75); fgcross(2, s + .9, 1520, 1.0, 1)
sfx("toggle.ogg", s + .3, -8)
push("c3", s, T["p1"], -.3, .4)

# --- steps (each: numeral slam, labels slam, ui card flips in, circle, tap ripple)
steps = [("p1", "p2", "pc1", "pn1", ["sl10", "sl11"], "ui1", "circ1", "tapr1"), ("p2", "p3", "pc2", "pn2", ["sl20", "sl21"], "ui2", "circ2", "tapr2"),
         ("p3", "p4", "pc3", "pn3", ["sl30"], "ui3", "circ3", "tapr3"), ("p4", "s5", "pc4", "pn4", ["sl40", "sl41", "sl42"], "ui4", "circ4", "tapr4")]
prev = "s3"
for i, (a, b, cam, pn, labs, ui, circ, tr) in enumerate(steps):
    s = T[a]; e = T[b]
    swap(prev, a, s, 2 + i); prev = a
    js(f"tl.fromTo('#{pn}',{{scale:1.7,opacity:0,x:-60}},{{scale:1,opacity:.95,x:0,duration:.34,ease:'expo.out',transformOrigin:'30% 50%'}},{at(s + .02)});")
    for j, l in enumerate(labs): slam("#" + l, s + .08 + j * .07, dx=220, rot=-1, s0=1.0, dur=.3)
    slam("#" + ui, s + .12, dy=90, rot=1, s0=1.05, dur=.4)
    js(f"tl.fromTo('#{circ}',{{opacity:0,scale:1.35}},{{opacity:1,scale:1,duration:.26,ease:'expo.out',transformOrigin:'50% 50%'}},{at(s + .5)});")
    js(f"tl.fromTo('#{tr}',{{opacity:.9,scale:.4}},{{opacity:0,scale:2.2,duration:.5,ease:'power2.out'}},{at(s + .5)});")
    sfx("tick.ogg", s + .5, -1); sfx("pop_b.ogg", s + .14, -6)
    if i % 2 == 0: fly(i, s + .25, 1360 + i * 20, 1420, 1, .7)
    else: fgcross(i % 3, s + .3, 1480, .9, -1)
    push(cam, s, e + .1, (.4, -.4, .3, -.3)[i], (-.3, .4, -.3, .3)[i], 1.04)
    if i == 3: js(f"tl.to('#{ui}',{{y:-6,duration:.9,ease:'sine.inOut'}},{at(s + .7)});")

# --- S5 OFF (the proof)
s = T["s5"]; swap("p4", "s5", s, 6)
slam("#t5", s + .02, dy=-130, rot=-2, s0=1.3, dur=.36, typed=True)
drop("#tgp2", s + .1, dy=360, dur=.5, ease="back.out(1.2)")
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
push("c5", s, T["s6"], -.3, .4, 1.04)

# --- S6 Meta
s = T["s6"]; swap("s5", "s6", s, 7)
slam("#t6a", s + .02, dy=-100, rot=2, s0=1.3, dur=.34)
slam("#pin6", s + .1, dy=60, rot=1, s0=1.06, dur=.42); sfx("pop_b.ogg", s + .45, -3)
js(f"tl.fromTo('#optin',{{scale:1.06}},{{scale:1,duration:.4,ease:'expo.out',transformOrigin:'50% 50%'}},{at(s + .3)});")
slam("#t6b", s + .6, dx=300, rot=-1, s0=1.0, dur=.34, typed=True); sfx("impactsoft.ogg", s + .65, -6)
slam("#t6c", s + 1.0, dy=60, s0=1.0, dur=.3)
sfx("pop_a.ogg", W(4, 2), -3)
fly(3, s + .4, 1380, 1480, 1, .8); fgcross(0, s + .9, 1540, 1.1, -1); fly(4, s + 1.5, 1330, 1450, -1, .7, 10, -20)
push("c6", s, T["s7"], .3, -.4)

# --- S7 send
s = T["s7"]; swap("s6", "s7", s, 8)
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
push("c7", s, T["end"], -.3, .3, 1.035)

# --- loop back to frame 0
swap("s7", "sH", T["loop"], 9)
sfx("whoosh_c.ogg", T["loop"] - .1, -5)
hook("H", T["loop"], D_, final=True)
js(f"tl.set('#sH',{{autoAlpha:0}},0);")

JS = "const D2=" + str(D_) + ";\n" + "\n".join(J)
json.dump([dict(f=f, t=t, g=g) for f, t, g in SFX if t < D_ and t >= 0], open(H + "/sfx6.json", "w"), indent=1)

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
