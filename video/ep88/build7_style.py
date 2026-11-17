
styles = r'''
@font-face{font-family:"BS";src:url("assets/fonts/BigShoulders-Bold.ttf");font-weight:700}
@font-face{font-family:"Gloock";src:url("assets/fonts/Gloock-Regular.ttf")}
@font-face{font-family:"PlexM";src:url("assets/fonts/IBMPlexMono-Bold.ttf");font-weight:700}
:root{--ink:#17130F;--yel:#F2C230;--red:#B6402B;--lime:#9BE22E}
html,body,#root{background:#8c6f48}
#world{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 960px}
.bgl{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden;background:#a07f52}
.bgimg{position:absolute;left:-900px;top:0;width:2880px;height:1920px}
#flys,#fgl{position:absolute;left:0;top:0;width:1080px;height:1920px;pointer-events:none}
.sset{position:absolute;left:0;top:0;width:1080px;height:1920px;pointer-events:none}
.dc{position:absolute}
.dc.fly{opacity:0}
.fgs{position:absolute;left:0;top:0;opacity:0}
.sc{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0;visibility:hidden}
.cam{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 760px}
.pcw{position:absolute}
.pbg{position:absolute;max-width:none;pointer-events:none}
.stx{position:absolute;left:50%;transform:translateX(-50%);top:0;width:auto;height:100%;white-space:nowrap;letter-spacing:-.005em;text-transform:uppercase;font-weight:700;filter:url(#ink);text-shadow:1.7px 1.2px 0 rgba(182,64,43,.34)}
.stx.dk{mix-blend-mode:multiply}
.stx.lt{text-shadow:1.4px 1px 0 rgba(0,0,0,.3)}
.stx[style*="Gloock"]{text-transform:none;letter-spacing:-.01em}
.stx[style*="PlexM"]{letter-spacing:-.02em}
.rl .stx{text-transform:none!important}
.tape{position:absolute;max-width:none;z-index:12}
.phimg{position:absolute;max-width:none;object-fit:cover}
.pvig{position:absolute;background:radial-gradient(120% 90% at 50% 40%,transparent 60%,rgba(0,0,0,.3))}
.stp{position:absolute;white-space:nowrap;mix-blend-mode:multiply;letter-spacing:.06em;text-transform:uppercase}
.inkA{filter:url(#stA)}.inkB{filter:url(#stB)}.inkAB{filter:url(#stA)}
.fbs{position:absolute;z-index:20;border-radius:50%;background:#fff;box-shadow:0 0 0 6px #fff,0 8px 20px rgba(30,18,6,.45);overflow:hidden}.fbs img{width:100%;height:100%;padding:6px}
.pnum{position:absolute;top:340px;font:700 440px BS;line-height:400px;color:var(--red);opacity:.95;letter-spacing:-.02em;mix-blend-mode:multiply;filter:url(#ink)}
.of4{position:absolute;top:302px;font:700 26px PlexM;letter-spacing:.1em;color:#3b2a14}
.uibody{position:absolute;left:26px;top:24px;right:26px;bottom:28px;background:#f4f1e8;border-radius:22px;overflow:hidden;filter:sepia(.3) contrast(1.12) saturate(.85)}
.copy{position:absolute;left:26px;top:24px;right:26px;bottom:28px;border-radius:22px;pointer-events:none;
 background:radial-gradient(circle at 2.5px 2.5px,rgba(20,16,12,.22) 1.1px,transparent 1.6px) 0 0/5px 5px,linear-gradient(90deg,rgba(0,0,0,.09),transparent 7%,transparent 93%,rgba(0,0,0,.1)),linear-gradient(0deg,rgba(0,0,0,.07),transparent 14%);mix-blend-mode:multiply}
.mkw{position:absolute;z-index:30;pointer-events:none}
.uihd{position:absolute;left:30px;top:26px;font:800 44px IDisp;color:#1b1814}
.uir{position:absolute;left:24px;right:24px;height:106px;display:flex;align-items:center;justify-content:space-between;padding:0 22px;font:700 40px IDisp;color:#34302a;border-bottom:2px solid rgba(40,34,26,.18);gap:14px}
.uir.hot{background:rgba(242,194,48,.6);border-radius:10px;color:#17130F;border-bottom-color:transparent}
.uil{white-space:nowrap;flex:1}
.chev{font:400 60px IDisp;color:#6d6558;line-height:60px}
.fbtop{position:absolute;left:0;top:0;width:100%;height:130px;background:#ece7d8;border-bottom:2px solid rgba(40,34,26,.2)}
.fbsm{position:absolute;left:28px;top:20px;width:90px;height:90px;border-radius:50%;background:#fff;overflow:hidden}.fbsm img{width:100%;height:100%;padding:4px}
.ico{position:absolute;top:34px;width:62px;height:62px;border-radius:50%;background:#cfc7b3}.ico:nth-of-type(1){right:262px}.ico:nth-of-type(2){right:186px}
.avt{position:absolute;right:46px;top:12px;width:106px;height:106px;border-radius:50%;background:linear-gradient(160deg,#C99A62,#8C5A2B);overflow:hidden}
.avh{position:absolute;left:33px;top:20px;width:40px;height:40px;border-radius:50%;background:#F5E7CB}.avb{position:absolute;left:18px;top:64px;width:70px;height:56px;border-radius:50% 50% 0 0;background:#F5E7CB}
.comp{position:absolute;left:20px;right:20px;top:146px;height:76px;display:flex;align-items:center;gap:16px;font:600 32px IDisp;color:#6d6558;border-bottom:2px solid rgba(40,34,26,.16)}
.cav{width:56px;height:56px;border-radius:50%;background:#c9bda3}
.feedimg{position:absolute;left:0;top:232px;width:100%;height:240px;object-fit:cover}
.tapr{position:absolute;right:120px;top:130px;width:90px;height:90px;border-radius:50%;border:8px solid var(--red);opacity:0}
.tg2{position:relative;width:132px;height:74px;border-radius:37px;background:#CBBFA3;flex:none}
.tg2 i{position:absolute;left:4px;top:4px;width:66px;height:66px;border-radius:50%;background:#fff;box-shadow:0 4px 10px rgba(14,14,14,.35)}
.tg2.on{background:#2a2118}.tg2.on i{left:auto;right:4px}
.uinote{position:absolute;left:0;width:100%;top:318px;text-align:center;font:700 22px PlexM;color:#4a3a26}
.btg{position:absolute;background:#CBBFA3;box-shadow:inset 0 -10px 0 rgba(0,0,0,.10)}
.btg i{position:absolute;left:24px;top:24px;border-radius:50%;background:#fff;box-shadow:0 12px 26px rgba(14,14,14,.4)}
.btg.on{background:#2a2118}.btg.on i{left:auto;right:24px}
.mini{position:absolute;inset:0;display:flex;align-items:center;justify-content:space-between;padding:0 50px;gap:20px}
.mini b{font:700 68px BS;line-height:68px;text-transform:uppercase;filter:url(#ink)}
.mini .tg2{width:190px;height:106px;border-radius:53px}.mini .tg2 i{width:94px;height:94px}
.mp{position:absolute;inset:0}
.optin{position:absolute;left:0;top:0;width:100%;height:100%;font:400 232px Gloock;line-height:430px;text-align:center;color:var(--ink);letter-spacing:-.03em;filter:url(#ink);mix-blend-mode:multiply}
.offst{position:absolute;left:90px;top:1050px;width:900px;height:140px;text-align:center;font-family:BS;font-weight:700;font-size:170px;line-height:140px}
.offst span{position:absolute;left:0;width:100%;top:0;opacity:0}
.offf{background:var(--lime);color:var(--ink);border:8px solid var(--ink);border-radius:30px;padding:0 60px;width:auto!important;left:50%!important;transform:translateX(-50%) rotate(-4deg)!important;box-shadow:8px 10px 0 var(--ink)}
.offst .scr{color:#4a3a26}
.burst{position:absolute;left:340px;top:640px;width:400px;height:400px;border-radius:50%;background:radial-gradient(circle,rgba(30,18,6,.55) 2.4px,transparent 3px) 0 0/16px 16px;-webkit-mask-image:radial-gradient(circle,transparent 30%,#000 60%,transparent 100%);opacity:0}
.mavt{position:absolute;left:100px;top:1080px;width:120px;height:120px;border-radius:50%;background:var(--yel);font:700 90px BS;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 6px #fff,0 8px 20px rgba(30,18,6,.45);opacity:0}
.dots2{position:absolute;left:250px;top:1086px;width:230px;height:112px;background:#FBF8EF;border-radius:50px 50px 50px 12px;box-shadow:0 8px 18px rgba(30,18,6,.4);display:flex;align-items:center;justify-content:center;gap:18px;opacity:0}
.dots2 i{display:block;width:26px;height:26px;border-radius:50%;background:var(--ink)}
.ring{position:absolute;left:760px;top:940px;width:110px;height:110px;border-radius:50%;border:10px solid var(--red);opacity:0;z-index:30}
.fing{position:absolute;left:780px;top:1020px;width:100px;height:100px;border-radius:50%;background:rgba(23,19,15,.8);opacity:0;z-index:30}
.sheet{position:absolute;left:0;top:-120px;width:1470px;height:2290px;max-width:none;z-index:80;opacity:0;pointer-events:none}
.ush{position:absolute;left:0;top:-120px;width:1470px;height:2290px;max-width:none;z-index:4;opacity:0;pointer-events:none}
.grainw{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden;z-index:90;pointer-events:none}
.grain{position:absolute;left:-40px;top:-40px;width:1160px;height:2000px;max-width:none;mix-blend-mode:overlay;opacity:.24;pointer-events:none}
'''
