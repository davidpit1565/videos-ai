#!/bin/bash
cd /home/user/videos-ai; export PATH=/opt/v311/bin:$PATH
V=video/ep84/voice
SEEDS=(8901 8911 8921 8931 8941 8951 8961 8971 8981 8991 9001 9011)
EX=(1.00 0.96 0.92 0.85 1.00 0.96 0.92 0.85 0.98 0.94 0.90 0.88)
CFG=(0.30 0.25 0.20 0.30 0.20 0.30 0.25 0.20 0.25 0.30 0.20 0.25)
SP=(1.2 1.2 1.2 1.2 1.5 1.5 1.5 1.5 1.5 1.5 1.5 1.5)
for i in 0 1 2 3 4 5 6 7 8 9 10 11; do
  B=${SEEDS[$i]}; [ -s $V/takes/f$B.wav ] && continue
  while pgrep -x "chrome|chrome-headless-shell|headless_shell" >/dev/null || [ $(free -m | awk 'NR==2{print $7}') -lt 7000 ]; do sleep 60; done
  python3 audio/build_voice.py --lines $V/h1.txt --out $V/takes/f$B.wav --exaggeration ${EX[$i]} --cfg ${CFG[$i]} --seed $B --line-seeds "1:$((B+1))" --line-exaggeration "1:${EX[$i]}" --min-rate 5.5 --max-speedup ${SP[$i]} --prosody-rolls 1 --retries 1 --no-verify > $V/takes/f$B.log 2>&1
  echo "f done $B ex=${EX[$i]} cfg=${CFG[$i]} sp=${SP[$i]} $(date +%T)" >> $V/progress.txt
done
echo FFDONE >> $V/progress.txt
