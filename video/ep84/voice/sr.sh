#!/bin/bash
cd /home/user/videos-ai; export PATH=/opt/v311/bin:$PATH
V=video/ep84/voice
SEEDS=(9101 9111 9121 9131 9141 9151 9161 9171 9181 9191 9201 9211)
E1=(0.95 0.90 1.00 0.92 0.95 0.88 1.00 0.92 0.90 0.96 0.94 0.98)
E2=(0.64 0.60 0.70 0.66 0.62 0.70 0.60 0.64 0.68 0.62 0.66 0.60)
E3=(0.95 1.00 0.92 0.98 0.90 1.00 0.95 0.92 0.98 0.90 1.00 0.94)
for i in 0 1 2 3 4 5 6 7 8 9 10 11; do
  B=${SEEDS[$i]}; [ -s $V/takes/s$B.wav ] && continue
  while pgrep -x "chrome|chrome-headless-shell|headless_shell" >/dev/null || [ $(free -m | awk 'NR==2{print $7}') -lt 7000 ]; do sleep 60; done
  python3 audio/build_voice.py --lines $V/seg.txt --out $V/takes/s$B.wav --exaggeration 0.9 --cfg 0.25 --seed $B --line-seeds "1:$((B+1)),2:$((B+2)),3:$((B+3))" --line-exaggeration "1:${E1[$i]},2:${E2[$i]},3:${E3[$i]}" --min-rate 1 --max-speedup 1.0 --no-prosody --retries 0 --no-verify > $V/takes/s$B.log 2>&1
  echo "s done $B $(date +%T)" >> $V/progress.txt
done
echo SSDONE >> $V/progress.txt
