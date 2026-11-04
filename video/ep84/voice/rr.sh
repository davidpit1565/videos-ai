#!/bin/bash
cd /home/user/videos-ai; export PATH=/opt/v311/bin:$PATH
V=video/ep84/voice
SEEDS=(8601 8611 8621 8631 8641 8651)
E5=(0.66 0.70 0.64 0.68 0.66 0.70)
E7=(0.68 0.72 0.64 0.70 0.66 0.74)
E8=(0.66 0.70 0.64 0.72 0.68 0.64)
for i in 0 1 2 3 4 5; do
  B=${SEEDS[$i]}; [ -s $V/takes/r$B.wav ] && continue
  while pgrep -x "chrome|chrome-headless-shell|headless_shell" >/dev/null || [ $(free -m | awk 'NR==2{print $7}') -lt 7000 ]; do sleep 60; done
  python3 audio/build_voice.py --lines $V/rr.txt --out $V/takes/r$B.wav --exaggeration 0.66 --cfg 0.30 --seed $B --line-seeds "1:$((B+5)),2:$((B+7)),3:$((B+8))" --line-exaggeration "1:${E5[$i]},2:${E7[$i]},3:${E8[$i]}" --prosody-rolls 1 --retries 1 --no-verify > $V/takes/r$B.log 2>&1
  echo "rr done $B $(date +%T)" >> $V/progress.txt
done
echo RRDONE >> $V/progress.txt
