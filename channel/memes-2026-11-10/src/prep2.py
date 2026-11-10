import sys; sys.path.insert(0,'.')
from torn import *
B='build/assets/'
def slip(out,w,h,seed,col):
    im=Image.new('RGB',(w,h),col)
    p=torn_piece(im,pad=16,rim=5,rough=9,seed=seed,paper=tuple(min(255,c+8) for c in col))
    shadow(p,off=(5,8),blur=9,op=.4).save(B+out)
slip('sl_yel2.png',470,280,41,(240,196,56))
slip('sl_yel3.png',500,300,42,(240,196,56))
slip('sl_blk3.png',480,200,43,(23,19,15))
