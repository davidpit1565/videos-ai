ep91 narration, ep89 recipe: exaggeration 0.78, hook line 0.90, lines 3 and 4 at 0.82, gap 0.18, min-rate 5.4, retries 5, seeds 6201-6204, fast take atempo 1.12.
Lines: 1 Me with Claude. It listens. | 2 Me with ChatGPT. It's way more tangled. | 3 Which one are you? | 4 Send this to the friend who overcomplicates everything.
Wording: "complicated" is flagged by script_lint (flapped T), so line 2 now says "tangled" (script_lint: 0 risky words).
Commands:
  bash video/ep91/voice/gen91b.sh   (build_voice.py -> w91b.wav raw 11.8 s, w91b-cues.json)
  /opt/v311/bin/python audio/mk_voice_cues.py video/ep91/voice/w91b.wav video/ep91/voice/w91b-cues.json video/ep91/voice/narration91b.wav video/ep91/voice/cues91b.json 1.12
Result: narration91b.wav 10.56 s (48 kHz mono 16-bit), cues91b.json (line start/end + whisper word times).
Checks: script_lint 0 risky words; voice_doctor no BAD (only the 0.16 s gap note of the recipe); voice_quality: clean (line 1 range 9.7 st, close to the 10 st limit). Accent check skipped (transformers not installed). Measured, not heard.
Endings for David's ear (voice_doctor end level): line 3 "you?" -41 dB, line 4 "everything." -38 dB, line 2 "tangled." -33 dB, line 1 "listens." -19 dB.
