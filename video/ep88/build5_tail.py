# ---- markup: torn-paper magazine collage (visual language of the reference reel, our own content)
import random as _r

def torn(w, h, seed, amp=7, step=24):
    rnd = _r.Random(seed); pts = []
    x = 0
    while x < w: pts.append((x, rnd.uniform(0, amp))); x += step * rnd.uniform(.6, 1.3)
    pts.append((w, rnd.uniform(0, amp))); y = 0
    while y < h: pts.append((w - rnd.uniform(0, amp), y)); y += step * rnd.uniform(.6, 1.3)
    pts.append((w - rnd.uniform(0, amp), h)); x = w
    while x > 0: pts.append((x, h - rnd.uniform(0, amp))); x -= step * rnd.uniform(.6, 1.3)
    pts.append((0, h - rnd.uniform(0, amp))); y = h
    while y > 0: pts.append((rnd.uniform(0, amp), y)); y -= step * rnd.uniform(.6, 1.3)
    return "polygon(" + ",".join(f"{a:.0f}px {b:.0f}px" for a, b in pts) + ")"

YEL, BLK, CRM, KRF = "#F2C230", "#17130F", "#F0E4C8", "#C9A672"

def piece(inner, id, x, y, w, h, rot=0, bg=CRM, seed=1, amp=7, z=3, cls=""):
    return (f'<div class="pcw {cls}" id="{id}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:{z}">'
            f'<div class="pc"><div class="pcb" style="clip-path:{torn(w, h, seed, amp)};background:{bg}"><div class="paperfx"></div>{inner}</div></div></div>')

def strip(id, text, x, y, w, h, rot, bg=YEL, color="#17130F", font="BS", size=120, seed=1, z=4, left=None, align="center"):
    inner = f'<div class="stx" id="{id}t" style="font-family:{font};font-size:{size}px;line-height:{h}px;color:{color};text-align:{align};{("padding-left:%dpx" % left) if left else ""}">{text}</div>'
    return piece(inner, id, x, y, w, h, rot, bg, seed, 6, z)

def tape(x, y, rot, w=150, h=46):
    return f'<div class="tape" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg)"></div>'

def print_(k, id, x, y, w, h, rot, z=3, stamp=True, tp=True):
    inner = (f'<div class="pic" style="inset:14px 14px 50px 14px"><img class="pimg" src="assets/photos/{ {0: "beach", 1: "cake", 3: "desk"}[k] }.jpg"><div class="ht2"></div><div class="pvig"></div></div>'
             + (f'<div class="stamp" id="{id}s" style="left:50%;top:auto;bottom:7px;transform:translateX(-50%) rotate(-2deg)">NEVER POSTED</div>' if stamp else ''))
    return (f'<div class="pcw prn" id="{id}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:{z}">'
            f'<div class="pc"><div class="pcb" style="background:#FBF6EA;clip-path:{torn(w, h, 40 + k, 3, 40)}">{inner}</div></div>'
            + (tape(w // 2 - 70, -16, -4 + k) if tp else '') + '</div>')

def fbsticker(id, x, y, size, rot):
    return (f'<div class="fbs" id="{id}" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px;transform:rotate({rot}deg)"><img src="assets/facebook.svg"></div>')

def hookblock(sfx):
    return (f'<div class="cam" id="hcam{sfx}">'
            + strip(f"hA{sfx}", "FACEBOOK CAN LOOK", 90, 290, 900, 132, -1.2, YEL, size=96, seed=3, left=190, align="left")
            + strip(f"hB{sfx}", "THROUGH PHOTOS YOU", 90, 436, 900, 130, 1.0, YEL, size=104, seed=5, z=5)
            + strip(f"hC{sfx}", "never posted", 190, 580, 700, 116, -1.8, BLK, "#fff", "Gloock", 90, 7, z=6)
            + f'<div id="cards{sfx}">' + print_(0, f"pr1{sfx}", 92, 752, 320, 420, -8, 3) + print_(3, f"pr3{sfx}", 668, 762, 320, 420, 9, 3) + print_(1, f"pr2{sfx}", 345, 722, 390, 480, 2, 4, False) + '</div>'
            + fbsticker(f"fbs{sfx}", 100, 298, 112, -8) + '</div>')

def uiblock(n):
    if n == 1:
        body = ('<div class="fbtop"><div class="fbsm"><img src="assets/facebook.svg"></div><div class="avt" id="hot1"><i class="avh"></i><i class="avb"></i></div></div>'
                '<u class="sk" style="top:230px;width:70%"></u><u class="sk" style="top:276px;width:52%"></u><u class="sk" style="top:360px;width:62%"></u><u class="sk" style="top:406px;width:40%"></u><div class="circ" id="circ1" style="right:30px;top:6px;width:200px;height:170px"></div>')
    elif n == 2:
        body = ('<u class="sk" style="top:50px;width:46%"></u><u class="sk" style="top:150px;width:58%"></u>'
                '<div class="hrow" id="hot2" style="top:236px"><b>Settings &amp; Privacy</b></div><u class="sk" style="top:370px;width:52%"></u><u class="sk" style="top:430px;width:40%"></u><div class="circ" id="circ2" style="left:20px;top:222px;width:860px;height:120px"></div>')
    elif n == 3:
        body = ('<u class="sk" style="top:60px;width:50%"></u><div class="hrow" id="hot3" style="top:160px"><i class="gear"></i><b>Settings</b></div>'
                '<u class="sk" style="top:310px;width:60%"></u><u class="sk" style="top:370px;width:44%"></u><div class="circ" id="circ3" style="left:20px;top:146px;width:860px;height:120px"></div>')
    else:
        body = ('<u class="sk" style="top:36px;width:56%"></u><div class="hrow tall" id="hot4" style="top:120px"><b>Camera roll sharing suggestions</b><div class="tg2 on" id="tg4"><i></i></div></div>'
                '<u class="sk" style="top:330px;width:48%"></u><div class="uinote">menu names can differ by app version</div><div class="circ" id="circ4" style="left:20px;top:104px;width:860px;height:200px"></div>')
    return piece(f'<div class="uibody">{body}</div>', f"ui{n}", 90, 760, 900, 466, 0.6 * (-1) ** n, "#FBF8EF", 20 + n, 6, 3)

def stepscene(n, lines):
    lab = "".join(strip(f"sl{n}{i}", t, 360 - i * 6, 338 + i * 130, 620 + (i % 2) * 12, 112, (-1.5, 1.2, -.8)[i], YEL if i != 1 else BLK, "#17130F" if i != 1 else "#fff", "BS", 92, 60 + n * 3 + i, z=5) for i, t in enumerate(lines))
    return (f'<div class="sc" id="p{n}"><div class="cam" id="pc{n}"><div class="pnum" id="pn{n}">{n}</div>{lab}'
            f'<div class="of4" id="of{n}">STEP {n} OF 4</div>{uiblock(n)}</div></div>')

def bigtoggle(id, x, y, w, h, on=True):
    return (f'<div class="btg {"on" if on else ""}" id="{id}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{h//2}px"><i style="width:{h-48}px;height:{h-48}px"></i></div>')

def chat():
    return (piece('<div class="mini"><b>Camera roll sharing suggestions</b><div class="tg2" id="tg7"><i></i></div></div>', "outb", 110, 650, 860, 240, 1.0, "#FBF8EF", 91, 6, 3)
            + '<div class="mavt" id="mav">M</div><div class="dots2" id="dots2"><i></i><i></i><i></i></div>'
            + "".join(strip(f"al{k}", "ALLOW", 250 + (k - 1) * 255, 1070, 235, 112, (-3, 2, -2)[k - 1], YEL, size=88, seed=70 + k, z=6) for k in (1, 2, 3)))

NEWS = (piece('<div class="npr"></div>', 'np1', -60, 240, 620, 480, -5, '#E3D3AE', 101, 9, 1) + piece('<div class="npr"></div>', 'np2', 520, 330, 640, 520, 4, '#DFCDA5', 102, 9, 1)
        + piece('<div class="npr"></div>', 'np3', -40, 880, 560, 470, 3, '#E3D3AE', 103, 9, 1) + piece('<div class="npr"></div>', 'np4', 560, 940, 600, 440, -3, '#DFCDA5', 104, 9, 1))

markup = f'''
<div class="bgl" id="bgl"><div class="news" id="news"></div><div class="news2" id="news2"></div><div class="dots"></div><div id="npw">{NEWS}</div></div>
<div class="sc" id="s1" style="opacity:1;visibility:visible">{hookblock("")}</div>
<div class="sc" id="s2"><div class="cam" id="c2">
 {strip("t2", "ONLY IF YOU TAPPED", 90, 300, 900, 150, -1.2, YEL, size=112, seed=11, z=5)}
 {piece('<div class="mp"></div>', "dlg2", 90, 520, 900, 660, 0.5, CRM, 12, 8, 2)}
 <div id="stk">{print_(0, "d1", 160, 560, 240, 320, -8, 3, False, False)}{print_(1, "d2", 360, 540, 260, 340, 2, 4, False, False)}{print_(3, "d3", 580, 560, 240, 320, 9, 3, False, False)}</div>
 {strip("nb", "Not now", 125, 940, 280, 190, 0, "#D8CFB8", "#5d554a", "IDisp", 54, 21, z=4)}
 {strip("b2", "ALLOW", 430, 930, 470, 210, -1.5, BLK, "#fff", "BS", 190, 22, z=5)}
 <div class="ring" id="ring"></div><div class="fing" id="fing"></div><div class="tiny" id="ill2">illustration</div></div></div>
<div class="sc" id="s3"><div class="cam" id="c3">
 {strip("t3a", "HERE'S HOW", 90, 292, 900, 178, -1.2, YEL, size=150, seed=31, z=5)}
 {strip("t3b", "to stop it", 190, 488, 700, 170, 1.4, BLK, "#fff", "Gloock", 130, 32, z=6)}
 {piece(bigtoggle("bigtg", 70, 35, 700, 330, True), "tgp", 110, 690, 860, 400, -.8, CRM, 33, 8, 2)}
 {strip("tlab", "Camera roll sharing suggestions", 90, 1120, 900, 80, 0.8, YEL, size=32, font="PlexM", seed=34, z=5)}
 <div class="tiny" id="ill3" style="top:1246px;display:none"></div></div></div>
{stepscene(1, ["PROFILE", "PICTURE"])}
{stepscene(2, ["SETTINGS &amp;", "PRIVACY"])}
{stepscene(3, ["SETTINGS"])}
{stepscene(4, ["CAMERA ROLL", "SHARING", "SUGGESTIONS"])}
<div class="sc" id="s5"><div class="cam" id="c5">
 {strip("t5", "SWITCH IT OFF", 90, 300, 900, 170, -1.2, YEL, size=150, seed=51, z=5)}
 {piece(bigtoggle("bigtg2", 50, 50, 780, 420, True), "tgp2", 100, 520, 880, 520, .6, CRM, 52, 8, 2)}
 <div class="offst" id="offw"><span class="scr" id="scr0">X#7</span><span class="scr" id="scr1">0F?</span><span class="scr" id="scr2">OF#</span><span class="offf" id="offf">OFF</span></div></div></div>
<div class="sc" id="s6"><div class="cam" id="c6">
 {strip("t6a", "META SAYS", 290, 296, 500, 110, -2, BLK, "#fff", "Gloock", 70, 61, z=6)}
 {piece('<div class="optin" id="optin">OPT-IN</div>', "pin6", 110, 440, 860, 420, -1, CRM, 62, 8, 3)}
 {strip("t6b", "NOT USED FOR ADS", 90, 890, 900, 150, 1.0, YEL, size=120, seed=63, z=5)}
 {strip("t6c", "Meta newsroom, April 2026 · EU and UK", 140, 1090, 800, 64, -0.6, "#EADFC2", "#3b342a", "IDisp", 32, 64, z=4)}</div></div>
<div class="sc" id="s7"><div class="cam" id="c7">
 {strip("t7a", "SEND THIS TO SOMEONE", 90, 292, 900, 120, -1.0, YEL, size=92, seed=71, z=5)}
 {strip("t7b", "who always taps Allow", 120, 426, 840, 120, 1.0, BLK, "#fff", "Gloock", 76, 72, z=6)}
 {chat()}</div></div>
<div class="sc" id="sH">{hookblock("H")}</div>
<div class="lens" id="lens1"></div><div class="lens l2" id="lens2"></div>
<div class="grain"></div>
'''

_noise = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .25  0 0 0 0 .18  0 0 0 0 .1  0 0 0 .9 0'/></filter><rect width='400' height='400' filter='url(%23n)'/></svg>")
_fib = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='f'><feTurbulence type='fractalNoise' baseFrequency='.02 .5' numOctaves='3'/><feColorMatrix values='0 0 0 0 .5  0 0 0 0 .38  0 0 0 0 .2  0 0 0 .6 0'/></filter><rect width='300' height='300' filter='url(%23f)'/></svg>")

styles = r'''
@font-face{font-family:"BS";src:url("assets/fonts/BigShoulders-Bold.ttf");font-weight:700}
@font-face{font-family:"Gloock";src:url("assets/fonts/Gloock-Regular.ttf")}
@font-face{font-family:"PlexM";src:url("assets/fonts/IBMPlexMono-Bold.ttf");font-weight:700}
:root{--ink:#17130F;--yel:#F2C230;--red:#B6402B;--lime:#9BE22E}
html,body,#root{background:#B8955F}
.bgl{position:absolute;left:0;top:0;width:1080px;height:1920px;background:linear-gradient(180deg,#DCCBA3,#CBB184 60%,#BC9D6C);overflow:hidden}
.news{position:absolute;left:-60px;top:-60px;width:1200px;height:2040px;opacity:.55;
 background:repeating-linear-gradient(0deg,rgba(60,42,22,.38) 0 3px,transparent 3px 11px) 0 0/290px 100% no-repeat,
 repeating-linear-gradient(0deg,rgba(60,42,22,.34) 0 3px,transparent 3px 11px) 330px 0/290px 100% no-repeat,
 repeating-linear-gradient(0deg,rgba(60,42,22,.30) 0 3px,transparent 3px 11px) 660px 0/290px 100% no-repeat,
 repeating-linear-gradient(0deg,rgba(60,42,22,.3) 0 3px,transparent 3px 11px) 990px 0/200px 100% no-repeat;
 -webkit-mask-image:radial-gradient(ellipse 90% 70% at 50% 45%,#000 40%,rgba(0,0,0,.25) 100%)}
.news2{position:absolute;left:-60px;top:-60px;width:1200px;height:2040px;opacity:.5;background:repeating-linear-gradient(90deg,transparent 0 46px,#C9AE80 46px 54px),repeating-linear-gradient(90deg,transparent 0 71px,#C9AE80 71px 77px);-webkit-mask-image:radial-gradient(ellipse 90% 70% at 50% 45%,#000 40%,rgba(0,0,0,.25) 100%)}
.news:before{content:"";position:absolute;left:60px;top:300px;width:420px;height:300px;background:#2a1f12;opacity:.28}
.news:after{content:"";position:absolute;left:560px;top:1000px;width:520px;height:360px;background:#2a1f12;opacity:.22}
.dots{position:absolute;inset:0;background:radial-gradient(circle,rgba(40,25,10,.34) 2px,transparent 2.6px) 0 0/16px 16px;-webkit-mask-image:radial-gradient(ellipse 70% 55% at 50% 100%,#000,transparent);opacity:.7}
.grain{position:absolute;left:0;top:0;width:1080px;height:1920px;background:url("''' + _noise + r'''");mix-blend-mode:multiply;opacity:.55;z-index:70;pointer-events:none}
.sc{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0;visibility:hidden}
.cam{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 760px}
.pcw{position:absolute}
.npr{position:absolute;inset:0;filter:sepia(.5);
 background:repeating-linear-gradient(0deg,rgba(40,28,14,.5) 0 3px,transparent 3px 11px) 26px 130px/calc(50% - 40px) calc(100% - 160px) no-repeat,
 repeating-linear-gradient(0deg,rgba(40,28,14,.5) 0 3px,transparent 3px 11px) calc(50% + 14px) 130px/calc(50% - 40px) calc(100% - 160px) no-repeat}
.npr:before{content:"";position:absolute;left:26px;top:28px;width:68%;height:62px;background:#2a1f12;opacity:.78}
.npr:after{content:"";position:absolute;right:26px;top:36px;width:22%;height:46px;background:radial-gradient(circle,rgba(30,18,6,.7) 2px,transparent 2.6px) 0 0/8px 8px}
.pc{position:absolute;inset:0;filter:drop-shadow(0 3px 3px rgba(30,18,6,.35)) drop-shadow(0 16px 16px rgba(30,18,6,.28)) drop-shadow(0 34px 34px rgba(30,18,6,.22))}
.pcb{position:absolute;inset:0;overflow:hidden}
.paperfx{position:absolute;inset:0;background:url("''' + _fib + r'''");mix-blend-mode:multiply;opacity:.55;pointer-events:none;z-index:9}
.stx{position:absolute;left:0;top:0;width:100%;height:100%;white-space:nowrap;letter-spacing:-.005em;text-transform:uppercase;font-weight:700}
.stx[style*="Gloock"]{text-transform:none;letter-spacing:-.01em}
.stx[style*="PlexM"]{letter-spacing:-.02em}
.tape{position:absolute;background:rgba(232,214,160,.82);box-shadow:0 2px 4px rgba(30,18,6,.3);z-index:12}
.pic{position:absolute;overflow:hidden;background:#fff}
.pimg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:grayscale(.25) sepia(.45) contrast(1.08) brightness(1.14)}
.ht2{position:absolute;inset:0;background:radial-gradient(circle,rgba(30,18,6,.42) 1.8px,transparent 2.4px) 0 0/8px 8px;mix-blend-mode:multiply;opacity:.3}
.pvig{position:absolute;inset:0;background:radial-gradient(120% 90% at 50% 40%,transparent 55%,rgba(0,0,0,.32))}
.stamp{position:absolute;left:50%;top:60%;transform:translate(-50%,-50%) rotate(-9deg);font:700 44px BS;letter-spacing:.04em;color:var(--red);border:6px solid var(--red);padding:2px 16px 4px;border-radius:8px;mix-blend-mode:multiply;opacity:.93;white-space:nowrap;z-index:11}
.prn .stamp{font-size:21px;border-width:3px;padding:1px 8px 2px;opacity:.78;letter-spacing:.06em}
.fbs{position:absolute;z-index:20;border-radius:50%;background:#fff;box-shadow:0 0 0 6px #fff,0 8px 20px rgba(30,18,6,.45);overflow:hidden}.fbs img{width:100%;height:100%;padding:6px}
.pnum{position:absolute;left:92px;top:340px;font:700 440px BS;line-height:400px;color:var(--red);mix-blend-mode:multiply;opacity:.95;letter-spacing:-.02em}
.of4{position:absolute;left:360px;top:288px;font:700 26px PlexM;letter-spacing:.1em;color:#3b2a14}
.uibody{position:absolute;inset:0}
.sk{display:block;position:absolute;left:44px;height:24px;border-radius:12px;background:#D9D0BA;text-decoration:none}
.fbtop{position:absolute;left:0;top:0;width:100%;height:180px;background:#EFE7D2}
.fbsm{position:absolute;left:34px;top:34px;width:112px;height:112px;border-radius:50%;background:#fff;box-shadow:0 4px 10px rgba(30,18,6,.3);overflow:hidden}.fbsm img{width:100%;height:100%;padding:6px}
.avt{position:absolute;right:50px;top:14px;width:150px;height:150px;border-radius:50%;background:linear-gradient(160deg,#C99A62,#8C5A2B);overflow:hidden}
.avh{position:absolute;left:50px;top:28px;width:50px;height:50px;border-radius:50%;background:#F5E7CB}.avb{position:absolute;left:28px;top:90px;width:94px;height:80px;border-radius:50% 50% 0 0;background:#F5E7CB}
.hrow{position:absolute;left:30px;right:30px;height:100px;border-radius:14px;background:linear-gradient(transparent 12%,rgba(242,194,48,.9) 12%,rgba(242,194,48,.9) 88%,transparent 88%);display:flex;align-items:center;padding:0 24px;gap:20px}
.hrow b{font:700 66px BS;letter-spacing:.005em;text-transform:uppercase}
.hrow.tall{height:190px}.hrow.tall b{font-size:58px;line-height:60px;flex:1}
.circ{position:absolute;border:9px solid var(--red);border-radius:50%/60%;transform:rotate(-2deg);opacity:0}
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
.mavt{position:absolute;left:100px;top:1080px;width:120px;height:120px;border-radius:50%;background:var(--yel);font:700 90px BS;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 6px #fff,0 8px 20px rgba(30,18,6,.45);opacity:0}
.dots2{position:absolute;left:250px;top:1086px;width:230px;height:112px;background:#FBF8EF;border-radius:50px 50px 50px 12px;box-shadow:0 8px 18px rgba(30,18,6,.4);display:flex;align-items:center;justify-content:center;gap:18px;opacity:0}
.dots2 i{display:block;width:26px;height:26px;border-radius:50%;background:var(--ink)}
.ring{position:absolute;left:720px;top:940px;width:110px;height:110px;border-radius:50%;border:10px solid var(--red);opacity:0;z-index:30}
.fing{position:absolute;left:740px;top:1020px;width:100px;height:100px;border-radius:50%;background:rgba(23,19,15,.8);opacity:0;z-index:30}
.tiny{position:absolute;left:65px;width:950px;text-align:center;font:700 26px PlexM;letter-spacing:.06em;color:#3b2a14;text-transform:uppercase}
#ill2{top:1150px}
.lens{position:absolute;left:-700px;top:560px;width:620px;height:620px;border-radius:50%;background:radial-gradient(circle at 40% 40%,rgba(30,18,6,.55),rgba(30,18,6,.1));filter:blur(46px);opacity:0;z-index:60;pointer-events:none}
.lens.l2{top:760px;width:520px;height:520px}
'''
styles = styles.replace('font-family:{font}', 'font-family:{font}')

js = r'''
const T=%s;
const EA="sine.inOut",EO="power2.out",EX="expo.out";
const Q=s=>document.querySelector(s), QA=s=>[...document.querySelectorAll(s)];
const sceneIn=(id,t)=>tl.fromTo('#'+id,{autoAlpha:0},{autoAlpha:1,duration:.18,ease:EA},t);
const sceneOut=(id,t)=>tl.to('#'+id,{autoAlpha:0,duration:.1,ease:EA},t-.1);
const push=(cam,t0,t1,s0,s1)=>tl.fromTo('#'+cam,{scale:s0||1},{scale:s1||1.06,duration:Math.max(.3,t1-t0),ease:EA},t0);
// a torn strip slams in (scale 1.35 -> 1, blur -> sharp) and its text is typed in with a hard wipe
const slamP=(id,t,dir)=>{ tl.fromTo('#'+id,{scale:1.35,opacity:0,filter:"blur(12px)",rotation:'+=' + (dir||5)},{scale:1,opacity:1,filter:"blur(0px)",rotation:'-=' + (dir||5),duration:.42,ease:EX,transformOrigin:"50%% 50%%"},t);
  tl.fromTo('#'+id+'t',{clipPath:"inset(0 100%% 0 0)"},{clipPath:"inset(0 0%% 0 0)",duration:.34,ease:"steps(14)"},t+.12); };
const lensCross=(id,t,dur)=>{ tl.fromTo('#'+id,{x:0,opacity:0},{opacity:.6,duration:dur*.3,ease:EA},t); tl.to('#'+id,{x:1900,duration:dur,ease:"power1.inOut"},t); tl.to('#'+id,{opacity:0,duration:dur*.25,ease:EA},t+dur*.75); };
// slow parallax of the newspaper layer over the whole video
tl.fromTo('#news,#news2',{x:0,y:0},{x:-70,y:-60,duration:D,ease:"none"},0);
tl.fromTo('#npw',{x:0,y:0},{x:-40,y:-30,duration:D,ease:"none"},0);
function hook(sfx,t0,t1){
  const h='hcam'+sfx;
  tl.fromTo('#pr1'+sfx,{y:36,rotation:-10},{y:0,rotation:-8,duration:.6,ease:EX},t0);
  tl.fromTo('#pr3'+sfx,{y:44,rotation:11},{y:0,rotation:9,duration:.6,ease:EX},t0+.05);
  tl.fromTo('#pr2'+sfx,{y:30,scale:.97},{y:0,scale:1,duration:.6,ease:EX},t0+.1);
  tl.fromTo('#fbs'+sfx,{scale:.85,rotation:-20},{scale:1,rotation:-8,duration:.5,ease:"back.out(2.2)"},t0+.15);
  if(sfx!='H') tl.fromTo(['#hA'+sfx,'#hB'+sfx,'#hC'+sfx],{x:-26},{x:0,duration:.5,ease:EX,stagger:.06},t0);
  if(sfx=='H') push(h,t0,t1,1.04,1.0); else push(h,t0,t1,1,1.04);
  [1,3].forEach((k,i)=>tl.fromTo('#pr'+k+sfx+'s',{scale:1.14},{scale:1,duration:.3,ease:"power4.out"},t0+.55+i*.3));
  tl.fromTo('#hC'+sfx,{scale:1.07},{scale:1,duration:.5,ease:EX,immediateRender:false,transformOrigin:"50%% 50%%"},T.slam1);
    if(sfx!='H'){ const m=t0+1.25; tl.to('#pr2'+sfx,{scale:1.06,rotation:-1,duration:.55,ease:EA,yoyo:true,repeat:1},m); tl.to('#pr1'+sfx,{x:-16,rotation:-11,duration:.55,ease:EA,yoyo:true,repeat:1},m); tl.to('#pr3'+sfx,{x:16,rotation:12,duration:.55,ease:EA,yoyo:true,repeat:1},m+.05); [['hA',-5],['hB',3],['hC',3]].forEach((k,i)=>tl.to('#'+k[0]+sfx,{y:k[1],duration:.7,ease:EA,yoyo:true,repeat:1},t0+.6+i*.12)); }
  if(sfx=='H') tl.fromTo('#cards'+sfx,{x:-16},{x:0,duration:t1-t0,ease:EA},t0); else tl.fromTo('#cards'+sfx,{x:0},{x:-16,duration:t1-t0,ease:EA},t0);
  (sfx=='H'?[]:[['pr1',-12,.7],['pr3',-10,.85],['pr2',-14,.75]]).forEach(a=>tl.to('#'+a[0]+sfx,{y:a[1],duration:1.3,ease:EA,yoyo:true,repeat:Math.max(1,Math.floor((t1-t0-a[2])/1.3)-1)},t0+a[2]));
}
hook('',0,T.s2+.1);
lensCross('lens1',T.s2-.45,.55);
sceneOut('s1',T.s2-.02);
// ---------- S2
sceneIn('s2',T.s2); push('c2',T.s2,T.s3,1,1.04);
slamP('t2',T.s2+.02,-4);
tl.fromTo('#dlg2',{y:110,scale:.94,opacity:0},{y:0,scale:1,opacity:1,duration:.5,ease:EX},T.s2+.1);
tl.fromTo('#stk .prn',{y:60,opacity:0},{y:0,opacity:1,duration:.45,ease:EX,stagger:.07},T.s2+.25);
tl.fromTo('#nb',{opacity:0,y:30},{opacity:1,y:0,duration:.35,ease:EX},T.s2+.4);
slamP('b2',T.s2+.5,4);
tl.fromTo('#fing',{opacity:0,y:60},{opacity:1,y:0,duration:.4,ease:EO},T.tapAllow-.4);
tl.to('#b2',{scale:.94,duration:.14,ease:EA,transformOrigin:"50%% 50%%"},T.tapAllow);
tl.fromTo('#ring',{opacity:.95,scale:.5},{opacity:0,scale:2.6,duration:.7,ease:EO},T.tapAllow+.02);
tl.to('#b2',{scale:1.0,duration:.3,ease:EA},T.tapAllow+.14);
tl.to('#fing',{opacity:0,duration:.3,ease:EA},T.tapAllow+.45);
tl.fromTo('#ill2',{opacity:0},{opacity:1,duration:.3},T.s2+.6);
sceneOut('s2',T.s3-.02);
// ---------- S3
sceneIn('s3',T.s3); push('c3',T.s3,T.p1,1,1.04);
slamP('t3a',T.s3+.02,-4); slamP('t3b',T.s3+.2,5);
tl.fromTo('#tgp',{scale:.88,opacity:0,y:60},{scale:1,opacity:1,y:0,duration:.55,ease:EX},T.s3+.25);
slamP('tlab',T.s3+.5,-3);
tl.to('#tgp',{y:-10,duration:T.p1-T.s3,ease:EA},T.s3+.8);
sceneOut('s3',T.p1-.02);
// ---------- steps
const st=[['p1','p2','pc1','pn1','sl10','sl11','ui1','hot1','circ1'],['p2','p3','pc2','pn2','sl20','sl21','ui2','hot2','circ2'],['p3','p4','pc3','pn3','sl30',null,'ui3','hot3','circ3'],['p4','s5','pc4','pn4','sl40','sl41','ui4','hot4','circ4']];
st.forEach((s,i)=>{
  const t0=T[s[0]], t1=T[s[1]];
  sceneIn(s[0],t0); push(s[2],t0,t1+.1,1,1.05);
  tl.fromTo('#'+s[3],{scale:1.4,opacity:0,filter:"blur(14px)"},{scale:1,opacity:.95,filter:"blur(0px)",duration:.4,ease:EX,transformOrigin:"30%% 50%%"},t0+.02);
  slamP(s[4],t0+.08,-4); if(s[5]) slamP(s[5],t0+.2,4);
  if(i==3){ slamP('sl42',t0+.32,-3); }
  tl.fromTo('#'+s[6],{y:100,opacity:0,scale:.95},{y:0,opacity:1,scale:1,duration:.45,ease:EX},t0+.1);
  tl.fromTo('#'+s[8],{opacity:0,scale:1.3},{opacity:1,scale:1,duration:.3,ease:EX,transformOrigin:"50%% 50%%"},t0+.45);
  if(s[1]!='s5') sceneOut(s[0],t1-.02);
});
sceneOut('p4',T.s5-.02);
// ---------- S5 switch OFF: the proof
sceneIn('s5',T.s5); push('c5',T.s5,T.s6,1,1.05);
slamP('t5',T.s5+.02,-4);
tl.fromTo('#tgp2',{scale:.9,opacity:0},{scale:1,opacity:1,duration:.4,ease:EX},T.s5+.05);
tl.to('#bigtg2 i',{right:384,duration:.34,ease:"power3.inOut"},T.flip);
tl.to('#bigtg2',{backgroundColor:"#9BE22E",duration:.34,ease:"power3.inOut"},T.flip);
tl.fromTo('#bigtg2',{boxShadow:"0 0 0 0 rgba(155,226,46,.9)"},{boxShadow:"0 0 0 50px rgba(155,226,46,0)",duration:.6,ease:EO,immediateRender:false},T.flip+.3);
[0,1,2].forEach(i=>{ tl.set('#scr'+i,{opacity:1},T.flip+.34+i*.07); tl.set('#scr'+i,{opacity:0},T.flip+.34+i*.07+.07); });
tl.fromTo('#offf',{scale:1.4,opacity:0,filter:"blur(14px)"},{scale:1,opacity:1,filter:"blur(0px)",duration:.4,ease:EX,transformOrigin:"50%% 50%%"},T.flip+.55);
tl.to('#tgp2',{y:-8,duration:T.s6-T.s5,ease:EA},T.s5+.5);
sceneOut('s5',T.s6-.02);
// ---------- S6 Meta
sceneIn('s6',T.s6); push('c6',T.s6,T.s7,1,1.04);
slamP('t6a',T.s6+.02,-4);
tl.fromTo('#pin6',{scale:1.25,opacity:0,filter:"blur(14px)"},{scale:1,opacity:1,filter:"blur(0px)",duration:.45,ease:EX,transformOrigin:"50%% 50%%"},T.s6+.1);
slamP('t6b',T.s6+.55,4);
slamP('t6c',T.s6+1.0,-2);
lensCross('lens2',T.s7-.5,.55);
sceneOut('s6',T.s7-.02);
// ---------- S7 send
sceneIn('s7',T.s7); push('c7',T.s7,T.end,1,1.04);
slamP('t7a',T.s7+.02,-4); slamP('t7b',T.s7+.2,4);
tl.fromTo('#outb',{x:90,y:30,opacity:0,scale:.94},{x:0,y:0,opacity:1,scale:1,duration:.55,ease:EX},T.s7+.3);
tl.fromTo('#mav',{opacity:0,scale:.6},{opacity:1,scale:1,duration:.4,ease:"back.out(2)"},T.s7+1.0);
tl.fromTo('#dots2',{opacity:0,scale:.8},{opacity:1,scale:1,duration:.35,ease:EO},T.s7+1.1);
tl.to('#dots2 i',{y:-10,duration:.28,ease:EA,yoyo:true,repeat:3,stagger:.09},T.s7+1.2);
tl.to('#dots2',{opacity:0,duration:.18},T.s7+1.75);
[1,2,3].forEach((k,i)=>slamP('al'+k,T.s7+1.8+i*.28,(i%%2?4:-4)));
tl.to('#tg7 i',{left:5,duration:.01},T.s7);
sceneOut('s7',T.loop-.1);
// ---------- loop back to frame 0
tl.set('#sH',{autoAlpha:0},0);
tl.fromTo('#sH',{autoAlpha:0},{autoAlpha:1,duration:.3,ease:EA},T.loop-.1);
hook('H',T.loop,D);
'''

html = open(H + "/shell8.html").read()
html = (html.replace("__STYLES__", styles).replace("__MARKUP__", markup).replace("__CHROME__", "").replace("__SCRIPTS__", "")
        .replace("__D__", str(D)).replace("__CUES__", json.dumps(dict(lines=lines, D=D)))
        .replace("__CALLS__", js.replace("const T=%s;", "const T=" + json.dumps(T) + ";").replace("%%", "%")).replace("__NSC__", "1"))
html = re.sub(r'<div class="abs clip" id="gd".*?</div>', '', html, flags=re.S)
html = html.replace('font-family:{font}', '')
os.makedirs(H + "/hf", exist_ok=True)
open(H + "/hf/index.html", "w").write(html)
print("D=", D, [(l["n"], l["start"], l["end"]) for l in lines])
print("scenes", {k: round(v, 2) for k, v in B.items()})
if "--render" in sys.argv:
    name = sys.argv[sys.argv.index("--render") + 1]
    env = dict(os.environ, HYPERFRAMES_NO_TELEMETRY="1", DO_NOT_TRACK="1")
    r = subprocess.run(["npx", "--no-install", "hyperframes", "render", "-o", f"{H}/out/{name}.mp4", "--format", "mp4", "--quiet"],
                       cwd=H + "/hf", env=env, capture_output=True, text=True, timeout=2400)
    print(r.stdout[-400:], r.stderr[-800:])
