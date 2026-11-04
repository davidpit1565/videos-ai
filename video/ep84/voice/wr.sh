#!/bin/bash
cd /home/user/videos-ai; export PATH=/opt/v311/bin:$PATH
V=video/ep84/voice
SEEDS=(9301 9311 9321 9331 9341 9351 9361 9371 9381 9391 9401 9411 9421 9431 9441 9451)
EX=(0.92 0.96 1.00 0.88 0.94 0.90 0.98 0.92 0.96 1.00 0.88 0.94 0.90 0.98 0.92 0.96)
for i in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do
  B=${SEEDS[$i]}; [ -s $V/takes/f$B.wav ] && continue
  F=$V/h1.txt; [ $((i%2)) -eq 1 ] && F=$V/h1c.txt
  while pgrep -x "chrome|chrome-headless-shell|headless_shell" >/dev/null || [ $(free -m | awk 'NR==2{print $7}') -lt 7000 ]; do sleep 60; done
  python3 audio/build_voice.py --lines $F --out $V/takes/f$B.wav --exaggeration ${EX[$i]} --cfg 0.25 --seed $B --line-seeds "1:$((B+1))" --line-exaggeration "1:${EX[$i]}" --min-rate 5.0 --max-speedup 1.4 --no-prosody --retries 0 --no-verify > $V/takes/f$B.log 2>&1
  echo "w done $B $(basename $F) $(date +%T)" >> $V/progress.txt
done
echo WWDONE >> $V/progress.txt
