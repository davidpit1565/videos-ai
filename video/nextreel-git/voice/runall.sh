cd /home/user/videos-ai
for N in H P; do V=video/nextreel-git/voice
EX=$(cut -d'|' -f1 $V/r$N.args); SD=$(cut -d'|' -f2 $V/r$N.args)
/opt/v311/bin/python audio/build_voice.py --lines $V/r$N.txt --out $V/take$N.wav --exaggeration 0.78 --cfg 0.30 --seed 9700 --line-exaggeration "$EX" --line-seeds "$SD" --prosody-rolls 2 --retries 1 > $V/take$N.log 2>&1
echo DONE >> $V/take$N.log; done
