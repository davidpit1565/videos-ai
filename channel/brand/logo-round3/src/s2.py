from lib import *; from c1 import *; from c2 import *
B='#2447FF'; R='#FF2D2D'; G='#00C853'
items=[
 ('N1 CYCLOPS A', svg(cyclops(PAPER,INK),INK), svg(cyclops(INK,INK),YEL)),
 ('N2 SEAL', svg(seal(PAPER,INK,achar(YEL,INK)),INK), svg(seal(INK,PAPER,achar(INK,INK)),PAPER)),
 ('N3 TYPE a.', svg(typ('a.',PAPER,YEL),INK), svg(typ('A!',INK,INK,620),YEL)),
 ('N21 A-PLUG', svg(aplug(PAPER,INK),YEL), svg(aplug(YEL,PAPER,PAPER),B)),
 ('C3v2 A-CHAR\n+brow', svg(achar(INK,INK,PAPER,YEL),YEL), svg(achar(YEL,INK,PAPER,INK),B)),
 ('C2v2 EYES', svg(eyes2(PAPER,INK,YEL),INK), svg(eyes2(PAPER,INK,INK),B)),
]
print(sheet(items,'s2.png','round3 sketches C'))
