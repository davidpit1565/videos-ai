from PIL import Image, ImageDraw, ImageFont
FK="/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
W,H=900,420
im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
d.rounded_rectangle((0,0,W,H),radius=44,fill=(250,248,244,245))
f=ImageFont.truetype(FK,78)
def center(t,y,fill=(15,15,15)):
    w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=fill)
center("Send this to",28); center("the friend who",112)
t="overcomplicates"; w=d.textlength(t,font=f); x=(W-w)/2
d.rounded_rectangle((x-18,206,x+w+18,206+100),radius=18,fill=(12,12,12)); d.text((x,214),t,font=f,fill=(255,255,255))
center("everything.",312)
im.save("card.png")
