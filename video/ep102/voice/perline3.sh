#!/bin/bash
# v3 voice: only the changed lines (1,3,4,5,6,7), one TTS at a time (flock), seed loop until the accent check passes. Files in pl2/.
cd /home/user/videos-ai; D=video/ep102/voice
declare -A TXT=( [3]="Loom? Try Cap. Notion? App Flowy." [5]="Intercom? Chat woot, if you host it." )
declare -A EX=( [3]=0.74 [4]=0.74 [5]=0.74 [6]=0.70 )
for i in ${LINES_TODO:-3 4 5 6}; do
  [ -f $D/pl2/L$i.ok ] && continue
  if [ -n "${TXT[$i]}" ]; then echo "${TXT[$i]}" > $D/pl2/line$i.txt; else sed -n "${i}p" $D/lines.txt > $D/pl2/line$i.txt; fi
  for seed in ${SEEDS:-11 22 33 44 55 66}; do
    flock /tmp/tts.lock /opt/v311/bin/python audio/build_voice.py --lines $D/pl2/line$i.txt --out $D/pl2/L$i-$seed.wav --exaggeration ${E_OVERRIDE:-${EX[$i]}} --cfg 0.30 --gap 0.06 --long 0.15 --max-speedup 1.45 --min-rate 5.8 --no-verify --line-seeds "1:$seed" > $D/pl2/log.txt 2>&1 < /dev/null
    sc=$(/opt/v311/bin/python audio/check_accent.py --cues $D/pl2/L$i-$seed-cues.json $D/pl2/L$i-$seed.wav 2>&1 < /dev/null | grep "ln 1" | sed 's/.*not-american=\([0-9.]*\).*/\1/')
    echo "L$i seed $seed accent $sc" >> $D/pl2/out.txt
    if python3 -c "import sys;sys.exit(0 if float('${sc:-1}')<0.15 else 1)"; then echo $seed > $D/pl2/L$i.ok; break; fi
  done
done
echo DONE >> $D/pl2/out.txt
