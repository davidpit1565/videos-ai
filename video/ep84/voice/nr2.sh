#!/bin/bash
cd /home/user/videos-ai; export PATH=/opt/v311/bin:$PATH
V=video/ep84/voice
SEEDS=(8801 8811 8821 8831 8841 8851)
EX=(0.88 0.84 0.90 0.86 0.88 0.82)
for i in 0 1 2 3 4 5; do
  B=${SEEDS[$i]}; [ -s $V/takes/n$B.wav ] && continue
  while pgrep -x "chrome|chrome-headless-shell|headless_shell" >/dev/null || [ $(free -m | awk 'NR==2{print $7}') -lt 7000 ]; do sleep 60; done
  python3 audio/build_voice.py --lines $V/h1.txt --out $V/takes/n$B.wav --exaggeration ${EX[$i]} --cfg 0.30 --seed $B --line-seeds "1:$((B+1))" --line-exaggeration "1:${EX[$i]}" --prosody-rolls 1 --retries 1 --no-verify > $V/takes/n$B.log 2>&1
  echo "n done $B ex=${EX[$i]} $(date +%T)" >> $V/progress.txt
done
echo N2DONE >> $V/progress.txt
