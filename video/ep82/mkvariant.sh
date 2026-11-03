#!/bin/bash
# mkvariant.sh <tag> <line9.wav> "<line 9 text>" "<row2 words separated by |>"
set -e
V=$1; W=$2; TX=$3; ROW=$4
S=/tmp/claude-0/-home-user-videos-ai/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/scratchpad/ep82; cd $S; P=/opt/v311/bin/python
cp $W voice/final/9.wav
$P - <<PY
import re
L=open('lines.v1.txt').read().rstrip('\n').split('\n'); L[8]="""$TX"""; open('lines.txt','w').write('\n'.join(L)+'\n')
s=open('scenes/scene-9.v1.html').read().split('\n')
words="$ROW".split('|')
sty=['<span class="w sel s80" style="font-size:62px;margin-top:6px;padding:0 20px" data-w="%d">%s</span>','<span class="w sel" style="font-size:62px;margin-top:6px;padding:0 20px" data-w="%d">%s</span>']
row='  <div class="row">'+''.join((sty[0] if i==0 else sty[1])%(3+i,w) for i,w in enumerate(words))+'</div>'
i=[k for k,l in enumerate(s) if 'data-w="3"' in l][0]; s[i]=row
open('scenes/scene-9.html','w').write('\n'.join(s))
PY
$P build82.py --render $V 2>&1 | tail -2
cp out/narration.wav out/narration-$V.wav; cp cues.json out/cues-$V.json; cp hf/index.html hf/index-$V.html
./finish.sh $V
