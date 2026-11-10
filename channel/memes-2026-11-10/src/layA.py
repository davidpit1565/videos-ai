from build import *
b=''
b+=img('sh_blue.png',540,420,-.7,z=1)+img('sh_red.png',540,1005,.6,z=1)
# shared question on top
b+=img('sl_black2.png',540,80,-.8,z=10)+txt('mono','ME: YES OR NO?',540,82,-.8,'font-size:50px',z=11)
# panel 1 Claude
b+=img('pr_essay.png',330,455,-2.5,w=548,z=3)
b+=img('sl_black1.png',335,175,-1.6,z=4)+txt('lab','ME WITH CLAUDE',335,177,-1.6)
b+=badge('claude.svg',668,175,6)
b+=img('sl_yel2.png',795,450,2.2,z=4)+txt('big','A thoughtful<br>essay.',795,450,2.2)
# panel 2 ChatGPT
b+=img('pr_sales.png',285,1045,2.2,w=470,z=3)
b+=img('sl_black1.png',335,765,1.4,z=4)+txt('lab','ME WITH CHATGPT',335,767,1.4)
b+=badge('openai.svg',672,765,-5)
b+=img('sl_yel3.png',775,1035,-1.8,z=4)+txt('big','A table.<br>Then an offer<br>for a bigger one.',775,1035,-1.8,'font-size:50px')
page(b,'A')
