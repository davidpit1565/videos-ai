#!/bin/bash
# one TTS job at a time; whole-script takes with different seeds
cd /home/user/videos-ai
export PATH=/opt/v311/bin:$PATH
V=video/ep83/voice
SEEDS=(8301 8311 8321 8331 8341 8351 8361 8371)
EXS=(0.78 0.80 0.78 0.82 0.78 0.80 0.64 0.70)
for i in 0 1 2 3 4 5 6 7; do
  B=${SEEDS[$i]}
  [ -f $V/takes/t$B.wav ] && continue
  E=${EXS[$i]}; H=$(python3 -c "print(min(0.88,$E+0.05))")
  LS=$(python3 -c "print(','.join(f'{n}:{$B+n}' for n in range(1,11)))")
  LE="1:$H,2:$E,3:$E,4:$E,5:$E,6:$E,7:$E,8:$E,9:$E,10:$E"
  python3 audio/build_voice.py --lines video/ep83/lines.txt --out $V/takes/t$B.wav --exaggeration $E --cfg 0.30 --seed $B --line-seeds "$LS" --line-exaggeration "$LE" > $V/takes/t$B.log 2>&1
  echo "done $B ex=$E $(date +%T)" >> $V/progress.txt
done
echo ALLDONE >> $V/progress.txt
