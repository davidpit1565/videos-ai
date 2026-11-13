from lib import *; from fin2 import *
items=[
 ('F1 wide\nupright', svg(f1(YEL,INK,PAPER,INK),B), svg(f1(YEL,INK,PAPER,INK),INK)),
 ('F1 wide\ntilt -14', svg(f1(YEL,INK,PAPER,INK,rot=-14),B), svg(f1(INK,INK,PAPER,YEL,rot=-14),YEL)),
 ('F1 small\nvariant (no brow)', svg(f1(YEL,INK,PAPER,INK,small=True,sc=.96),B), svg(f1(YEL,INK,PAPER,INK,small=True,sc=.96),INK)),
 ('F2 lid', svg(f2(PAPER,INK,INK,B),B), svg(f2(PAPER,INK,YEL,INK),INK)),
 ('F2 lid small', svg(f2(PAPER,INK,INK,B,True),B), svg(f2(PAPER,INK,YEL,INK,True),INK)),
 ('F3 bigger', svg(f3(YEL,INK,B),B), svg(f3(YEL,INK,INK,True),INK)),
 ('F4 no ticks', svg(f4(PAPER,R,INK,PAPER),INK), svg(f4(INK,R,'#3a3a3a',PAPER),YEL)),
]
print(sheet(items,'sf2.png','finalists iteration 2'))
