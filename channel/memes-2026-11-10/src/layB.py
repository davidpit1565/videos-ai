from build import *
b=''
b+=img('sh_blue.png',540,355,.6,z=1)+img('sh_red.png',540,990,-.6,z=1)
# panel 1
b+=img('pr_judge.png',270,365,-2.2,w=450,z=3)
b+=img('sl_blk3.png',765,190,1.4,z=4)+txt('mono','ME: A €900 PHONE<br>I DON\'T NEED.<br>SMART PLAN?',765,192,1.4,'font-size:40px',z=5)
b+=badge('openai.svg',968,312,6,s=112)
b+=img('sl_yel3.png',770,455,-1.6,z=4)+txt('big','Absolutely<br>not.',770,455,-1.6,'font-size:76px')
b+=tape(500,560,100,32,28)
# panel 2
b+=img('pr_pair.png',270,1000,2,w=450,z=3)
b+=img('sl_blk3.png',765,805,-1.2,z=4)+txt('mono','ME: JUST SAY<br>I\'M RIGHT.',765,807,-1.2,'font-size:44px',z=5)
b+=badge('openai.svg',968,940,-5,s=112)
b+=img('sl_yel3.png',770,1075,1.6,z=4)+txt('big','You\'re right.<br>Buy the phone.<br>You deserve it.',770,1075,1.6,'font-size:56px')
b+=tape(500,1200,100,32,-26)
page(b,'B')
