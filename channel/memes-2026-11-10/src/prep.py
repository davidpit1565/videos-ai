import sys; sys.path.insert(0,'.')
from torn import *
from PIL import ImageOps, ImageEnhance
B='build/assets/'
def prep_print(path,box,out,width,seed,tint=(238,230,214)):
    im=Image.open(path).convert('RGB').crop(box).convert('L')
    im=ImageOps.autocontrast(im,cutoff=1)
    im=ImageEnhance.Contrast(im).enhance(1.15)
    rgb=ImageOps.colorize(im,(18,14,12),tint)
    h=int(rgb.height*width/rgb.width); rgb=rgb.resize((width,h),Image.LANCZOS)
    p=torn_piece(rgb,pad=22,rim=8,rough=12,seed=seed,paper=(244,239,226))
    shadow(p).save(B+out)
    print(out,shadow(p).size)
prep_print('raw/conviction.jpg',(52,62,908,666),'pr_essay.png',560,3)
prep_print('raw/c2.jpg',(30,150,930,1060),'pr_sales.png',430,5)
prep_print('raw/voisines.jpg',(300,150,680,640),'pr_judge.png',400,9)
prep_print('raw/voisines.jpg',(70,120,900,1060),'pr_pair.png',420,12)
def sheet(src,out,w,h,seed):
    im=Image.open(B+src).convert('RGB'); 
    im=im.resize((w,h),Image.LANCZOS)
    p=torn_piece(im,pad=20,rim=9,rough=22,seed=seed,paper=(238,232,220))
    shadow(p,off=(9,13),blur=16,op=.5).save(B+out); print(out)
sheet('pap_blue.jpg','sh_blue.png',950,575,21)
sheet('pap_red.jpg','sh_red.png',950,575,22)
def slip(out,w,h,seed,col):
    im=Image.new('RGB',(w,h),col)
    p=torn_piece(im,pad=16,rim=5,rough=9,seed=seed,paper=tuple(min(255,c+8) for c in col))
    shadow(p,off=(5,8),blur=9,op=.4).save(B+out)
slip('sl_yel1.png',420,200,31,(240,196,56)); slip('sl_cream1.png',440,230,32,(243,238,224)); slip('sl_cream2.png',900,150,33,(243,238,224))
slip('sl_black1.png',560,120,34,(23,19,15)); slip('sl_black2.png',640,110,35,(23,19,15))
