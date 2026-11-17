#!/usr/bin/env bash
cd "$(dirname "$0")"
for N in "$@"; do
  V=${N:2:4}; V=$(echo $N | sed -E 's/^v6(short|long).*/\1/')
  D=$(python3 -c "import json;print(json.load(open('cues-$N.json'))['D'])")
  OUT=$(python3 mix.py out/narration-$N.wav out/$N.mp4 $D $N 2>&1 | tail -2)
  FIX=$(echo "$OUT" | grep -oE "corrected by -?[0-9.]+" | grep -oE "\-?[0-9.]+$")
  VOL=$(python3 -c "import json;print(round(json.load(open('out/gain-$N-M.json'))['lin']*10**($FIX/20),3))")
  cp out/index-$N.html hf/index.html
  cd ../.. 
  ./export/check_hf.sh video/ep86v5/hf/index.html video/ep86v5/out/narration-$N.wav video/ep86v5/cues-$N.json video/ep86v5/out/ep86v5-$N-M.mp4 video/ep86v5/out/bed-M.wav $VOL > video/ep86v5/out/gate-$N.txt 2>&1
  cd video/ep86v5
  echo "== $N D=$D vol=$VOL"; grep -E "^  (PASS|FAIL|SKIP)|ALL CHECKS|<--|overlap  |overlaps:" out/gate-$N.txt
done
