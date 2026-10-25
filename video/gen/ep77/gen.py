import re
src=open('video/reel-67.html').read()
head=src[:src.index('<!-- Scene 1 -->')]
head=head.replace('--accent:#34D399','--accent:#38BDF8').replace('rgba(13,148,136,.7)','rgba(56,189,248,.7)')
head=re.sub(r'<title>.*?</title>','<title>Reel 77 — Your phone hides a map pin inside your photos.</title>',head,1)
head=re.sub(r'<!--.*?-->','<!-- Episode 77 — photo-composite style. See channel/episode-77-script.md. Photos: reused faceless stock from channel/assets (ep57/ep59/ep67). Logos: ep69 Apple, ep70 ChatGPT. -->',head,1,flags=re.S)
G='linear-gradient(180deg, rgba(4,4,4,.62) 0%, rgba(4,4,4,.52) 14%, rgba(4,4,4,.30) 26%, rgba(4,4,4,.10) 36%, transparent 42%, transparent 50%, rgba(4,4,4,.16) 58%, rgba(4,4,4,.44) 68%, rgba(4,4,4,.62) 78%, rgba(4,4,4,.70) 100%)'
# id, photo, brightness, html, fontsize, logo, text, kb
S=[
 ('A','ep59-scene-c-phonelaptop.jpg',0.8,'Your phone can write a <span class="box">map pin</span> into your photos!',None,None,"Your phone can write a map pin into your photos!",dict(fromScale=1.0,toScale=1.25,toX=-2.0,toY=2.0)),
 ('B','ep59-scene-d-laptopdesk.jpg',0.8,'It is saved as <span class="box">coordinates</span> inside the file.','5.8',None,"It is saved as coordinates inside the file.",dict(fromScale=1.0,toScale=1.3,toX=0,toY=-3.0)),
 ('C','ep57-scene-c-street.jpg',0.9,'Send one, and the person who gets it <span class="box">may see</span> the exact place.','6.0',None,"Send one, and the person who gets it may see the exact place.",dict(fromScale=1.0,toScale=1.3,toX=2.0,toY=-3.0)),
 ('D','ep67-scene-c.jpg',0.7,'OpenAI says ChatGPT <span class="box">does not process</span> a photo&#8217;s metadata.','6.0','ep70-chatgpt-logo.svg',"OpenAI says ChatGPT does not process a photo's metadata.",dict(fromScale=1.0,toScale=1.5,toX=-6.0,toY=4.0)),
 ('E','ep57-scene-d-citystreet.jpg',0.9,'It only looks at the picture itself. And a picture can <span class="box">still give</span> a place away.','5.8',None,"It only looks at the picture itself. And a picture can still give a place away.",dict(fromScale=1.0,toScale=1.3,toX=2.5,toY=-3.0)),
 ('F','ep67-scene-b.jpg',0.8,'To keep it off, tap the send arrow, then Options, and switch <span class="box">Location</span> off.','5.6','ep69-apple-logo.svg',"To keep it off, tap the send arrow, then Options, and switch Location off.",dict(fromScale=1.0,toScale=1.3,toX=2.5,toY=-3.0)),
 ('G','ep59-scene-b-darkroom.jpg',0.8,"The setup's in the link in bio.",None,None,"The setup's in the link in bio.",None),
 ('H','ep59-scene-b-darkroom.jpg',0.8,"Next, I'll show you what ChatGPT does when I <span class=\"box\">hide even more</span> of the photo. Follow, so you get the full story.",'5.6','ep70-chatgpt-logo.svg',"Next, I'll show you what ChatGPT does when I hide even more of the photo. Follow, so you get the full story.",None),
]
# placeholder timings (retime.py rewrites them)
T=[0,4,8,12,16,21,26,30,38]
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
  <input id="seek" type="range" min="0" max="38" step="0.05" value="0" aria-label="Seek">
  <span id="cur2">0:00</span>
</div>
</div>
</div>

<script src="../export/motion-kit.js"></script>
<script>
(function(){
  var MK=window.MotionKit;
  var DUR=38,t=0,playing=false,last=0;
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
kb+="    var ghIn=+scenes[6].dataset.in, ghOut=+scenes[7].dataset.out;\n    photobgG.style.transform=driftGH(ghIn,ghOut);\n    photobgH.style.transform=driftGH(ghIn,ghOut);\n\n"
tail=tail[:a]+kb+tail[b:]
out+=tail
open('video/reel-77.html','w').write(out)
