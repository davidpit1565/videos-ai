import cairosvg, io, math
from PIL import Image, ImageDraw, ImageFont
INK='#0B0B0C'; PAPER='#FFFFFF'; YEL='#FFE600'
def svg(inner, bg, clip=True, size=1000):
    c = '<clipPath id="c"><circle cx="500" cy="500" r="500"/></clipPath>' if clip else ''
    g = '<g clip-path="url(#c)">' if clip else '<g>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="{size}" height="{size}"><defs>{c}</defs>{g}<rect width="1000" height="1000" fill="{bg}"/>{inner}</g></svg>'
def png(svgtxt, px):
    b = cairosvg.svg2png(bytestring=svgtxt.encode(), output_width=px*4 if px<200 else px*2, output_height=px*4 if px<200 else px*2)
    im = Image.open(io.BytesIO(b)).convert('RGBA')
    return im.resize((px,px), Image.LANCZOS)
def font(sz):
    return ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf', sz)
def sheet(items, out, title=''):
    # items: list of (label, svg_on_dark_page, svg_on_light_page)
    rowh=350; W=1640
    im = Image.new('RGB',(W, 70+rowh*len(items)),'#D9D6CB'); d=ImageDraw.Draw(im)
    d.text((20,18),title,fill='black',font=font(30))
    for i,(lab,sd,sl) in enumerate(items):
        y=70+i*rowh
        d.rectangle((250,y,940,y+rowh-10),fill='#000000'); d.rectangle((945,y,1635,y+rowh-10),fill='#FFFFFF')
        d.multiline_text((14,y+20),lab,fill='black',font=font(22),spacing=6)
        for s,x0 in ((sd,250),(sl,945)):
            x=x0+10
            for px in (320,110,40,32):
                a=png(s,px); im.paste(a,(x,y+10+(320-px)//2),a); x+=px+ (25 if px>100 else 18)
            # x4 blowup of 32
            a=png(s,32).resize((128,128),Image.NEAREST); im.paste(a,(x0+555,y+200),a)
    im.save(out); return im.size
