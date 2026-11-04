#!/bin/bash
cd /home/user/videos-ai; export PATH=/opt/v311/bin:$PATH
V=video/ep84/voice
SEEDS=(9501 9511 9521 9531 9541 9551 9561 9571)
EX=(0.80 0.78 0.82 0.80 0.78 0.82 0.80 0.79)
for i in 0 1 2 3 4 5 6 7; do
  B=${SEEDS[$i]}; [ -s $V/takes/l$B.wav ] && continue
  while pgrep -x "chrome|chrome-headless-shell|headless_shell" >/dev/null || [ $(free -m | awk 'NR==2{print $7}') -lt 7000 ]; do sleep 60; done
  python3 audio/build_voice.py --lines $V/l2.txt --out $V/takes/l$B.wav --exaggeration ${EX[$i]} --cfg 0.30 --seed $B --line-seeds "1:$((B+2))" --line-exaggeration "1:${EX[$i]}" --prosody-rolls 1 --retries 1 --no-verify > $V/takes/l$B.log 2>&1
  echo "l done $B ex=${EX[$i]} $(date +%T)" >> $V/progress.txt
done
echo LLDONE >> $V/progress.txt
