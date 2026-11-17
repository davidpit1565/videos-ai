from lib import *; from c1 import *
B='#2447FF'; R='#FF2D2D'; G='#00C853'
items=[
 ('C1 PLUG\nmascot', svg(plug(PAPER,INK,INK),YEL), svg(plug(YEL,INK,PAPER),B)),
 ('C2 SKEPTIC\neyes+brow', svg(skeptic(PAPER,INK),YEL), svg(skeptic(PAPER,INK),R)),
 ('C3 A-GHOST\nA + W feet', svg(aghost(INK,INK),YEL), svg(aghost(YEL,INK),INK)),
 ('C4 TEST\nMARKER', svg(marker(YEL,INK,PAPER),INK), svg(marker(YEL,INK,INK),PAPER)),
 ('C4b DUMMY\nhead', svg(dummy(YEL,INK,YEL,INK),B), svg(dummy(YEL,INK,PAPER,INK),INK)),
 ('C5 FINGER\n"actually"', svg(finger(PAPER,INK,INK),YEL), svg(finger(PAPER,INK,YEL),B)),
 ('C6 BUTTON', svg(button(PAPER,R,INK),INK), svg(button(INK,R,'#333'),YEL)),
]
print(sheet(items,'s1a.png','round3 sketches A'))
items=[
 ('C7 A holds W', svg(aw(PAPER,INK),INK), svg(aw(INK,YEL),YEL)),
 ('C9 BULB', svg(bulb(YEL,INK,PAPER),INK), svg(bulb(YEL,INK,INK),PAPER)),
 ('C10 POWER !', svg(power(PAPER,YEL),INK), svg(power(INK,PAPER),G)),
 ('C12 LEVER', svg(lever(PAPER,INK,R,'#CCC'),YEL), svg(lever('#333',PAPER,YEL,INK),INK)),
 ('C13 THUMB', svg(thumb(PAPER,INK,INK),YEL), svg(thumb(YEL,INK,PAPER),B)),
 ('C14 CLICK\nfits', svg(click(PAPER,YEL),INK), svg(click(INK,B),PAPER)),
]
print(sheet(items,'s1b.png','round3 sketches B'))
