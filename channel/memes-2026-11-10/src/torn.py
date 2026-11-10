import numpy as np
from PIL import Image, ImageFilter
rng=np.random.default_rng(7)
def fbm(h,w,scale,oct=4,seed=0):
    r=np.random.default_rng(seed); out=np.zeros((h,w)); amp=1; tot=0
    for o in range(oct):
        s=max(2,int(scale/(2**o)))
        g=r.random((h//s+3,w//s+3))
        im=Image.fromarray((g*255).astype('uint8')).resize((w,h),Image.BICUBIC)
        out+=amp*np.asarray(im)/255; tot+=amp; amp*=.5
    return out/tot
def torn_piece(img, pad=26, rim=9, rough=16, seed=1, paper=(243,238,226), edges='all'):
    """img: RGB PIL. returns RGBA with torn edge, pale fibrous rim, soft shadow baked separately."""
    w,h=img.size; W,H=w+2*pad,h+2*pad
    yy,xx=np.mgrid[0:H,0:W].astype(float)
    n1=fbm(H,W,40,4,seed)-.5; n2=fbm(H,W,9,3,seed+11)-.5
    d=np.minimum.reduce([xx-pad, W-pad-xx, yy-pad, H-pad-yy])  # distance inside rect (neg outside)
    disp=(n1*rough*2.2+n2*rough*.8)
    outer=(d+disp+rim*.5)>0
    inner=(d+disp*.6-rim)>0
    canvas=np.zeros((H,W,3),float); canvas[:]=paper
    fib=fbm(H,W,3,2,seed+5)
    canvas*= (0.93+0.1*fib)[...,None]
    base=np.zeros((H,W,3),float); base[:]=paper
    big=Image.new('RGB',(W,H),paper); big.paste(img,(pad,pad))
    a=np.asarray(big).astype(float)
    res=np.where(inner[...,None],a,canvas)
    alpha=(outer*255).astype('uint8')
    A=Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(.8))
    out=Image.fromarray(res.clip(0,255).astype('uint8')).convert('RGBA'); out.putalpha(A)
    return out
def shadow(piece, off=(7,10), blur=12, op=.42):
    W,H=piece.size
    sh=Image.new('RGBA',(W+60,H+60),(0,0,0,0))
    a=piece.split()[3].point(lambda v:int(v*op))
    blk=Image.new('RGBA',piece.size,(30,18,6,255)); blk.putalpha(a)
    sh.paste(blk,(30+off[0],30+off[1]),blk)
    sh=sh.filter(ImageFilter.GaussianBlur(blur))
    sh.alpha_composite(piece,(30,30))
    return sh
