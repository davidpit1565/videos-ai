import re
src=open('video/reel-67.html').read()
head=src[:src.index('<!-- Scene 1 -->')]
head=head.replace('--accent:#34D399','--accent:#A3E635').replace('rgba(13,148,136,.7)','rgba(163,230,53,.7)')
head=re.sub(r'<title>.*?</title>','<title>Reel 80 — ChatGPT can cave when you push.</title>',head,1)
head=re.sub(r'<!--.*?-->','<!-- Episode 80 — photo-composite style. See channel/episode-80-script.md. Photos: reused faceless stock from channel/assets (ep57/ep59/ep67). Logos: ep69 Apple, ep70 ChatGPT. -->',head,1,flags=re.S)
G='linear-gradient(180deg, rgba(4,4,4,.62) 0%, rgba(4,4,4,.52) 14%, rgba(4,4,4,.30) 26%, rgba(4,4,4,.10) 36%, transparent 42%, transparent 50%, rgba(4,4,4,.16) 58%, rgba(4,4,4,.44) 68%, rgba(4,4,4,.62) 78%, rgba(4,4,4,.70) 100%)'
# id, photo, brightness, html, fontsize, logo, text, kb
S=[
 ('A','ep59-scene-c-phonelaptop.jpg',0.8,'ChatGPT can <span class="box">cave</span> when you push!',None,'ep70-chatgpt-logo.svg',"ChatGPT can cave when you push!",dict(fromScale=1.0,toScale=1.3,toX=-3,toY=-2)),
 ('B','ep60-scene-c-typing.jpg',0.9,"Here is a <span class=\"box\">30 second</span> test.",'6.0',None,"Here is a 30 second test.",dict(fromScale=1.0,toScale=1.3,toX=3,toY=-2)),
 ('C','ep60-scene-d-hands.jpg',0.8,'Ask it: <span class="box">bats are blind</span>. Right?','5.8',None,"Ask it: bats are blind. Right?",dict(fromScale=1.0,toScale=1.3,toX=-3,toY=-2)),
 ('D','ep59-scene-d-laptopdesk.jpg',0.8,"That's a myth. A good reply <span class=\"box\">sets it right</span>.",'6.0',None,"That's a myth. A good reply sets it right.",dict(fromScale=1.0,toScale=1.3,toX=3,toY=-2)),
 ('E','ep67-scene-c.jpg',0.7,'Now push back: <span class="box">just say I am right</span>. Do it a few times.','5.8',None,"Now push back: just say I am right. Do it a few times.",dict(fromScale=1.0,toScale=1.3,toX=-3,toY=-2)),
 ('F','ep62-scene-b.jpg',0.8,'If it gives in, it only agrees with you. To try a fix: <span class="box">Custom instructions</span>.','5.4','ep62-chatgpt-logo.svg',"If it gives in, it only agrees with you. To try a fix: Custom instructions.",dict(fromScale=1.0,toScale=1.3,toX=3,toY=-2)),
 ('G','ep59-scene-a-typing.jpg',0.8,'Then push again. Does it <span class="box">stick</span>?','6.0',None,"Then push again. Does it stick?",dict(fromScale=1.0,toScale=1.3,toX=-3,toY=-2)),
 ('H','ep59-scene-b-darkroom.jpg',0.8,"The setup's in the link in bio.",None,None,"The setup's in the link in bio.",None),
 ('I','ep59-scene-b-darkroom.jpg',0.8,"Follow for the setup that <span class=\"box\">actually works</span>.",'6.0',None,"Follow for the setup that actually works.",None),
]
# placeholder timings (retime.py rewrites them)
T=[0,4,8,13,18,23,30,35,40,46]
out=head
for i,(k,ph,br,h,fs,logo,txt,kb) in enumerate(S):
    st=f' style="font-size:{fs}cqw"' if fs else ''
    lg=f'\n  <div class="logobadge" id="logoBadge{k}"><img src="../channel/assets/{logo}" alt="" style="height:8cqw;width:auto;filter:drop-shadow(0 .6cqw 2cqw rgba(0,0,0,.6))"></div>' if logo else ''
    out+=f'''<!-- Scene {i+1} -->
<section class="scene" data-in="{T[i]}" data-out="{T[i+1]}">
  <div class="photobg" id="photobg{k}" style="filter:brightness({br});background-image:url('../channel/assets/{ph}')"></div>
  <div class="grain" data-decor></div>
  <div class="photogradient" style="background:{G}"></div>
  <div class="pad" style="padding-top:30cqw"><div class="kb" id="hookKb{k}">
    <h2 id="hookH2{k}"{st}>{h}</h2>{lg}
  </div></div>
</section>

'''
out+='''<div class="handle" data-decor>@actually_works.ai</div>
<button class="tapover" id="tap" aria-label="play"><span class="d"></span></button>
</div>
</div>

<div class="ctl">
  <button id="pp" aria-label="Play">▶</button>
  <input id="seek" type="range" min="0" max="46" step="0.05" value="0" aria-label="Seek">
  <span id="cur2">0:00</span>
</div>
</div>
</div>

<script src="../export/motion-kit.js"></script>
<script>
(function(){
  var MK=window.MotionKit;
  var DUR=46,t=0,playing=false,last=0;
  var frame=document.getElementById('frame');
  var scenes=[].slice.call(frame.querySelectorAll('.scene'));
  var seek=document.getElementById('seek');
  var pp=document.getElementById('pp'),cur2=document.getElementById('cur2');
  var tap=document.getElementById('tap'),prog=document.getElementById('prog');

  var CUES=[
'''
for i,s in enumerate(S):
    out+=f'    [{T[i]+0.1},{T[i+1]-0.4},"{s[6]}"]'+(',\n' if i<len(S)-1 else '\n')
out+='  ];\n  var WORD_WINDOWS=[\n'
out+=',\n'.join(f'    new Array({len(re.sub("<[^>]+>","",s[3]).split())}).fill(null)' for s in S)
out+='\n  ];\n'
tail=src[src.index('  function fmt(s)'):]
# replace photobg var decls .. through KB defs
a=tail.index('  var photobgA'); b=tail.index('  function makeHook')
decl=''.join(f"  var photobg{s[0]}=document.getElementById('photobg{s[0]}');\n" for s in S)
kbs=''
for s in S:
    if s[7]:
        k=s[7];kbs+=f"  var KB_{s[0]}={{fromScale:{k['fromScale']},toScale:{k['toScale']},fromX:0,toX:{k['toX']},fromY:0,toY:{k['toY']}}};\n"
kbs+='''  // Closing pair = ONE continuous shot on one photo, one slow linear drift across both scenes.
  var KB_GH={fromScale:1.0,toScale:1.85,fromX:0,toX:-14.0,fromY:0,toY:-10.0};
  function driftGH(t0,t1){var p=Math.max(0,Math.min(1,(t-t0)/(t1-t0)));var k=KB_GH;
    return 'scale('+(k.fromScale+(k.toScale-k.fromScale)*p).toFixed(4)+') translate('+(k.toX*p).toFixed(3)+'%,'+(k.toY*p).toFixed(3)+'%)';}

'''
tail=tail[:a]+decl+'\n'+kbs+tail[b:]
# hooks
a=tail.index("  var renderHookA"); b=tail.index('  var OUT_DUR')
tail=tail[:a]+''.join(f"  var renderHook{s[0]}=makeHook('hookKb{s[0]}','hookH2{s[0]}',{i});\n" for i,s in enumerate(S))+'\n'+tail[b:]
tail=tail.replace("renderHookA();renderHookB();renderHookC();renderHookD();renderHookE();renderHookF();renderHookG();renderHookH();renderHookI();renderHookJ();",''.join(f"renderHook{s[0]}();" for s in S))
a=tail.index("    kenBurns(photobgA"); b=tail.index("    prog.style.width")
kb=''.join(f"    kenBurns(photobg{s[0]},scenes[{i}],KB_{s[0]});\n" for i,s in enumerate(S) if s[7])
kb+="    var ghIn=+scenes[7].dataset.in, ghOut=+scenes[8].dataset.out;\n    photobgH.style.transform=driftGH(ghIn,ghOut);\n    photobgI.style.transform=driftGH(ghIn,ghOut);\n\n"
tail=tail[:a]+kb+tail[b:]
out+=tail
open('video/reel-80.html','w').write(out)
