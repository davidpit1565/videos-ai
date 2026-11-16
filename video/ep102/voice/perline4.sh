#!/bin/bash
# v4 voice: only the changed lines (1,3,4,5), one TTS at a time (flock). Keeps EVERY seed's take in pl3/ and logs the accent score;
# the take is chosen afterwards by Whisper text, word gaps, accent and pitch (voice/wcand.py), not by the first pass.
cd /home/user/videos-ai; D=video/ep102/voice
declare -A TXT=( [4]="For Calendly, Cal D I Y. For Intercom, Chat woot." )
for i in ${LINES_TODO:-1 3 4 5}; do
  if [ -n "${TXT[$i]}" ]; then echo "${TXT[$i]}" > $D/pl3/line$i.txt; else sed -n "${i}p" $D/lines.txt > $D/pl3/line$i.txt; fi
  [ -n "$TEXT" ] && echo "$TEXT" > $D/pl3/line$i.txt
  for seed in ${SEEDS:-11 22 33}; do
    flock /tmp/tts.lock /opt/v311/bin/python audio/build_voice.py --lines $D/pl3/line$i.txt --out $D/pl3/L$i-$seed.wav --exaggeration ${EXA:-0.72} --cfg 0.30 --gap 0.06 --long 0.15 --max-speedup 1.45 --min-rate 5.8 --no-verify --line-seeds "1:$seed" > $D/pl3/log.txt 2>&1 < /dev/null
    sc=$(/opt/v311/bin/python audio/check_accent.py --cues $D/pl3/L$i-$seed-cues.json $D/pl3/L$i-$seed.wav 2>&1 < /dev/null | grep "ln 1" | sed 's/.*not-american=\([0-9.]*\).*/\1/')
    echo "L$i seed $seed accent $sc" >> $D/pl3/out.txt
  done
done
echo DONE >> $D/pl3/out.txt
