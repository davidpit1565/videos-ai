"""Generate video/reel-N.html from video/reel-63.html's structure. Usage: gen_reel.py spec.json"""
import re, sys, json
spec=json.load(open(sys.argv[1]))
EP=spec['ep']; ACC=spec['accent']; root=spec['root']; FPS=spec.get('fps',10)
src=open(f'{root}/video/reel-63.html').read()
head=src[:src.index('<!-- Scene 1')]
grad=re.search(r'class="photogradient" style="([^"]+)"',src).group(1)
tail_html=src[src.index('<div class="handle"'):src.index('<script src="../export/motion-kit.js">')]
head=head.replace('</style>\n','</style>\n'+CSS_PLACEHOLDER,1) if False else head
head=head.replace('#A78BFA',ACC).replace('#3F6212','#92400E').replace('Reel 63 — Is the AI chat you use one of the risky ones?',f"Reel {EP} — {spec['title']}")
head=re.sub(r'<!--\s*Episode 63.*?-->',f"<!--\n  Episode {EP} — real-photo composite style (video/reel-template-photo.html). {spec['note']}\n  See channel/episode-{EP}-script.md. Photos: channel/assets/ep{EP}-scene-*.jpg (Unsplash License, faceless).\n  Logos (icons only, no captions): real marks from official/Wikimedia sources.\n-->",head,flags=re.S)
LOGO=lambda f: f'<img src="../channel/assets/{f}" alt="" style="height:6.4cqw;width:auto;filter:invert(1) drop-shadow(0 .4cqw 1.4cqw rgba(0,0,0,.6))">'
CSS=open(f'{root}/video/gen/ep74/css.txt').read().replace('#3F6212','#92400E')+".hlw{position:absolute;background:rgba(245,158,11,.36);border:.5cqw solid rgba(245,158,11,.9);border-radius:1.2cqw;box-shadow:0 0 3.2cqw rgba(245,158,11,.55);opacity:0;pointer-events:none}\n"
scenes=spec['scenes']; n=len(scenes)
HL=json.load(open(f'{root}/video/gen/ep74/hl.json'))
t=0.0; times=[]
for s in scenes:
    d=s.get('dur') or max(2.4,len(s['spoken'].split())*0.42+0.5); times.append((round(t,2),round(t+d,2))); t+=d
DUR=round(t,2)
ids='ABCDEFGHIJKLMNOPQR'
body=''
for i,s in enumerate(scenes):
    lab=ids[i]; dur=times[i]
    padtop=' style="padding-top:%scqw"'%s.get('pt',30) if s.get('top',True) else ''
    fsty=f' style="font-size:{s["fs"]}cqw"' if s.get('fs') else ''
    badge=''
    hcls=' class="hookbar"' if s.get('bar') else ''
    if s.get('logos'):
        badge=f'\n  <div class="logobadge" id="logoBadge{lab}">'+''.join(LOGO(f) for f in s['logos'])+'</div>'
    br=s.get('br',1.0)
    filt=f'filter:brightness({br});' if br!=1.0 else ''
    ring=''
    for (rx,ry,rw,rh,rdl) in s.get('rings',[]):
        ring+=f'<div class="ring" data-rf="{rx},{ry},{rw},{rh}" data-rd="{rdl}"></div>'
    if s.get('hl'):
        ring+='<div class="hlw" data-hl=\''+json.dumps(HL[s['hl']])+'\'></div>'
    nofilt=' style="filter:none"' if s.get('nofilter') else ''
    body+=f'''<!-- Scene {i+1} -->
<section class="scene" data-in="{dur[0]}" data-out="{dur[1]}" data-y0="{s.get('y0',0)}" data-s0="{s['s0']}" data-s1="{s['s1']}" data-z0="{s.get('z0',1)}" data-z1="{s.get('z1',1)}" data-cx="{s.get('cx',360)}" data-cy="{s.get('cy',545)}" data-rd="{s.get('rd',0.5)}" data-rt="{s.get('rt',0)}" data-dl="{s.get('dl',0)}" data-neg="{1 if s.get('neg') else 0}" data-ct="{s.get('ct',0)}" data-zlin="{1 if s.get('zlin') else 0}"{(" data-zs='"+json.dumps(s['zs'])+"'") if s.get('zs') else ''}>
  <div class="photobg" id="photobg{lab}" style="background:radial-gradient(120% 75% at 50% 48%,{ACC}66 0%,{ACC}26 38%,#07151a 78%)"><div class="card"><canvas class="scrcard" width="1080" height="1920"{nofilt}></canvas>{ring}</div><div class="scrim"></div></div>
  <div class="grain" data-decor></div>
  <div class="photogradient" style="{grad}"></div>
  <div class="pad"{padtop}><div class="kb" id="hookKb{lab}">
    <h2 id="hookH2{lab}"{fsty}{hcls}>{s['html']}</h2>{badge}
  </div></div>
</section>

'''
cues=',\n    '.join(f'[{times[i][0]+0.08},{times[i][1]-0.4:.2f},"{s["spoken"]}"]' for i,s in enumerate(scenes))
windows=',\n    '.join(f'new Array({len(s["spoken"].split())}).fill(null)' for s in scenes)
js=src[src.index('<script>\n(function(){'):]
js=js.replace('var DUR=49.0','var DUR='+str(DUR))
js=re.sub(r'var CUES=\[.*?\n  \];','var CUES=[\n    '+cues+'\n  ];',js,flags=re.S)
js=re.sub(r'var WORD_WINDOWS=\[.*?\n  \];','var WORD_WINDOWS=[\n    '+windows+'\n  ];',js,flags=re.S)
pg=''.join(f"  var photobg{ids[i]}=document.getElementById('photobg{ids[i]}');\n" for i in range(n))
js=re.sub(r"  var photobgA=.*?var photobgBridge=document.getElementById\('photobgBridge'\);\n",pg,js,flags=re.S)
base=['{fromScale:1.0,toScale:1.30,fromX:0,toX:-3.0,fromY:0,toY:2.0}','{fromScale:1.0,toScale:1.32,fromX:0,toX:2.6,fromY:0,toY:-3.0}','{fromScale:1.0,toScale:2.0,fromX:0,toX:-12.0,fromY:0,toY:7.0}','{fromScale:1.0,toScale:1.34,fromX:0,toX:3.0,fromY:0,toY:-3.4}','{fromScale:1.0,toScale:1.6,fromX:0,toX:-8.0,fromY:0,toY:5.0}','{fromScale:1.0,toScale:1.75,fromX:0,toX:-9.0,fromY:0,toY:-6.0}','{fromScale:1.0,toScale:1.30,fromX:0,toX:3.0,fromY:0,toY:-2.2}','{fromScale:1.0,toScale:1.4,fromX:0,toX:2.0,fromY:0,toY:-2.5}']
nk=n-2  # last two scenes share one continuous drift
kbdef=''.join(f'  var KB_{ids[i]}={base[i%len(base)]};\n' for i in range(nk))
js=re.sub(r"  var KB_A=.*?var KB_Bridge=\{[^\n]*\n",kbdef,js,flags=re.S)
hooks=''.join(f"  var renderHook{ids[i]}=makeHook('hookKb{ids[i]}','hookH2{ids[i]}',{i});\n" for i in range(n))
js=re.sub(r"  var renderHookA=.*?var renderHookH=makeHook\('hookKbH','hookH2H',8\);\n",hooks,js,flags=re.S)
calls=''.join(f'renderHook{ids[i]}();' for i in range(n))
js=re.sub(r"renderHookA\(\);renderHookB\(\);.*?renderHookH\(\);",calls,js)
kbcalls=''.join(f"    kenBurns(photobg{ids[i]},scenes[{i}],KB_{ids[i]});\n" for i in range(nk))
js=re.sub(r"    kenBurns\(photobgA,scenes\[0\],KB_A\);.*?photobgH\.style\.transform=driftGH\(ghIn,ghOut\);",
   kbcalls+f"    var ghIn=+scenes[{nk}].dataset.in, ghOut=+scenes[{nk+1}].dataset.out;\n    photobg{ids[nk]}.style.transform=driftGH(ghIn,ghOut);\n    photobg{ids[nk+1]}.style.transform=driftGH(ghIn,ghOut);",js,flags=re.S)
tail=tail_html.replace('max="49.7"',f'max="{DUR+0.7}"')
frs='<div class="frs" data-decor>'+''.join(f'<img class="fr" data-k="{k}" src="../channel/assets/ep{EP}-screen/f_{k:03d}.jpg" alt="">' for k in spec['frame_files'])+'</div>\n'
draw='''  var FPSV=%d;
  var FRM={};[].slice.call(document.querySelectorAll('img.fr')).forEach(function(im){FRM[+im.dataset.k-1]=im;});
  var GRP=%s;
  function grpOf(i){for(var g=0;g<GRP.length;g++){if(GRP[g].indexOf(i)>=0)return g;}return -1;}
  function sameGrp(a,b){var ga=grpOf(a);return ga>=0&&ga===grpOf(b);}
  var scrScenes=scenes.map(function(sc,si){var c=sc.querySelector('.scrcard');if(!c)return null;var hw=sc.querySelector('.hlw');
    return {si:si,sc:sc,card:c,s0:+sc.dataset.s0,s1:+sc.dataset.s1,z0:+sc.dataset.z0,z1:+sc.dataset.z1,cx:+sc.dataset.cx,cy:+sc.dataset.cy,rd:+sc.dataset.rd,rt:+sc.dataset.rt,dl:+sc.dataset.dl,neg:+sc.dataset.neg,ct:+sc.dataset.ct,zlin:+sc.dataset.zlin,zs:sc.dataset.zs?JSON.parse(sc.dataset.zs):null,
      rings:[].slice.call(sc.querySelectorAll('.ring')),hl:hw,hld:hw?JSON.parse(hw.dataset.hl):null};}).filter(Boolean);
  function drawScr(){
    scrScenes.forEach(function(o){
      var a=+o.sc.dataset.in,b=+o.sc.dataset.out,p=Math.max(0,Math.min(1,(t-a)/(b-a)));
      var pp=o.rt>0?Math.max(0,Math.min(1,(t-a-o.dl)/o.rt)):p,ss=o.s0+(o.s1-o.s0)*pp,idx=Math.round(ss*FPSV);
      var im=FRM[idx]; if(!im||!im.complete||!im.naturalWidth) return;
      var K=im.naturalWidth/720,fh=im.naturalHeight/K,pe=p*p*(3-2*p),z=o.z0+(o.z1-o.z0)*(o.zlin?p:pe);
      if(o.zs){var rel=t-a,zc=o.zs[0][1],zp=zc;for(var q=0;q<o.zs.length;q++){if(rel>=o.zs[q][0]){var ee=Math.max(0,Math.min(1,(rel-o.zs[q][0])/0.22));ee=ee*ee*(3-2*ee);zp=q>0?o.zs[q-1][1]:o.zs[q][1];zc=zp+(o.zs[q][1]-zp)*ee;}}z=zc;}
      var sw=720/z,sh=1280/z,sx=Math.max(0,Math.min(720-sw,o.cx-sw/2)),syr=o.cy-sh/2;
      var sy=o.neg?Math.min(fh-sh,syr):Math.max(0,Math.min(fh-sh,syr));
      var ctx=o.card.getContext('2d');
      if(o.neg){var srcY=Math.max(o.ct||0,sy,0),top=Math.max(0,srcY-sy),srcH=Math.min(sh-top,fh-srcY);
        ctx.fillStyle='#000';ctx.fillRect(0,0,1080,1920);
        ctx.drawImage(im,sx*K,srcY*K,sw*K,srcH*K,0,top/sh*1920,1080,srcH/sh*1920);}
      else ctx.drawImage(im,sx*K,sy*K,sw*K,sh*K,0,0,1080,1920);
      o.rings.forEach(function(rg){var r=rg.dataset.rf.split(',').map(Number);
        rg.style.left=((r[0]-sx)/sw*100).toFixed(2)+'%%';rg.style.top=((r[1]-sy)/sh*100).toFixed(2)+'%%';rg.style.width=(r[2]/sw*100).toFixed(2)+'%%';rg.style.height=(r[3]/sh*100).toFixed(2)+'%%';
        var e=Math.max(0,Math.min(1,(t-a-(+rg.dataset.rd))/0.3));rg.style.opacity=(e*(0.82+0.18*Math.sin(t*7))).toFixed(3);});
      if(o.hl){var cue=CUES[o.si],rel=t-cue[0],cur=null;
        for(var k=0;k<o.hld.length;k++){var w=o.hld[k];if(rel>=w.s&&rel<w.e){cur=w;break;}}
        if(cur){var bx=cur.b;o.hl.style.left=((bx[0]-sx)/sw*100).toFixed(2)+'%%';o.hl.style.top=((bx[1]-sy)/sh*100).toFixed(2)+'%%';o.hl.style.width=(bx[2]/sw*100).toFixed(2)+'%%';o.hl.style.height=(bx[3]/sh*100).toFixed(2)+'%%';o.hl.style.opacity='1';}
        else o.hl.style.opacity='0';}
    });
  }
''' % (FPS, json.dumps(spec.get('groups',[])))
js=js.replace("  function render(){\n","draw+\"  function render(){\n    drawScr();\n\"",1) if False else js
js=js.replace("    var opacity,scale,blur;\n    if(prev && t<inStart){","    var opacity,scale,blur;\n    if(prev&&sameGrp(i-1,i)){ inStart=+prev.dataset.out; inEndsAt=inStart; }\n    if(next&&sameGrp(i,i+1)){ outStart=outTime; }\n    if(prev && t<inStart){",1)
js=js.replace("  function render(){\n",draw+"  function render(){\n    drawScr();\n",1)
tail=tail.replace('<div class="handle"',frs+'<div class="handle"',1)
tail=re.sub(r'<div class="handle"[^>]*>.*?</div>','',tail,flags=re.S)  # full-bleed screen episodes: the handle used to sit on the keyboard / the answer (David, 18.10.2026)
head=head.replace('</style>\n',CSS.replace('<style>\n','').replace('</style>\n','')+'</style>\n',1)
a=js.index("    kenBurns(photobgA,scenes[0],KB_A);")
endtok="photobg"+ids[n-1]+".style.transform=driftGH(ghIn,ghOut);"
b=js.index(endtok)+len(endtok)
GR=spec.get('groups',[])
newkb="""    scenes.forEach(function(sc,i){
      var i0=i,i1=i;for(var g=0;g<GRP.length;g++){if(GRP[g].indexOf(i)>=0){i0=GRP[g][0];i1=GRP[g][GRP[g].length-1];}}
      var a=+scenes[i0].dataset.in,b=+scenes[i1].dataset.out,p=Math.max(0,Math.min(1,(t-a)/(b-a)));
      var dir=(i0%2?-1:1);
      document.getElementById('photobg'+'ABCDEFGHIJKLMNOPQR'[i]).style.transform='scale('+(1+0.055*p).toFixed(4)+') translate('+(dir*0.9*p).toFixed(3)+'%,'+(-0.7*p).toFixed(3)+'%)';
    });"""
js=js[:a]+newkb+js[b:]
open(f'{root}/video/reel-{EP}.html','w').write(head+body+tail+'<script src="../export/motion-kit.js"></script>\n'+js)
print('written',DUR,n)
