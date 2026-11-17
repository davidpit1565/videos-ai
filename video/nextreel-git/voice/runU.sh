cd /home/user/videos-ai; V=video/nextreel-git/voice
/opt/v311/bin/python audio/build_voice.py --lines $V/rU.txt --out $V/takeU.wav --exaggeration 0.78 --cfg 0.30 --seed 13000 --line-exaggeration "1:0.84,2:0.78,3:0.72,4:0.80,5:0.76" --line-seeds "1:13001,2:13002,3:13003,4:13004,5:13005" --prosody-rolls 2 --retries 1 > $V/takeU.log 2>&1
echo DONE >> $V/takeU.log
