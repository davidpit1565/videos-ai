cd /home/user/videos-ai; V=video/nextreel-git/voice
/opt/v311/bin/python audio/build_voice.py --lines $V/rS.txt --out $V/takeS.wav --exaggeration 0.78 --cfg 0.30 --seed 9900 --line-exaggeration "1:0.84,2:0.78,3:0.9,4:0.72,5:0.82,6:0.76,7:0.88,8:0.8" --line-seeds "1:11001,2:11002,3:11003,4:11004,5:11005,6:11006,7:11007,8:11008" --prosody-rolls 2 --retries 1 > $V/takeS.log 2>&1
echo DONE >> $V/takeS.log
