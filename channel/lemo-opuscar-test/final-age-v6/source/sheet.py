import sys,glob,re
from PIL import Image
d,out,cols,w=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
fs=sorted(glob.glob(d+'/*.jpg'),key=lambda f:float(re.findall(r'_([\d.]+?)\.jpg',f)[0]))
h=w*16//9 if False else int(w*1920/1080)
rows=(len(fs)+cols-1)//cols
S=Image.new('RGB',(w*cols,h*rows),'white')
for i,f in enumerate(fs): S.paste(Image.open(f).convert('RGB').resize((w,h)),((i%cols)*w,(i//cols)*h))
S.save(out,quality=88); print(len(fs),S.size)
