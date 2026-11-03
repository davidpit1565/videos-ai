#!/bin/bash
cd /home/user/videos-ai
export PATH=/opt/v311/bin:$PATH
V=video/ep83/voice
# wait for take 1 python to end
while pgrep -f "out video/ep83/voice/takes/t8301" >/dev/null; do sleep 5; done
echo "done 8301 $(date +%T)" >> $V/progress.txt
SEEDS=(8311 8321 8331 8341 8351 8361)
EXS=(0.80 0.78 0.82 0.78 0.80 0.64)
for i in 0 1 2 3 4 5; do
  B=${SEEDS[$i]}
  [ -f $V/takes/t$B.wav ] && continue
  E=${EXS[$i]}; H=$(python3 -c "print(min(0.88,$E+0.05))")
  LS=$(python3 -c "print(','.join(f'{n}:{$B+n}' for n in range(1,11)))")
  LE="1:$H,2:$E,3:$E,4:$E,5:$E,6:$E,7:$E,8:$E,9:$E,10:$E"
  python3 audio/build_voice.py --lines video/ep83/lines.txt --out $V/takes/t$B.wav --exaggeration $E --cfg 0.30 --seed $B --line-seeds "$LS" --line-exaggeration "$LE" --prosody-rolls 1 --retries 1 --no-verify > $V/takes/t$B.log 2>&1
  echo "done $B ex=$E $(date +%T)" >> $V/progress.txt
done
echo ALLDONE >> $V/progress.txt
