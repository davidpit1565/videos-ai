#!/bin/bash
# roll.sh: one TTS at a time. kind=B (body line i from body.txt) or H (hook i from hooks.txt). Takes pl/<K><i>-<seed>.wav
cd /home/user/videos-ai; D=video/ep106/voice; PY=/opt/v311/bin/python
SEEDS=${SEEDS:-"11 22 33"}
run() { # kind idx exa
  local K=$1 i=$2 E=$3 f=$D/body.txt; [ $K = H ] && f=$D/hooks.txt
  sed -n "${i}p" $f > $D/pl/$K$i.txt
  for seed in $SEEDS; do
    [ -f $D/pl/$K$i-$seed.wav ] && continue
    flock /tmp/tts.lock $PY audio/build_voice.py --lines $D/pl/$K$i.txt --out $D/pl/$K$i-$seed.wav --exaggeration $E --cfg 0.30 --gap 0.06 --long 0.15 --max-speedup 1.45 --min-rate 5.8 --no-verify --line-seeds "1:$seed" > $D/pl/log-$K$i.txt 2>&1 < /dev/null
    sc=$($PY audio/check_accent.py --cues $D/pl/$K$i-$seed-cues.json $D/pl/$K$i-$seed.wav 2>&1 < /dev/null | grep "ln 1" | sed 's/.*not-american=\([0-9.]*\).*/\1/')
    echo "$K$i seed $seed E=$E accent $sc" >> $D/pl/out.txt
  done
}
EXAH=${EXAH:-0.82}
if [ -z "$ONLYB$ONLYH" ] || [ -n "$ONLYH" ]; then for i in ${ONLYH:-1 2 3 4 5}; do run H $i $EXAH; done; fi
if [ -z "$ONLYB$ONLYH" ] || [ -n "$ONLYB" ]; then
EXA=(0.76 0.70 0.68 0.68 0.68 0.68 0.70 0.70 0.68 0.70)
for i in ${ONLYB:-1 2 3 4 5 6 7 8 9 10}; do run B $i ${EXA_B:-${EXA[$((i-1))]}}; done; fi
echo DONE >> $D/pl/out.txt
