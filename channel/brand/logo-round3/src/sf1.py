from lib import *; from fin1 import *
def row(lab,a,b): return (lab,a,b)
items=[
 ('F1 A-char\nY on ink /\nfull colour', svg(f1(YEL,INK,PAPER,INK),INK), svg(f1(YEL,INK,PAPER,INK),B)),
 ('F1 ink on Y /\nwhite on red', svg(f1(INK,INK,PAPER,YEL),YEL), svg(f1(PAPER,INK,INK,INK),R)),
 ('F2 eyes\nink+Y brows /\ncobalt', svg(f2(PAPER,INK,YEL),INK), svg(f2(PAPER,INK,INK),B)),
 ('F2 full: cobalt\n+Y brows / red', svg(f2(PAPER,INK,YEL),B), svg(f2(PAPER,INK,INK),R)),
 ('F3 plug\nY on ink /\nfull colour', svg(f3(YEL,INK,INK),INK), svg(f3(YEL,INK,B),B)),
 ('F3 white on\ncobalt / red', svg(f3(PAPER,INK,B),B), svg(f3(PAPER,INK,R),R)),
 ('F4 button\nred / yellow', svg(f4(PAPER,R,INK,PAPER,PAPER),INK), svg(f4(PAPER,YEL,INK,PAPER,YEL),INK)),
 ('F4 on cobalt /\non yellow', svg(f4(PAPER,R,INK,PAPER,PAPER),B), svg(f4(INK,R,'#3a3a3a',PAPER,INK),YEL)),
]
print(sheet(items,'sf1.png','finalists iteration 1 x colour systems'))
