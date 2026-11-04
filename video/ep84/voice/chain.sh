#!/bin/bash
V=/home/user/videos-ai/video/ep84/voice
until grep -q ALLDONE $V/progress.txt; do sleep 5; done
for s in 8411 8421 8431 8441 8451 8461 8471 8481 8491 8501 8511; do rm $V/takes/t$s.wav; done
sed -i '/ALLDONE/d' $V/progress.txt
exec bash $V/roll2.sh
