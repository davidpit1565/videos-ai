import numpy as np
from PIL import Image, ImageDraw, ImageFilter
W,H=1080,1920
rng=np.random.default_rng(7)
base=np.zeros((H,W,3),np.float32); base[:]=(236,234,228)
img=Image.fromarray(base.astype(np.uint8)); d=ImageDraw.Draw(img)
px,py=120,108; ox,oy=60,54
# dashed grid lines
col=(207,205,198)
for x in range(ox,W,px):
    for y in range(0,H,22): d.line([(x,y),(x,y+11)],fill=col,width=2)
for y in range(oy,H,py):
    for x in range(0,W,22): d.line([(x,y),(x+11,y)],fill=col,width=2)
for x in range(ox,W,px):
    for y in range(oy,H,py): d.ellipse([x-3,y-3,x+3,y+3],fill=(178,176,168))
a=np.asarray(img).astype(np.float32)
# paper grain: fine noise + low-frequency blotches
n=rng.normal(0,4.2,(H,W,1)).astype(np.float32)
lo=Image.fromarray((rng.normal(128,40,(H//40,W//40))).clip(0,255).astype(np.uint8)).resize((W,H),Image.BICUBIC).filter(ImageFilter.GaussianBlur(25))
lo=(np.asarray(lo).astype(np.float32)-128)/128*5.0
a=a+n+lo[...,None]
# soft vignette
yy,xx=np.mgrid[0:H,0:W]; r=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2)
a=a*(1-0.045*np.clip(r-.55,0,1)[...,None])
Image.fromarray(a.clip(0,255).astype(np.uint8)).save('hf/assets/bg.jpg',quality=90)
