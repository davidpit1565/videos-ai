ep90 narration, ep89 recipe (video/ep89b/voice/README.md): exaggeration 0.78, hook line 0.90, lines 4/6/7 0.82, gap 0.18, min-rate 5.4, retries 5, long pause (0.85 s) after lines 5 and 6, seeds 6101-6107, then fast take atempo 1.12.
Commands:
  bash video/ep90/voice/gen6.sh   (build_voice.py; w6.wav = raw render, w6-cues.json raw line times; render about 40 min because another TTS ran in parallel)
  /opt/v311/bin/python audio/mk_voice_cues.py video/ep90/voice/w6.wav video/ep90/voice/w6-cues.json video/ep90/voice/narration90b.wav video/ep90/voice/cues90b.json 1.12
Result: narration90b.wav 16.78 s (48 kHz mono 16-bit), cues90b.json (line start/end + whisper word times).
Checks: script_lint flagged only "number" (kept, word-for-word); voice_doctor: no BAD, only the "gap under 0.3 s" notes (the recipe's 0.18 s gap; same as ep89); voice_quality: line 6 pitch range 10.8 st at the exact window (pyin edge, see the shifted-window numbers in the report), tone clean. Accent check skipped (transformers not installed). Measured, not heard.
Line endings for David's ear (voice_doctor "end" level in dB, softer = more risk): line 2 "47." -45.1, line 7 "you." -38.1, line 6 "100." -33.4, line 1 "timeout." -28.3.
