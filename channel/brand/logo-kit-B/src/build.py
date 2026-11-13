"""Builds the whole kit: python3 src/build.py  (needs fonttools, uharfbuzz, pillow, node + playwright chromium)."""
import json,subprocess,os,tempfile,math
from PIL import Image,ImageDraw,ImageFont
from geom import *
from wordmark import wordmark,FONT
HERE=os.path.dirname(os.path.abspath(__file__)); KIT=os.path.dirname(HERE)
TMP=tempfile.mkdtemp(); jobs=[]
V=variants(); SIZES=[320,110,40,32,16]
def w(path,s):
    os.makedirs(os.path.dirname(path),exist_ok=True); open(path,'w').write(s+'\n')
def job(svg,wd,ht,out,transparent=False,circle=False):
    svg=svg.replace('<svg ',f'<svg width="{wd}" height="{ht}" ',1)
    html=f'<div style="width:{wd}px;height:{ht}px;border-radius:50%;overflow:hidden">{svg}</div>' if circle else svg
    jobs.append(dict(html=html,w=wd,h=ht,out=out,transparent=transparent))

def tuned16(v,R=470):
    """16 px version. The notch is KEPT (a solid wedge was rendered and read as a hat, not an A).
    Swipe 14% thicker; the whole mark is moved so the feet end exactly on a pixel row."""
    S=v['S']; cx=sum(x for x,y in S)/len(S); cy=sum(y for x,y in S)/len(S)
    a=math.radians(v.get('angle',7)); n=(math.sin(a),math.cos(a)); S2=[]
    for x,y in S:
        d=(x-cx)*n[0]+(y-cy)*n[1]; S2.append((x+n[0]*d*0.14,y+n[1]*d*0.14))
    A,S3,_,_=fit(v['A'],S2,R=R); px=1000/16; bot=max(y for x,y in A); dy=round(bot/px)*px-bot
    return [(x,y+dy) for x,y in A],[(x,y+dy) for x,y in S3]

info={}
for k,v in V.items():
    v['angle']=8 if k=='b' else 7
    A,S,s,c=fit(v['A'],v['S']); v['fA'],v['fS']=A,S
    info[k]=dict(scale=round(s,4),centre=[round(c[0],1),round(c[1],1)],A=pts(v['A']),S=pts(v['S']),fA=pts(A),fS=pts(S))
    d=f'{KIT}/{k}'
    for m in('dark','light'):
        svg=mark_svg(A,S,m); w(f'{d}/mark-{k}-{m}.svg',svg)
        job(svg,1024,1024,f'{d}/avatar-{k}-{m}-1024.png')
        for z in SIZES: job(svg,z,z,f'{TMP}/{k}-{m}-{z}.png',transparent=True,circle=True)
    dark=mark_svg(A,S,'dark')
    for name,z in(('apple-touch-icon.png',180),('icon-192.png',192),('icon-512.png',512)): job(dark,z,z,f'{d}/{name}')
    A32,S32,_,_=fit(v['A'],v['S'],R=455)                     # square icon: no circle crop, mark larger
    w(f'{d}/favicon-{k}.svg',mark_svg(A32,S32,'dark')); job(mark_svg(A32,S32,'dark'),32,32,f'{d}/favicon-32.png')
    A16,S16=tuned16(v); info[k]['A16']=pts(A16); info[k]['S16']=pts(S16)
    w(f'{d}/favicon-{k}-16.svg',mark_svg(A16,S16,'dark')); job(mark_svg(A16,S16,'dark'),16,16,f'{d}/favicon-16.png')
    job(mark_svg(A32,S32,'dark'),16,16,f'{TMP}/{k}-fav16-full.png')
    for m in('dark','light'):
        for one in(False,True):
            svg,W,H=wordmark(m,(v['A'],v['S']),one_swipe=one)
            n=f'lockup-{k}-{m}'+('-one-swipe' if one else '')
            w(f'{KIT}/wordmark/{n}.svg',svg); job(svg,2400,round(2400*H/W),f'{KIT}/wordmark/{n}.png')
for m in('dark','light'):
    svg,W,H=wordmark(m); w(f'{KIT}/wordmark/wordmark-{m}.svg',svg); job(svg,2400,round(2400*H/W),f'{KIT}/wordmark/wordmark-{m}.png')
json.dump(info,open(f'{HERE}/construction.json','w'),indent=1)
json.dump(jobs,open(f'{TMP}/jobs.json','w')); subprocess.run(['node',f'{HERE}/render.js',f'{TMP}/jobs.json'],check=True)

# ---------------- sheets (composed with Pillow from the real-size renders) ----------------
F=lambda z:ImageFont.truetype(FONT,z)
SM=lambda z:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',z)
BLACK=(11,11,12); WH=(255,255,255); GREY=(217,214,204)
def circ(k,m,z): return Image.open(f'{TMP}/{k}-{m}-{z}.png').convert('RGBA')
def zoom(im,f): return im.resize((im.width*f,im.height*f),Image.NEAREST)

def panel(k,bg):
    """One background colour: dark version row and light version row, five sizes + pixel zooms."""
    fg=WH if bg==BLACK else BLACK; sub=(150,150,150) if bg==BLACK else (110,110,110)
    P=Image.new('RGB',(1080,980),bg); d=ImageDraw.Draw(P)
    d.text((40,26),'ON BLACK' if bg==BLACK else 'ON WHITE',font=F(30),fill=fg)
    y=90
    for m in('dark','light'):
        d.text((40,y),f'{m} version',font=SM(18),fill=sub)
        x=40; cy=y+40+160
        for z in SIZES:
            im=circ(k,m,z); P.paste(im,(x,cy-z//2),im); d.text((x+z//2-12,y+40+330),str(z),font=SM(16),fill=sub); x+=z+34
        for z,f in((32,5),(16,5)):
            im=zoom(circ(k,m,z),f); P.paste(im,(x+10,cy-im.height//2),im); d.text((x+10,y+40+330),f'{z} px x{f}',font=SM(16),fill=sub); x+=im.width+34
        y+=440
    return P

for k,v in V.items():
    S=Image.new('RGB',(2160,1090),GREY); d=ImageDraw.Draw(S)
    d.text((40,24),f'{k.upper()}  ·  {v["name"].upper()}',font=F(44),fill=BLACK)
    d.text((2120,40),'circle crop at 320 / 110 / 40 / 32 / 16 px, real size',font=SM(20),fill=(90,90,90),anchor='ra')
    S.paste(panel(k,BLACK),(0,110)); S.paste(panel(k,WH),(1080,110)); S.save(f'{KIT}/{k}/preview-{k}.png')

# overview, 1600 wide
def fitw(path,wd):
    im=Image.open(path).convert('RGB'); return im.resize((wd,round(im.height*wd/im.width)),Image.LANCZOS)
W=1600; rows=[]
for k,v in V.items():
    R=Image.new('RGB',(W,1010),GREY); d=ImageDraw.Draw(R)
    d.rectangle((0,0,W,6),fill=BLACK)
    d.text((40,26),k,font=F(150),fill=BLACK); d.text((190,62),v['name'].upper(),font=F(40),fill=BLACK)
    d.text((190,116),{'a':'the research construction, unchanged: 7 degrees, 70-degree ends',
                      'b':'heavier A with constant-width legs, 8 degrees, thicker swipe, 66-degree chisel ends',
                      'c':'same A as a; swipe narrows 5% and each end is a two-facet hand cut'}[k],font=SM(22),fill=(70,70,70))
    x=40
    for m in('dark','light'):
        im=Image.open(f'{TMP}/{k}-{m}-320.png').convert('RGBA'); R.paste(im,(x,200),im); x+=350
    # small sizes on black and on white strips
    for bg,m,yy in((BLACK,'dark',200),(WH,'light',365)):
        d.rectangle((760,yy,1560,yy+155),fill=bg); xx=790
        for z in(110,40,32,16):
            im=circ(k,m,z); R.paste(im,(xx,yy+78-z//2),im); xx+=z+30
        for z,f in((32,4),(16,4)):
            im=zoom(circ(k,m,z),f); R.paste(im,(xx+20,yy+78-im.height//2),im); xx+=im.width+40
    d.text((760,526),'110 / 40 / 32 / 16 px real size, then 32 and 16 px enlarged x4',font=SM(18),fill=(90,90,90))
    f32=zoom(Image.open(f'{KIT}/{k}/favicon-32.png').convert('RGB'),3); f16=zoom(Image.open(f'{KIT}/{k}/favicon-16.png').convert('RGB'),6)
    R.paste(Image.open(f'{KIT}/{k}/favicon-32.png'),(1290,570)); R.paste(f32,(1335,570)); R.paste(Image.open(f'{KIT}/{k}/favicon-16.png'),(1450,570)); R.paste(f16,(1475,570))
    d.text((1290,676),'favicon 32 (x3)   16 (x6)',font=SM(18),fill=(90,90,90))
    y=570
    for i,n in enumerate((f'lockup-{k}-dark',f'lockup-{k}-light')):
        im=fitw(f'{KIT}/wordmark/{n}.png',600); R.paste(im,(40+i*620,y))
    y2=y+im.height+16
    for i,n in enumerate((f'lockup-{k}-dark-one-swipe',f'lockup-{k}-light-one-swipe')):
        im2=fitw(f'{KIT}/wordmark/{n}.png',600); R.paste(im2,(40+i*620,y2))
    d.text((1290,y2+20),'top: lockup as briefed\n(mark + bar = 2 swipes)\nbottom: one-swipe\nalternative',font=SM(18),fill=(90,90,90),spacing=6)
    rows.append(R.crop((0,0,W,y2+im2.height+40)))
wm=[fitw(f'{KIT}/wordmark/wordmark-{m}.png',740) for m in('dark','light')]
head=Image.new('RGB',(W,150),GREY); d=ImageDraw.Draw(head)
d.text((40,30),'ACTUALLY WORKS  ·  LOGO KIT B  ·  THE HIGHLIGHT',font=F(46),fill=BLACK)
d.text((40,96),'Three variants of the avatar mark: a / b / c. Dark and light, in the circle crop, at real sizes. Nothing is published.',font=SM(20),fill=(70,70,70))
foot=Image.new('RGB',(W,wm[0].height+120),GREY); d=ImageDraw.Draw(foot); d.rectangle((0,0,W,6),fill=BLACK)
d.text((40,24),'WORDMARK (SAME FOR ALL VARIANTS)',font=F(34),fill=BLACK)
foot.paste(wm[0],(40,90)); foot.paste(wm[1],(820,90))
O=Image.new('RGB',(W,head.height+sum(r.height for r in rows)+foot.height),GREY); y=0
for im in[head]+rows+[foot]: O.paste(im,(0,y)); y+=im.height
O.save(f'{KIT}/kit-overview.png'); SP='/tmp/claude-0/-home-user-videos-ai/2effda64-8e71-5ab6-95b7-5d1257c9dd3f/scratchpad/kit'
C=Image.new('RGB',(16*12*6+70,16*12+20),(120,120,120)); x=10
for k in V:
    for p in(f'{TMP}/{k}-fav16-full.png',f'{KIT}/{k}/favicon-16.png'):
        C.paste(zoom(Image.open(p).convert('RGB'),12),(x,10)); x+=16*12+10
C.save(SP+'/fav16.png')
for k,v in V.items():
    print(k,'max radius %%: %.1f'%(max(math.hypot(x-500,y-500) for x,y in v['fA']+v['fS'])/5))
print('ok',O.size,len(jobs),'renders')
