cd /home/user/videos-ai; V=video/nextreel-git/voice
EX=$(cut -d'|' -f1 $V/rT.args); SD=$(cut -d'|' -f2 $V/rT.args)
/opt/v311/bin/python audio/build_voice.py --lines $V/rT.txt --out $V/takeT.wav --exaggeration 0.78 --cfg 0.30 --seed 12000 --line-exaggeration "$EX" --line-seeds "$SD" --prosody-rolls 2 --retries 1 > $V/takeT.log 2>&1
echo DONE >> $V/takeT.log
