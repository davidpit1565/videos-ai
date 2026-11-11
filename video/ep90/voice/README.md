Narration for the ghost reels (ep90 recording version and ep90b drawn version), cloned voice, ONE TTS render.
Lines (lines5.txt, true to the real run): 1 I gave ChatGPT a 47-day timeout. 2 I asked it to pick a number. It picked 47. 3 So I said: no talking for 47 days. 4 It begged: can I have a second chance? 5 I said yes. 6 And it still chose 100. 7 Send this to someone who ghosts you.
Commands:
  python3 audio/script_lint.py --text "<the 7 lines>"   -> only "number" flagged (unstressed -ER); NOT reworded (word-for-word was asked); voice_doctor did not flag its ending.
  bash video/ep90/voice/gen5.sh  = /opt/v311/bin/python audio/build_voice.py --lines video/ep90/voice/lines5.txt --out video/ep90/voice/v5.wav --exaggeration 0.74 --line-exaggeration "1:0.80,4:0.78,6:0.78,7:0.78" --line-seeds "1:4101,...,7:4107" --gap 0.18 --min-rate 5.2 --retries 5 --pauses "5,6" --watch ""   (render about 9 min, v5.wav 20.5 s, raw lines in v5-cues.json)
  ffmpeg -i v5.wav -af atempo=1.15 -ar 48000 -ac 1 -c:a pcm_s16le v5-fast.wav   (fast take like ep89b; the raw voice is slow)
  /opt/v311/bin/python mkcues.py  (faster-whisper word times -> cues.json, copied to cues-fast-raw.json)  then  python3 assemble.py  -> narration90.wav (48 kHz mono 16-bit) + cues.json with line start/end and word times, gaps 0.34/0.34/0.34/0.40/0.85/0.85 s
Checks: voice_doctor (no BAD, nothing flagged); voice_quality: clean except line 3 pitch range 11.5 st at the exact window (9.8-10.8 st with the window start moved by -0.06/+0.05/+0.1 s: pyin edge, same effect seen on ep89c line 4), tone clean. Accent check SKIPPED (transformers not installed). Measured, not heard.
Whisper hears "chose" in line 6 as "shows" and "begged:" as "begged." - listen to line 6 before shipping.
