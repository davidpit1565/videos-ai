#!/bin/bash
# finish.sh <variant>  (needs out/narration-<v>.wav, out/cues-<v>.json, hf/index-<v>.html, out/<v>.mp4 silent render)
set -e
V=$1; S=/tmp/claude-0/-home-user-videos-ai/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/scratchpad/ep82; cd $S; P=/opt/v311/bin/python
$P - <<PY
import json
c=json.load(open('out/cues-$V.json'))
L=[dict(n=l['n'],line=l['text'],start=l['start'],end=l['end']) for l in c['lines']]
json.dump(dict(cues=L),open('out/vd-cues-$V.json','w'),indent=1); json.dump(L,open('out/cues-vq-$V.json','w'),indent=1)
PY
cd /home/user/videos-ai
$P audio/voice_doctor.py $S/out/narration-$V.wav --cues $S/out/vd-cues-$V.json --repair $S/out/narration-$V-r.wav --no-watch > $S/out/vd-$V.log 2>&1 || true
tail -4 $S/out/vd-$V.log
cd $S
D=$($P -c "import json;print(json.load(open('out/cues-$V.json'))['D'])")
$P mix.py out/narration-$V-r.wav out/$V.mp4 $D $V
