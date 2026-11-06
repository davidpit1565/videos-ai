#!/usr/bin/env bash
# builds short/long x excited/calm hook; mixes each. usage: bash runall.sh
cd "$(dirname "$0")"
for V in short long; do
 for H in exc calm; do
  if [ $H = calm ]; then VO=voice/calm; WD=voice/words-calm.json; else VO=voice/final; WD=voice/words.json; fi
  N=$V-$H
  [ -f out/ep86v5-$N-M.mp4 ] && continue
  VOICE=$VO WORDS=$WD V=$V python3 build.py --render $N 2>&1 | grep -E "rror" 
  D=$(python3 -c "import json;print(json.load(open('cues-$V.json'))['D'])")
  cp out/narration-$V.wav out/narration-$N.wav; cp cues-$V.json cues-$N.json; cp hf/index.html out/index-$N.html
  python3 mix.py out/narration-$N.wav out/$N.mp4 $D $N 2>&1 | tail -1
  echo done $N D=$D
 done
done
