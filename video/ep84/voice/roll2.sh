#!/bin/bash
cd /home/user/videos-ai
export PATH=/opt/v311/bin:$PATH
V=video/ep84/voice
SEEDS=(8401 8411 8421 8431 8441 8451 8461 8471 8481 8491 8501 8511)
H1=(0.88 0.84 0.90 0.86 0.88 0.84 0.90 0.86 0.88 0.85 0.90 0.87)
H2=(0.84 0.80 0.86 0.82 0.84 0.80 0.86 0.82 0.84 0.81 0.86 0.83)
EX=(0.80 0.78 0.82 0.78 0.80 0.82 0.78 0.80 0.82 0.78 0.80 0.82)
echo "{}" > /dev/null
for i in 0 1 2 3 4 5 6 7 8 9 10 11; do
  B=${SEEDS[$i]}
  [ -s $V/takes/t$B.wav ] && continue
  E=${EX[$i]}
  LS=$(python3 -c "print(','.join(f'{n}:{$B+n}' for n in range(1,9)))")
  LE="1:${H1[$i]},2:${H2[$i]},3:$E,4:$E,5:$E,6:$E,7:$E,8:$E"
  free -m | awk 'NR==2{print "free MB",$7}' >> $V/progress.txt
  python3 audio/build_voice.py --lines video/ep84/lines.txt --out $V/takes/t$B.wav --exaggeration $E --cfg 0.30 --seed $B --line-seeds "$LS" --line-exaggeration "$LE" --prosody-rolls 1 --retries 1 --no-verify > $V/takes/t$B.log 2>&1
  python3 - <<PY
import json,os
f="$V/takes_ex.json"; d=json.load(open(f)) if os.path.exists(f) else {}
d["$B"]=[$E,${H1[$i]},${H2[$i]}]; json.dump(d,open(f,"w"))
PY
  echo "done $B ex=$E h1=${H1[$i]} h2=${H2[$i]} $(date +%T)" >> $V/progress.txt
done
echo ALLDONE >> $V/progress.txt
