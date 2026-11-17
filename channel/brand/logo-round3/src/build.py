import os, io, cairosvg, shutil
from PIL import Image, ImageDraw, ImageFont
from lib import INK, PAPER, YEL
from fin2 import f1, f2, f3, f4, B, R
from txt import text_path
OUT='/home/user/videos-ai/channel/brand/logo-round3/'
os.makedirs(OUT+'exploration',exist_ok=True); os.makedirs(OUT+'src',exist_ok=True)
BR='BricolageGrotesque[opsz,wdth,wght].ttf'; AR='Archivo[wdth,wght].ttf'; FR='Fredoka[wdth,wght].ttf'; UN='Unbounded[wght].ttf'
# name, dark(inner,bg), light(inner,bg), small dark, small light, font spec
FIN=[
 ('1-a-character', (f1(YEL,INK,PAPER,INK),INK), (f1(YEL,INK,PAPER,INK),B), (f1(YEL,INK,PAPER,INK,small=True,sc=.96),INK), (f1(YEL,INK,PAPER,INK,small=True,sc=.96),B),
   (BR,(('wght',800),('wdth',100),('opsz',96)),'Actually','Works',0)),
 ('2-raised-eyebrow', (f2(PAPER,INK,YEL,INK),INK), (f2(PAPER,INK,INK,B),B), (f2(PAPER,INK,YEL,INK,True),INK), (f2(PAPER,INK,INK,B,True),B),
   (AR,(('wght',800),('wdth',112)),'ACTUALLY','WORKS',2)),
 ('3-plug', (f3(YEL,INK,INK),INK), (f3(YEL,INK,B),B), (f3(YEL,INK,INK,True),INK), (f3(YEL,INK,B,True),B),
   (FR,(('wght',700),('wdth',100)),'actually','works',0)),
 ('4-button', (f4(PAPER,R,INK,PAPER),INK), (f4(INK,R,'#3a3a3a',PAPER),YEL), (f4(PAPER,R,INK,PAPER),INK), (f4(INK,R,'#3a3a3a',PAPER),YEL),
   (UN,(('wght',800),),'ACTUALLY','WORKS',0)),
]
def S(inner,bg,clip,cid='c'):
    c=f'<defs><clipPath id="{cid}"><circle cx="500" cy="500" r="500"/></clipPath></defs>' if clip else ''
    g=f'<g clip-path="url(#{cid})">' if clip else '<g>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">{c}{g}<rect width="1000" height="1000" fill="{bg}"/>{inner}</g></svg>'
def P(svgtxt,px,ss=4):
    b=cairosvg.svg2png(bytestring=svgtxt.encode(),output_width=px*ss,output_height=px*ss)
    return Image.open(io.BytesIO(b)).convert('RGBA').resize((px,px),Image.LANCZOS)
def wordmark(inner,bg,spec,fg,page):
    font,axes,l1,l2,tr=spec
    d1,w1=text_path(font,l1,118,330,138,axes,tr); d2,w2=text_path(font,l2,118,330,256,axes,tr)
    W=int(330+max(w1,w2)+40)
    s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 300" width="{W}" height="300"><defs><clipPath id="k"><circle cx="500" cy="500" r="500"/></clipPath></defs>'
    s+=f'<g transform="translate(30 20) scale(.26)"><g clip-path="url(#k)"><rect width="1000" height="1000" fill="{bg}"/>{inner}</g></g>'
    s+=f'<path d="{d1}" fill="{fg}"/><path d="{d2}" fill="{fg}"/></svg>'
    return s,W
def F(sz,b=True): return ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-%s.otf'%('Bold' if b else 'Regular'),sz)
BW=1600; BH=1010
ov=Image.new('RGB',(BW,150+BH*4),'#D9D6CB'); d=ImageDraw.Draw(ov)
d.text((30,24),'ACTUALLY WORKS  ·  LOGO ROUND 3  ·  four finalists',fill='black',font=F(40))
d.text((30,80),'Each: 320 / 110 / 40 / 32 px in the circle crop on dark and on light, 64 px favicon, a comment line, and a plain wordmark. Drafts, nothing is published.',fill='#333',font=F(22,False))
TITLES=['1 · A-CHARACTER  (the letter A as a mascot)','2 · RAISED EYEBROW  (the look of someone who tests it first)','3 · PLUG  (plug it in, it works)','4 · BUTTON  (press it, it works)']
for i,(name,dk,lt,sdk,slt,spec) in enumerate(FIN):
    for tag,(inner,bg),(sinner,sbg),page,fg in (('dark',dk,sdk,'#000000',PAPER),('light',lt,slt,'#FFFFFF',INK)):
        open(OUT+f'{name}-avatar-{tag}.svg','w').write(S(inner,bg,False))
        open(OUT+f'{name}-small-{tag}.svg','w').write(S(sinner,sbg,True))
        P(S(inner,bg,False),1024,2).convert('RGB').save(OUT+f'{name}-avatar-{tag}-1024.png')
        P(S(sinner,sbg,True),64).save(OUT+f'{name}-favicon-64-{tag}.png')
        w,W=wordmark(inner,bg,spec,fg,page); open(OUT+f'{name}-wordmark-{tag}.svg','w').write(w)
    y0=150+i*BH
    d.rectangle((0,y0,BW,y0+4),fill='black'); d.text((30,y0+18),TITLES[i],fill='black',font=F(34))
    for j,(tag,(inner,bg),(sinner,sbg),page,fg,sub) in enumerate((('dark',dk,sdk,'#000000',PAPER,'#A8A8A8'),('light',lt,slt,'#FFFFFF',INK,'#737373'))):
        x0=20+j*790; y=y0+75
        d.rectangle((x0,y,x0+770,y+915),fill=page)
        full=S(inner,bg,True); sm=S(sinner,sbg,True)
        a=P(full,320); ov.paste(a,(x0+20,y+20),a)
        a=P(full,110); ov.paste(a,(x0+365,y+20),a)
        a=P(sm,40); ov.paste(a,(x0+500,y+55),a)
        a=P(sm,32); ov.paste(a,(x0+565,y+59),a)
        a=P(sm,64); ov.paste(a,(x0+630,y+43),a)
        for lab,lx in (('320',20),('110',365),('40',500),('32',565),('favicon 64',630)): d.text((x0+lx,y+345 if lab=='320' else y+140),lab,fill=sub,font=F(16,False))
        # x5 blow-up of the 32 px
        a=P(sm,32).resize((160,160),Image.NEAREST); ov.paste(a,(x0+365,y+180),a); d.text((x0+540,y+250),'32 px, enlarged x5',fill=sub,font=F(16,False))
        # comment line mock
        cy=y+400
        d.line((x0+20,cy-12,x0+750,cy-12),fill=sub,width=1)
        for k,(u,t) in enumerate((('actually_works.ai','Tested it three times. This one works.'),('some.viewer','ok this is the first one that worked for me'))):
            yy=cy+k*74
            if k==0: a=P(sm,40); ov.paste(a,(x0+20,yy),a)
            else: d.ellipse((x0+20,yy,x0+60,yy+40),fill='#8a8a8a')
            d.text((x0+74,yy-1),u,fill=fg,font=F(19)); d.text((x0+74+d.textlength(u,font=F(19))+10,yy-1),t,fill=fg,font=F(19,False))
            d.text((x0+74,yy+25),'2h    Reply',fill=sub,font=F(15,False))
        d.line((x0+20,cy+150,x0+750,cy+150),fill=sub,width=1)
        # profile header mock
        py=cy+170; a=P(full,110); ov.paste(a,(x0+20,py),a)
        d.text((x0+150,py+12),'actually_works.ai',fill=fg,font=F(26)); d.text((x0+150,py+52),'AI, tested. Only what works.',fill=fg,font=F(19,False)); d.text((x0+150,py+80),'310 followers',fill=sub,font=F(17,False))
        # wordmark
        w,W=wordmark(inner,bg,spec,fg,page)
        h=150; ww=int(W*h/300); b=cairosvg.svg2png(bytestring=w.encode(),output_width=ww*2,output_height=h*2)
        im=Image.open(io.BytesIO(b)).convert('RGBA').resize((ww,h),Image.LANCZOS); ov.paste(im,(x0+20,py+150),im)
        im.save(OUT+f'{name}-wordmark-{tag}.png')
ov.save(OUT+'round3-overview.png'); print(ov.size)
for f in ('s1a.png','s1b.png','s2.png','sf1.png','sf2.png'): shutil.copy(f,OUT+'exploration/'+{'s1a.png':'01-sketches-a.png','s1b.png':'02-sketches-b.png','s2.png':'03-sketches-c.png','sf1.png':'04-finalists-iteration1-colour-systems.png','sf2.png':'05-finalists-iteration2.png'}[f])
shutil.copy('../av/sheet.png',OUT+'exploration/00-reference-avatars-youtube.png')
for f in ('lib.py','c1.py','c2.py','fin1.py','fin2.py','txt.py','build.py','s1.py','s2.py','sf1.py','sf2.py'): shutil.copy(f,OUT+'src/'+f)
